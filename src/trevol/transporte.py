"""El transporte: lo que hace que las llamadas se comporten igual en los 7 SDK (docs/api/43 §2.6.2 a §2.6.5).

Se conecta al código generado subclaseando `ApiClient`: `param_serialize` sabe QUÉ operación es (conoce la plantilla de la ruta) y pone la
Idempotency-Key; `call_api` pone las cabeceras, reintenta y convierte toda respuesta que no es 2xx en un error tipado que atraviesa el
código generado sin envolverse (`ApiClient.call_api` solo relanza `ApiException`).
"""

from __future__ import annotations

import random as _azar_modulo
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

import urllib3

from trevol._generado.api_client import ApiClient
from trevol._generado.configuration import Configuration
from trevol._generado.exceptions import ApiException
from trevol._generado.tablas import CLASE_POR_CODE, CLASE_POR_ESTADO, OPERACIONES

from .errores import APIConnectionError, ConfigurationError, error_de_respuesta

_ESTADOS_REINTENTABLES = frozenset({429, 500, 502, 503, 504})
_CODES_EN_CURSO = frozenset({"request_in_progress", "previous_event_pending"})


@dataclass(frozen=True)
class Resultado:
    """Qué pasó en un intento: `respuesta` (con `estado`) o `red` (sin respuesta)."""

    tipo: str
    estado: Optional[int] = None
    code: Optional[str] = None
    retryable: Optional[bool] = None
    #: Segundos, ya resueltos (cabecera o `retry_after` del cuerpo).
    retry_after: Optional[float] = None


@dataclass(frozen=True)
class Decision:
    reintentar: bool
    #: Segundos a esperar antes del siguiente intento.
    espera: Optional[float] = None
    #: `exito`, `agotado` o `retry_after_excede` cuando el «no» tiene una razón que contar.
    motivo: Optional[str] = None


def espera_propia(intento: int, azar: float) -> float:
    """La espera propia antes del intento siguiente: 0,5 · 2^(intento−1), con tope de 8 s, por un factor al azar en [0,75; 1]."""
    return min(0.5 * 2 ** (intento - 1), 8.0) * (0.75 + 0.25 * azar)


def decidir(*, intento: int, reintento: str, max_reintentos: int, max_retry_after: float, azar: float, resultado: Resultado) -> Decision:
    """Función PURA: ¿se reintenta y cuánto se espera? Las mismas reglas y los mismos casos (`pruebas/datos/transporte.json`) en los 7 SDK."""
    r = resultado
    if r.tipo == "respuesta" and 200 <= (r.estado or 0) < 300:
        return Decision(False, motivo="exito")
    if r.tipo == "red":
        reintentable = reintento == "seguro"
    else:
        estado = r.estado or 0
        if reintento == "solo_429":
            reintentable = estado == 429
        elif estado == 402:
            reintentable = False
        else:
            reintentable = estado in _ESTADOS_REINTENTABLES or (bool(r.code) and r.code in _CODES_EN_CURSO) or r.retryable is True
    if not reintentable:
        return Decision(False)
    if intento > max_reintentos:
        return Decision(False, motivo="agotado")
    propia = espera_propia(intento, azar)
    pedida = r.retry_after if r.tipo == "respuesta" and r.retry_after and r.retry_after > 0 else 0.0
    if pedida > max_retry_after:
        return Decision(False, motivo="retry_after_excede")
    return Decision(True, espera=max(pedida, propia))


# ── La Idempotency-Key ──────────────────────────────────────────────────────
def validar_clave(clave: str) -> None:
    if not (1 <= len(clave) <= 255) or any(not ("!" <= c <= "~") for c in clave):
        raise ConfigurationError("La idempotency_key debe tener de 1 a 255 caracteres ASCII visibles (sin espacios).")


@dataclass
class Opciones:
    llave: str
    api_version: str
    user_agent: str
    max_reintentos: int = 2
    #: Segundos por intento.
    timeout: float = 65.0
    max_retry_after: float = 60.0
    sleep: Callable[[float], None] = time.sleep
    random: Callable[[], float] = _azar_modulo.random
    uuid: Callable[[], str] = field(default=lambda: str(uuid.uuid4()))

    def __repr__(self) -> str:                      # la llave nunca sale en un repr, un log ni un traceback
        return f"Opciones(api_version={self.api_version!r}, max_reintentos={self.max_reintentos!r}, timeout={self.timeout!r})"


