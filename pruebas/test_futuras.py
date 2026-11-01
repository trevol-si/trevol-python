import hashlib
import hmac
import json
from datetime import datetime, timezone

import pytest

import standardwebhooks.webhooks as sw
import trevol
from conftest import DOCUMENTO, Respuesta, datos
from trevol import TrevolError, Webhook

CASOS = datos("respuestas-futuras.json")["casos"]


@pytest.mark.parametrize("caso", [c for c in CASOS if "operacion" in c], ids=lambda c: c["nombre"])
def test_respuestas_del_futuro_no_rompen(banco, caso):
    tipo = "application/problem+json" if caso["estado"] >= 400 else "application/json"
    b = banco(Respuesta(caso["estado"], caso["cuerpo"], caso.get("cabeceras"), tipo=tipo), max_retries=0)
    llamar = (lambda: b.trevol.invoices.list_invoices()) if caso["operacion"] == "listInvoices" else (lambda: b.trevol.invoices.retrieve_invoice(id="inv_x"))
    e = caso["esperado"]
    if caso["estado"] < 400:
        r = llamar()
        if "cantidad" in e:
            assert len(r.data) == e["cantidad"] and r.has_more is e["has_more"]
        else:
            assert r.id == e["id"] and r.status == e["status"]
    else:
        with pytest.raises(TrevolError) as info:
            llamar()
        x = info.value
        assert type(x).__name__ == e["clase"] and x.code == e["code"] and x.status == e["status"]
        if "requestId" in e:
            assert x.request_id == e["requestId"]


@pytest.mark.parametrize("caso", [c for c in CASOS if "evento" in c], ids=lambda c: c["nombre"])
def test_eventos_del_futuro(monkeypatch, caso):
    clave = b"0123456789abcdef0123456789abcdef"
    import base64
    secreto = "whsec_" + base64.b64encode(clave).decode()
    ts = 1793491200
    cuerpo = json.dumps(caso["evento"])
    firma = "v1," + base64.b64encode(hmac.new(clave, f"{caso['evento']['id']}.{ts}.{cuerpo}".encode(), hashlib.sha256).digest()).decode()

    class Falso(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.fromtimestamp(ts, tz=tz or timezone.utc)

    monkeypatch.setattr(sw, "datetime", Falso)
    wh = Webhook(secreto)
    e = wh.verify(cuerpo, {"webhook-id": caso["evento"]["id"], "webhook-timestamp": str(ts), "webhook-signature": firma})
    assert str(e.type) == caso["esperado"]["type"]
    assert (wh.event_data(e) is not None) is caso["esperado"]["tieneModelo"]
    assert e.data == caso["evento"]["data"]
