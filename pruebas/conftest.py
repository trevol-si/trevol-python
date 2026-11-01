"""Ayudas de las pruebas: un servidor HTTP falso en localhost (pasa por urllib3 de verdad) y un cliente con reloj y azar inyectados."""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable, Optional

import pytest

from trevol import Trevol

DATOS = Path(__file__).parent / "datos"
HEX = "3f0c1a2b" * 8
LLAVE_TEST = "tvl_test_" + "a1" * 32
LLAVE_LIVE = "tvl_live_" + "b2" * 32
DOCUMENTO = {"id": "inv_" + HEX[:32], "object": "invoice", "environment": "test", "status": "accepted", "number": "SETP990012345",
             "external_id": "VENTA-2026-000123"}
ENTRADA_FACTURA = {"external_id": "VENTA-2026-000123", "customer": {"final_consumer": True},
                   "items": [{"description": "Café", "quantity": "1", "unit_price": "1000"}]}


def datos(nombre: str) -> Any:
    return json.loads((DATOS / nombre).read_text(encoding="utf-8"))


class Respuesta:
    def __init__(self, estado: int, cuerpo: Any = None, cabeceras: Optional[dict] = None, crudo: Optional[bytes] = None,
                 tipo: str = "application/json"):
        self.estado, self.cabeceras, self.tipo = estado, cabeceras or {}, tipo
        self.crudo = crudo if crudo is not None else (b"" if cuerpo is None else json.dumps(cuerpo).encode("utf-8"))


def json_(estado: int, cuerpo: Any, cabeceras: Optional[dict] = None) -> Respuesta:
    return Respuesta(estado, cuerpo, cabeceras)


def problema(estado: int, code: str, extra: Optional[dict] = None, cabeceras: Optional[dict] = None) -> Respuesta:
    cuerpo = {"type": f"https://platform.trevol.si/docs/errores#{code}", "title": "Título", "status": estado, "code": code,
              "retryable": False, "detail": f"Detalle de {code}", "request_id": "req_" + "c3" * 12, **(extra or {})}
    return Respuesta(estado, cuerpo, cabeceras, tipo="application/problem+json")


CORTAR = object()          # el servidor cierra la conexión sin responder (un fallo de red)


class Servidor:
    def __init__(self) -> None:
        self.respuestas: list[Any] = []
        self.peticiones: list[dict] = []
        servidor = self

        class Manejador(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def log_message(self, *a: Any) -> None:
                pass

            def _atender(self) -> None:
                largo = int(self.headers.get("content-length") or 0)
                cuerpo = self.rfile.read(largo) if largo else b""
                peticion = {"metodo": self.command, "ruta": self.path, "cabeceras": {k.lower(): v for k, v in self.headers.items()},
                            "cuerpo": cuerpo.decode("utf-8", "replace")}
                servidor.peticiones.append(peticion)
                i = min(len(servidor.peticiones) - 1, len(servidor.respuestas) - 1)
                r = servidor.respuestas[i]
                r = r(peticion) if callable(r) else r          # una función recibe la petición y contesta según la ruta
                if r is CORTAR:
                    self.close_connection = True
                    self.connection.close()
                    return
                self.send_response(r.estado)
                self.send_header("Content-Type", r.tipo)
                self.send_header("Content-Length", str(len(r.crudo)))
                for k, v in r.cabeceras.items():
                    self.send_header(k, v)
                self.end_headers()
                self.wfile.write(r.crudo)

            do_GET = do_POST = do_PUT = do_PATCH = do_DELETE = _atender

        self._http = ThreadingHTTPServer(("127.0.0.1", 0), Manejador)
        self._http.daemon_threads = True
        self.url = f"http://127.0.0.1:{self._http.server_address[1]}/v1"
        threading.Thread(target=self._http.serve_forever, daemon=True).start()

    def cerrar(self) -> None:
        self._http.shutdown()
        self._http.server_close()

    def vaciar(self, *respuestas: Any) -> "Servidor":
        self.respuestas, self.peticiones = list(respuestas), []
        return self


@pytest.fixture()
def servidor():
    s = Servidor()
    yield s
    s.cerrar()


class Banco:
    """Un cliente contra el servidor falso, con las esperas anotadas (no se duerme) y el azar en 1 (factor 1,0)."""

    def __init__(self, servidor: Servidor, *respuestas: Any, llave: str = LLAVE_TEST, **opciones: Any) -> None:
        self.servidor = servidor.vaciar(*respuestas)
        self.esperas: list[float] = []
        self._n = 0

        def uuid() -> str:
            self._n += 1
            return f"00000000-0000-4000-8000-{self._n:012d}"

        self.trevol = Trevol(llave, base_url=servidor.url, _internos={"sleep": self.esperas.append, "random": lambda: 1.0, "uuid": uuid},
                             **opciones)

    @property
    def peticiones(self) -> list[dict]:
        return self.servidor.peticiones


@pytest.fixture()
def banco(servidor):
    return lambda *r, **kw: Banco(servidor, *r, **kw)
