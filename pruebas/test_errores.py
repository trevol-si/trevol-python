import pickle
import pytest

import trevol
from conftest import DOCUMENTO, LLAVE_TEST, Respuesta, datos, json_, problema
from trevol import TrevolError

ERRORES = datos("errores.json")
TODOS = [(clase, code) for clase, codes in ERRORES["clases"].items() for code in codes]
ESTADO = {"AuthenticationError": 401, "PermissionDeniedError": 403, "NotFoundError": 404, "InvalidRequestError": 400,
          "IdempotencyError": 409, "ValidationError": 422, "ConflictError": 409, "PreconditionError": 422, "DianRejectedError": 422,
          "BalanceError": 402, "RateLimitError": 429, "DianUnavailableError": 503, "InternalServerError": 500}


def test_cubre_los_30_code():
    assert len(TODOS) == 30


@pytest.mark.parametrize("clase,code", TODOS, ids=[c for _, c in TODOS])
def test_cada_code_va_a_su_clase_a_traves_de_un_metodo_generado(banco, clase, code):
    b = banco(problema(ESTADO[clase], code, {"retryable": False}), max_retries=0)
    with pytest.raises(getattr(trevol, clase)) as info:
        b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    e = info.value
    assert isinstance(e, TrevolError) and isinstance(e, Exception)
    assert type(e).__name__ == clase and e.code == code and e.status == ESTADO[clase]
    assert e.request_id == "req_" + "c3" * 12
    assert e.type == f"https://platform.trevol.si/docs/errores#{code}"
    assert e.problem["code"] == code


def test_el_error_no_se_envuelve_en_apiexception_del_codigo_generado(banco):
    from trevol._generado.exceptions import ApiException
    b = banco(problema(404, "not_found"))
    with pytest.raises(trevol.NotFoundError) as info:
        b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    assert not isinstance(info.value, ApiException)


def test_un_code_desconocido_es_la_clase_base_y_no_rompe(banco):
    b = banco(problema(422, "code_del_futuro"))
    with pytest.raises(TrevolError) as info:
        b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    assert type(info.value) is TrevolError and info.value.code == "code_del_futuro"


@pytest.mark.parametrize("estado,clase", [(502, "InternalServerError"), (404, "NotFoundError"), (409, "ConflictError"), (401, "AuthenticationError")])
def test_una_respuesta_que_no_es_json_da_la_clase_por_estado_con_code_none_y_el_cuerpo_recortado(banco, estado, clase):
    html = b"<html>" + b"x" * 5000 + b"</html>"
    b = banco(Respuesta(estado, crudo=html, tipo="text/html"), max_retries=0)
    with pytest.raises(getattr(trevol, clase)) as info:
        b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    assert info.value.code is None and len(info.value.detail) == 2048


def test_toma_el_request_id_de_la_cabecera_cuando_el_cuerpo_no_lo_trae(banco):
    cuerpo = {"type": "x", "title": "t", "status": 404, "code": "not_found", "retryable": False}
    b = banco(Respuesta(404, cuerpo, {"Request-Id": "req_" + "d4" * 12}, tipo="application/problem+json"))
    with pytest.raises(trevol.NotFoundError) as info:
        b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    assert info.value.request_id == "req_" + "d4" * 12


def test_validationerror_trae_errors_con_field_pointer_y_message(banco):
    b = banco(problema(422, "validation_error", {"errors": [{"field": "items", "pointer": "/items", "message": "Falta"}]}))
    with pytest.raises(trevol.ValidationError) as info:
        b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    x = info.value.errors[0]
    assert (x.field, x.pointer, x.message) == ("items", "/items", "Falta")


def test_los_campos_extra_quedan_en_problem(banco):
    b = banco(problema(409, "external_id_in_use", {"existing_id": "inv_x"}))
    with pytest.raises(trevol.ConflictError) as info:
        b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    assert info.value.problem["existing_id"] == "inv_x"


def test_la_llave_no_aparece_en_str_repr_ni_traceback_de_ningun_error(banco):
    import traceback
    b = banco(problema(401, "invalid_api_key"))
    with pytest.raises(trevol.AuthenticationError) as info:
        b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    e = info.value
    textos = [str(e), repr(e), "".join(traceback.format_exception(e)), repr(b.trevol), repr(b.trevol._cliente._o), repr(e.problem)]
    for t in textos:
        assert LLAVE_TEST not in t and "a1" * 32 not in t
    assert "invalid_api_key" in str(e) and "HTTP 401" in str(e) and "req_" in str(e)
