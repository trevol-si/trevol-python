"""Verificación de webhooks (docs/api/43 §2.6.9): Standard Webhooks sobre el CUERPO CRUDO, con la biblioteca abierta `standardwebhooks`
(PyPI, MIT) y las defensas que ella no tiene: acepta cualquier mapa de cabeceras (Flask, Django, FastAPI/Starlette, `dict`), texto o bytes;
exige que `webhook-timestamp` sean solo dígitos (la biblioteca acepta «1e3» o «nan»); y rechaza un cuerpo ya parseado con un mensaje que dice
cómo leer el crudo. Los errores de la biblioteca (incluidos los `ValueError` de una firma mal formada) son siempre `WebhookVerificationError`.
"""

from __future__ import annotations

import re
from typing import Any, Mapping, Optional, Union

from standardwebhooks import Webhook as _Estandar

from trevol._generado.models.event import Event
from trevol._generado.tablas import EVENTO_MODELOS

from .errores import ConfigurationError, WebhookVerificationError

_NOMBRES = ("webhook-id", "webhook-timestamp", "webhook-signature")
_DIGITOS = re.compile(r"[0-9]{1,12}")


def normalizar_cabeceras(cabeceras: Any) -> dict[str, str]:
    """Las tres cabeceras en minúsculas, venga lo que venga (un mapa, una lista de pares, valores en lista). La primera repetida gana."""
    pares: Any
    if hasattr(cabeceras, "items"):
        pares = cabeceras.items()
    else:
        pares = cabeceras or []
    salida: dict[str, str] = {}
    for k, v in pares:
        nombre = str(k).lower()
        if isinstance(v, (list, tuple)):
            v = v[0] if v else None
        if nombre in _NOMBRES and v is not None and nombre not in salida:
            salida[nombre] = v.decode("latin-1") if isinstance(v, bytes) else str(v)
    return salida


class Webhook:
    """`Webhook(secreto).verify(cuerpo_crudo, cabeceras) → Event`."""

    def __init__(self, secret: str) -> None:
        """`secret`: el secreto del endpoint (`whsec_…`), que se muestra una sola vez al crearlo o rotarlo."""
        if not isinstance(secret, str) or not secret.strip():
            raise ConfigurationError("Falta el secreto del webhook (whsec_…). Se muestra una sola vez al crear o rotar el endpoint.")
        try:
            self._verificador = _Estandar(secret.strip())
        except Exception as e:                     # base64 inválido, vacío…: nunca se cuenta el secreto
            raise ConfigurationError("El secreto del webhook no tiene el formato esperado (whsec_ + base64).") from None

    def verify(self, body: Union[str, bytes, bytearray, memoryview], headers: Mapping[str, Any]) -> Event:
        """Verifica la firma y la fecha de una entrega y devuelve el evento. Lanza `WebhookVerificationError` si algo no cuadra.

        Ojo: la verificación NO evita repeticiones dentro de los 5 minutos ni los reintentos de entrega: deduplica por `webhook-id`.
        """
        if isinstance(body, (bytes, bytearray, memoryview)):
            try:
                texto = bytes(body).decode("utf-8")
            except UnicodeDecodeError:
                raise WebhookVerificationError("El cuerpo del webhook no es UTF-8.", "cuerpo") from None
        elif isinstance(body, str):
            texto = body
        else:
            raise WebhookVerificationError(
                "El cuerpo del webhook debe ser el CUERPO CRUDO (str o bytes), no un objeto ya parseado: la firma se calcula sobre los "
                "bytes exactos. En Flask usa request.get_data(); en FastAPI, await request.body(); en Django, request.body.",
                "cuerpo",
            )
        h = normalizar_cabeceras(headers)
        for n in _NOMBRES:
            if not h.get(n):
                raise WebhookVerificationError(f"Falta la cabecera {n}.", "cabeceras")
        if not _DIGITOS.fullmatch(h["webhook-timestamp"]):
            raise WebhookVerificationError("El webhook-timestamp no es un número de segundos.", "fecha")
        try:
            self._verificador.verify(texto, h, json_parse=False)
        except Exception as e:
            m = str(e)
            if "timestamp" in m.lower():
                raise WebhookVerificationError(f"La fecha del webhook está fuera de la tolerancia de 5 minutos ({m}).", "fecha") from None
            if "headers" in m.lower():
                raise WebhookVerificationError("Las cabeceras del webhook no son válidas.", "cabeceras") from None
            raise WebhookVerificationError(
                "La firma del webhook no coincide: revisa el secreto y que el cuerpo sea el crudo, sin reescribir.", "firma") from None
        try:
            return Event.from_json(texto)  # type: ignore[return-value]
        except Exception:
            raise WebhookVerificationError("El cuerpo firmado no es un evento válido.", "cuerpo") from None

    def event_data(self, evento: Event) -> Optional[Any]:
        """Los `data` del evento como el modelo de su `type` (p. ej. `DocumentEventData` para `invoice.accepted`). `None` si el tipo es
        nuevo y este SDK todavía no lo conoce: el evento no se pierde, `evento.data` sigue ahí como mapa."""
        modelo = EVENTO_MODELOS.get(str(evento.type))
        return modelo.from_dict(evento.data) if modelo is not None and evento.data is not None else None
