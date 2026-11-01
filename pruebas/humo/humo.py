"""Prueba de humo REAL en habilitación (docs/api/43 §2.10.4). NO es parte de la suite: la corre una persona, con una llave de PRUEBAS.

    TREVOL_API_KEY=tvl_test_… python pruebas/humo/humo.py

Solo lecturas y un preview (el SDK de Python NO emite; el de Node lo hace con TREVOL_HUMO_EMITIR=1). Se NIEGA a correr si la llave no es
tvl_test_. `TREVOL_BASE_URL` (opcional) apunta a otro servidor, p. ej. un Prism local.
"""

import base64
import hashlib
import hmac
import itertools
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

from trevol import NotFoundError, Trevol, Webhook

llave = os.environ.get("TREVOL_API_KEY", "")
if not re.fullmatch(r"tvl_test_[0-9a-f]{64}", llave):
    print("humo: me niego a correr si TREVOL_API_KEY no es una llave de PRUEBAS (tvl_test_…). Nunca se prueba con tvl_live_.", file=sys.stderr)
    sys.exit(2)

trevol = Trevol(llave, environment="test", **({"base_url": os.environ["TREVOL_BASE_URL"]} if os.environ.get("TREVOL_BASE_URL") else {}))
pasos = []


def paso(nombre):
    def decorador(f):
        try:
            detalle = f()
            pasos.append((nombre, True))
            print(f"ok   {nombre}{' — ' + str(detalle) if detalle else ''}")
        except Exception as e:  # noqa: BLE001 - es una prueba de humo: cuenta cualquier fallo
            pasos.append((nombre, False))
            print(f"FALLA {nombre} — {e!r}")
        return f

    return decorador


@paso("get_health")
def _():
    trevol.general.get_health()


@paso("retrieve_company")
def _():
    c = trevol.general.retrieve_company()
    assert c.environment == "test", f"la empresa dice environment={c.environment}"
    return f"{c.name} ({c.nit})"


@paso("preview_invoice")
def _():
    p = trevol.invoices.preview_invoice(invoice_input={
        "external_id": "HUMO-PREVIEW", "customer": {"final_consumer": True},
        "items": [{"description": "Prueba de humo del SDK de Trevol", "quantity": "1", "unit_price": "1000", "taxes": [{"code": "01", "rate": "19"}]}],
        "payment": {"form": "cash", "methods": [{"code": "10"}]}})
    return f"total {(p.totals or {}).get('total')}"


@paso("list_invoices + paginate (3)")
def _():
    trevol.invoices.list_invoices(limit=3)
    n = len(list(itertools.islice(trevol.paginate(lambda c: trevol.invoices.list_invoices(limit=3, starting_after=c)), 3)))
    return f"{n} facturas"


@paso("retrieve_invoice inexistente → NotFoundError con request_id")
def _():
    try:
        trevol.invoices.retrieve_invoice(id="inv_" + "0" * 32)
    except NotFoundError as e:
        assert e.request_id and e.request_id.startswith("req_")
        return e.request_id
    raise AssertionError("no lanzó NotFoundError")


@paso("Webhook.verify (firmado ahora, con un secreto local)")
def _():
    clave = b"trevol-humo-secreto-de-32-bytes!"
    msg_id = "evt_" + "1" * 32
    cuerpo = json.dumps({"id": msg_id, "object": "event", "type": "webhook.test", "timestamp": datetime.now(timezone.utc).isoformat(),
                         "environment": "test", "api_version": "2026-10-22", "data": {}})
    ts = int(time.time())
    firma = "v1," + base64.b64encode(hmac.new(clave, f"{msg_id}.{ts}.{cuerpo}".encode(), hashlib.sha256).digest()).decode()
    e = Webhook("whsec_" + base64.b64encode(clave).decode()).verify(
        cuerpo, {"webhook-id": msg_id, "webhook-timestamp": str(ts), "webhook-signature": firma})
    return e.type


fallas = [n for n, ok in pasos if not ok]
print(f"\n{len(pasos) - len(fallas)}/{len(pasos)} pasos bien")
sys.exit(1 if fallas else 0)
