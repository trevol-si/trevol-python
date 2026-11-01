"""Contra Prism (servidor simulado desde docs/api/openapi.json, docs/api/43 §2.10.2): `sdks/herramientas/prism.sh -- pytest pruebas/prism`.

Prism valida cada petición contra la especificación PÚBLICA: si el SDK serializa mal un cuerpo, olvida una cabecera o la Idempotency-Key, responde
4xx y la prueba falla (el motivo viene en la cabecera `sl-violations`, que se le pega al error)."""

import contextlib
import json
import os
from pathlib import Path

import pytest

import trevol
from trevol import Trevol, TrevolError

URL = os.environ.get("TREVOL_PRISM_URL")
LLAVE = os.environ.get("TREVOL_API_KEY", "tvl_test_" + "a1" * 32)
pytestmark = pytest.mark.skipif(not URL, reason="necesita Prism: sdks/herramientas/prism.sh -- pytest pruebas/prism")

OPERACIONES = json.loads((Path(__file__).parent.parent / "datos" / "operaciones.json").read_text(encoding="utf-8"))


def ejemplo(op: str, nombre: str | None = None):
    o = next(x for x in OPERACIONES if x["operationId"] == op)
    return next(e for e in o["ejemplos"] if e["nombre"] == nombre)["valor"] if nombre else o["ejemplos"][0]["valor"]


@contextlib.contextmanager
def con_violaciones():
    try:
        yield
    except TrevolError as e:
        v = (e.headers or {}).get("sl-violations") or (e.headers or {}).get("Sl-Violations")
        if v:
            raise AssertionError(f"Prism rechazó la petición ({e.status}): {v}") from e
        raise


@pytest.fixture(scope="module")
def t():
    return Trevol(LLAVE, base_url=URL, max_retries=0)


def prefer(valor):
    return {"_headers": {"Prefer": valor, "Content-Type": "application/json"}}


def test_crea_una_factura_201_con_el_cuerpo_de_ejemplo(t):
    with con_violaciones():
        doc = t.invoices.create_invoice(invoice_input=ejemplo("createInvoice"))
    assert doc.object == "invoice"


def test_crea_una_nota_credito_y_calcula_un_preview(t):
    with con_violaciones():
        nc = t.credit_notes.create_credit_note(note_input=ejemplo("createCreditNote"))
        p = t.invoices.preview_invoice(invoice_input=ejemplo("previewInvoice"))
    assert nc is not None and p.object == "preview" and p.totals is not None


def test_corrige_una_factura_rechazada_con_put(t):
    with con_violaciones():
        assert t.invoices.correct_invoice(id="inv_" + "0" * 32, invoice_input=ejemplo("correctInvoice")) is not None


def test_lista_facturas_y_eventos_e_itera_con_paginate_con_tope_de_3(t):
    for pagina, campo in ((lambda c: t.invoices.list_invoices(limit=2, starting_after=c), "facturas"),
                          (lambda c: t.events.list_events(starting_after=c), "eventos")):
        vistos = []
        with con_violaciones():
            for x in t.paginate(pagina):
                vistos.append(x.id)
                if len(vistos) == 3:                      # Prism repite siempre la misma página con has_more=true (C8)
                    break
        assert vistos, campo


@pytest.mark.parametrize("operacion,mime", [("download_invoice_pdf", "application/pdf"), ("download_invoice_xml", "application/xml"),
                                            ("download_invoice_zip", "application/zip"), ("download_invoice_dian_response", "application/xml")])
def test_descarga_pdf_xml_zip_y_respuesta_dian_los_bytes_llegan(t, operacion, mime):
    with con_violaciones():
        r = getattr(t.invoices, operacion + "_with_http_info")(id="inv_" + "0" * 32)
    assert mime in {k.lower(): v for k, v in r.headers.items()}.get("content-type", "")
    assert isinstance(r.data, (bytes, bytearray))


def test_prefer_code_422_sobre_un_evento_radian_es_preconditionerror_tacit_acceptance_not_due(t):
    with pytest.raises(trevol.PreconditionError) as e:
        t.radian_events.create_radian_event(radian_event_input=ejemplo("createRadianEvent", "tacita"), **prefer("code=422, example=tacita"))
    assert e.value.code == "tacit_acceptance_not_due" and e.value.status == 422


def test_prefer_code_409_sobre_un_evento_radian_es_conflicterror(t):
    with pytest.raises(trevol.ConflictError) as e:
        t.radian_events.create_radian_event(radian_event_input=ejemplo("createRadianEvent", "acuse"), **prefer("code=409, example=duplicado"))
    assert e.value.status == 409 and e.value.problem["existing_id"].startswith("rev_")


def test_prefer_code_429_es_un_trevolerror_con_status_429_retryable_y_la_clave(t):
    with pytest.raises(TrevolError) as e:
        t.invoices.create_invoice(invoice_input=ejemplo("createInvoice"), **prefer("code=429"))
    assert e.value.status == 429 and e.value.retryable is True and e.value.idempotency_key


def test_crea_un_endpoint_de_webhooks_y_manda_la_prueba_202(t):
    with con_violaciones():
        ep = t.webhook_endpoints.create_webhook_endpoint(webhook_endpoint_input=ejemplo("createWebhookEndpoint"))
        entrega = t.webhook_endpoints.test_webhook_endpoint(id="we_" + "0" * 32)
    assert ep.object == "webhook_endpoint" and entrega is not None


def test_company_y_acquirer_devuelven_modelos_no_void(t):
    with con_violaciones():
        c = t.general.retrieve_company()
        a = t.general.retrieve_dian_acquirer(document_type="31", document_number="900373591")
    assert c.object == "company" and a.object == "acquirer"


def test_reintenta_contra_prism_con_la_misma_clave_y_agota_con_el_error_del_503():
    esperas = []
    cliente = Trevol(LLAVE, base_url=URL, max_retries=1, _internos={"sleep": esperas.append})
    with pytest.raises(TrevolError) as e:
        cliente.invoices.create_invoice(invoice_input=ejemplo("createInvoice"), idempotency_key="PRUEBA-PRISM-1", **prefer("code=503"))
    assert e.value.status == 503 and e.value.idempotency_key == "PRUEBA-PRISM-1" and len(esperas) == 1