_OPERACIONES = {(o["metodo"], o["ruta"]): o for o in OPERACIONES}
# Lo que la API contesta: el archivo (o JSON) si sale bien, y problem+json si no. Así lo pide el SDK (un servidor simulado que negocia por
# `Accept`, como Prism, solo ofrece el error si lo aceptas; el generado elige solo uno de los dos).
_PROBLEMA = "application/problem+json"
_ACCEPT = {"pdf": f"application/pdf, {_PROBLEMA}", "xml": f"application/xml, {_PROBLEMA}", "zip": f"application/zip, {_PROBLEMA}",
           "json": f"application/json, {_PROBLEMA}"}


class ClienteApi(ApiClient):
    """El `ApiClient` generado con la capa de Trevol: cabeceras, Idempotency-Key, reintentos y errores tipados."""

    def __init__(self, configuration: Configuration, opciones: Opciones) -> None:
        super().__init__(configuration)
        self._o = opciones
        self._local = threading.local()
        self.user_agent = opciones.user_agent

    # Aquí se sabe QUÉ operación es: `resource_path` es la plantilla («/invoices/{id}/pdf»).
    def param_serialize(self, method, resource_path, path_params=None, query_params=None, header_params=None, body=None,
                        post_params=None, files=None, auth_settings=None, collection_formats=None, _host=None, _request_auth=None):
        op = _OPERACIONES.get((str(method).upper(), resource_path))
        cabeceras = dict(header_params or {})
        clave: Optional[str] = None
        if op and op["idempotente"]:
            dada = cabeceras.get("Idempotency-Key")
            if dada is not None:
                validar_clave(str(dada))
            clave = str(dada) if dada is not None else self._o.uuid()
            cabeceras["Idempotency-Key"] = clave           # UNA clave por llamada: la misma en todos los reintentos
        else:
            cabeceras.pop("Idempotency-Key", None)
        self._local.contexto = (op, clave)
        return super().param_serialize(method, resource_path, path_params, query_params, cabeceras, body, post_params, files,
                                       auth_settings, collection_formats, _host, _request_auth)

    def call_api(self, method, url, header_params=None, body=None, post_params=None, _request_timeout=None):
        op, clave = getattr(self._local, "contexto", (None, None))
        self._local.contexto = (None, None)
        metodo = str(method).upper()
        reintento = op["reintento"] if op else ("seguro" if metodo == "GET" else "solo_429")
        cabeceras = dict(header_params or {})
        cabeceras["Authorization"] = f"Bearer {self._o.llave}"
        cabeceras["Trevol-Version"] = self._o.api_version
        cabeceras["Accept"] = _ACCEPT.get((op or {}).get("binario") or "json", "*/*")
        timeout = _request_timeout if _request_timeout is not None else self._o.timeout
        intento = 0
        while True:
            intento += 1
            causa: Optional[BaseException] = None
            respuesta = None
            try:
                respuesta = self.rest_client.request(method, url, headers=cabeceras, body=body, post_params=post_params,
                                                     _request_timeout=timeout)
                respuesta.read()
            except ApiException as e:                       # el generado convierte los fallos de TLS en ApiException(status=0)
                if e.status not in (0, None):
                    raise
                causa = e
            except (urllib3.exceptions.HTTPError, OSError) as e:
                causa = e
            if causa is None and respuesta is not None:
                if 200 <= respuesta.status < 300:
                    return respuesta
                texto = (respuesta.data or b"").decode("utf-8", "replace")
                error = error_de_respuesta(respuesta.status, texto, dict(respuesta.headers.items()), CLASE_POR_CODE, CLASE_POR_ESTADO, clave)
                decision = decidir(
                    intento=intento, reintento=reintento, max_reintentos=self._o.max_reintentos, max_retry_after=self._o.max_retry_after,
                    azar=self._o.random(), resultado=Resultado("respuesta", respuesta.status, error.code, error.retryable, error.retry_after))
                if not decision.reintentar:
                    raise error
            else:
                decision = decidir(intento=intento, reintento=reintento, max_reintentos=self._o.max_reintentos,
                                   max_retry_after=self._o.max_retry_after, azar=self._o.random(), resultado=Resultado("red"))
                if not decision.reintentar:
                    detalle = (getattr(causa, "reason", None) or str(causa) or type(causa).__name__) if causa else "no hubo respuesta"
                    raise APIConnectionError(f"No pude conectar con la API de Trevol ({str(detalle)[:200]}).", idempotency_key=clave) from causa
            self._o.sleep(decision.espera or 0.0)


def configuracion(base_url: str, proxy: Optional[str] = None) -> Configuration:
    """La `Configuration` generada, sin los reintentos de urllib3 (el SDK es el único que reintenta: C14)."""
    c = Configuration(host=base_url)
    c.retries = 0
    if proxy:
        c.proxy = proxy
    return c
