import pytest

from conftest import CORTAR, DOCUMENTO, ENTRADA_FACTURA, json_, problema
from trevol import (APIConnectionError, ConflictError, DianUnavailableError, RateLimitError, ValidationError)

NUEVO_ENDPOINT = {"url": "https://tu-servidor.co/h", "events": ["*"]}


def test_reintenta_un_503_dian_unavailable_y_devuelve_el_201(banco):
    b = banco(problema(503, "dian_unavailable", {"retryable": True}), json_(201, DOCUMENTO))
    doc = b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA)
    assert doc.id == DOCUMENTO["id"]
    assert len(b.peticiones) == 2 and b.esperas == [0.5]


def test_un_202_processing_es_un_resultado_no_se_reintenta_y_no_es_error(banco):
    b = banco(json_(202, {**DOCUMENTO, "status": "processing"}, {"Retry-After": "30", "Location": "/v1/invoices/x"}))
    doc = b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA)
    assert doc.status == "processing" and len(b.peticiones) == 1


def test_respeta_retry_after_en_un_409_request_in_progress(banco):
    b = banco(problema(409, "request_in_progress", {"retryable": True}, {"Retry-After": "30"}), json_(201, DOCUMENTO))
    b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA)
    assert b.esperas == [30]


def test_un_409_invalid_state_es_final(banco):
    b = banco(problema(409, "invalid_state"))
    with pytest.raises(ConflictError):
        b.trevol.invoices.send_invoice(id="inv_x")
    assert len(b.peticiones) == 1


def test_un_retry_after_mayor_que_el_tope_no_espera_y_lanza_con_retry_after(banco):
    b = banco(problema(429, "rate_limited", {"retryable": True}, {"Retry-After": "120"}))
    with pytest.raises(RateLimitError) as e:
        b.trevol.invoices.list_invoices()
    assert e.value.retry_after == 120 and len(b.peticiones) == 1 and b.esperas == []


def test_agota_los_reintentos_y_lanza_el_error_de_la_ultima_respuesta(banco):
    b = banco(problema(503, "dian_unavailable", {"retryable": True}))
    with pytest.raises(DianUnavailableError):
        b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA)
    assert len(b.peticiones) == 3 and b.esperas == [0.5, 1]


def test_max_retries_0_los_apaga(banco):
    b = banco(problema(503, "dian_unavailable", {"retryable": True}), max_retries=0)
    with pytest.raises(DianUnavailableError):
        b.trevol.invoices.list_invoices()
    assert len(b.peticiones) == 1


def test_un_fallo_de_red_en_post_invoices_con_clave_se_reintenta_y_agotado_es_apiconnectionerror_con_la_clave(banco):
    b = banco(CORTAR)
    with pytest.raises(APIConnectionError) as e:
        b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA)
    assert e.value.idempotency_key == "00000000-0000-4000-8000-000000000001"
    assert len(b.peticiones) == 3
    assert "tvl_" not in str(e.value)


def test_un_fallo_de_red_en_post_webhook_endpoints_sin_clave_no_se_reintenta(banco):
    b = banco(CORTAR)
    with pytest.raises(APIConnectionError):
        b.trevol.webhook_endpoints.create_webhook_endpoint(webhook_endpoint_input=NUEVO_ENDPOINT)
    assert len(b.peticiones) == 1


def test_un_fallo_de_red_en_un_get_se_reintenta_y_se_recupera(banco):
    b = banco(CORTAR, json_(200, DOCUMENTO))
    assert b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"]).id == DOCUMENTO["id"]
    assert len(b.peticiones) == 2


def test_un_429_en_solo_429_se_reintenta_y_un_503_no(banco):
    a = banco(problema(429, "rate_limited", {"retryable": True}, {"Retry-After": "2"}), json_(201, {"id": "we_x"}))
    a.trevol.webhook_endpoints.create_webhook_endpoint(webhook_endpoint_input=NUEVO_ENDPOINT)
    assert len(a.peticiones) == 2 and a.esperas == [2]
    b = banco(problema(503, "dian_unavailable", {"retryable": True}))
    with pytest.raises(DianUnavailableError):
        b.trevol.webhook_endpoints.create_webhook_endpoint(webhook_endpoint_input=NUEVO_ENDPOINT)
    assert len(b.peticiones) == 1


def test_un_422_no_se_reintenta(banco):
    b = banco(problema(422, "validation_error"))
    with pytest.raises(ValidationError):
        b.trevol.invoices.create_invoice(invoice_input=ENTRADA_FACTURA)
    assert len(b.peticiones) == 1
