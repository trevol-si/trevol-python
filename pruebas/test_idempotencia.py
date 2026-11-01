import pytest

from conftest import DOCUMENTO, ENTRADA_FACTURA, json_, problema
from trevol import ConfigurationError, DianRejectedError


def test_genera_una_clave_y_la_repite_en_los_tres_intentos(banco):
    b = banco(problema(503, "dian_unavailable", {"retryable": True}), problema(503, "dian_unavailable", {"retryable": True}), json_(201, DOCUMENTO))
    b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA)
    claves = [p["cabeceras"].get("idempotency-key") for p in b.peticiones]
    assert len(claves) == 3 and len(set(claves)) == 1 and claves[0] == "00000000-0000-4000-8000-000000000001"
    assert len({p["cuerpo"] for p in b.peticiones}) == 1                   # el cuerpo viaja entero en cada intento
    assert '"external_id":"VENTA-2026-000123"' in b.peticiones[2]["cuerpo"].replace(" ", "")


def test_respeta_la_clave_de_la_persona(banco):
    b = banco(json_(201, DOCUMENTO))
    b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA, idempotency_key="VENTA-2026-000123")
    assert b.peticiones[0]["cabeceras"]["idempotency-key"] == "VENTA-2026-000123"


@pytest.mark.parametrize("mala", ["con espacio", "x" * 256, "tilde-é", ""])
def test_una_clave_mala_se_rechaza_localmente_sin_red(banco, mala):
    b = banco(json_(201, DOCUMENTO))
    with pytest.raises(ConfigurationError):
        b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA, idempotency_key=mala)
    assert b.peticiones == []


def test_la_lleva_el_error_para_reintentar_mas_tarde_con_la_misma(banco):
    b = banco(problema(422, "dian_rejected"))
    with pytest.raises(DianRejectedError) as e:
        b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA)
    assert e.value.idempotency_key == "00000000-0000-4000-8000-000000000001"


def test_crear_corregir_y_la_recarga_la_llevan_el_resto_no(banco):
    def segun_la_ruta(p):          # cada operación contesta con su éxito: el generado elige el modelo por el estado exacto
        if p["ruta"].endswith("/top_ups"):
            return json_(201, {"object": "top_up", "reference": "TRV-REC-1", "amount_cop": 50000, "status": "prepared"})
        if p["ruta"].endswith("/webhook_endpoints"):
            return json_(201, {"id": "we_" + "a" * 32, "object": "webhook_endpoint", "environment": "test"})
        if p["metodo"] == "POST" and p["ruta"].endswith("/invoices"):
            return json_(201, DOCUMENTO)
        return json_(200, DOCUMENTO)

    b = banco(segun_la_ruta)
    t = b.trevol
    t.invoices.create_invoice(invoice_input=ENTRADA_FACTURA)
    t.invoices.correct_invoice(id=DOCUMENTO["id"], invoice_input=ENTRADA_FACTURA)
    t.balance.create_balance_top_up(top_up_input={"amount_cop": 50000})
    t.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    t.invoices.send_invoice(id=DOCUMENTO["id"])
    t.webhook_endpoints.create_webhook_endpoint(webhook_endpoint_input={"url": "https://tu-servidor.co/h", "events": ["*"]})
    t.invoices.preview_invoice(invoice_input=ENTRADA_FACTURA)
    vistas = [f"{p['metodo']} {p['ruta'].split('?')[0]} {'idempotency-key' in p['cabeceras']}" for p in b.peticiones]
    assert vistas == [
        "POST /v1/invoices True", f"PUT /v1/invoices/{DOCUMENTO['id']} True", "POST /v1/balance/top_ups True",
        f"GET /v1/invoices/{DOCUMENTO['id']} False", f"POST /v1/invoices/{DOCUMENTO['id']}/send False",
        "POST /v1/webhook_endpoints False", "POST /v1/invoices/preview False",
    ]
