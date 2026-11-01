import pytest

from conftest import datos
from trevol import Resultado, decidir, espera_propia

CASOS = datos("transporte.json")["casos"]


def test_hay_casos():
    assert len(CASOS) >= 50


@pytest.mark.parametrize("caso", CASOS, ids=[c["nombre"] for c in CASOS])
def test_decidir_con_pruebas_datos_transporte_json(caso):
    r = caso["resultado"]
    resultado = Resultado(r["tipo"], r.get("estado"), r.get("code"), r.get("retryable"), r.get("retryAfter"))
    d = decidir(intento=caso["intento"], reintento=caso["reintento"], max_reintentos=caso["maxReintentos"],
                max_retry_after=caso["maxRetryAfter"], azar=caso["azar"], resultado=resultado)
    esperado = caso["esperado"]
    assert d.reintentar is esperado["reintentar"]
    if "espera" in esperado:
        assert d.espera == pytest.approx(esperado["espera"])
    if "motivo" in esperado:
        assert d.motivo == esperado["motivo"]
    if not esperado["reintentar"]:
        assert d.espera is None


def test_la_espera_propia_crece_con_tope_de_8_y_un_factor_entre_075_y_1():
    assert [espera_propia(n, 1) for n in (1, 2, 3, 4, 5, 6, 9)] == [0.5, 1, 2, 4, 8, 8, 8]
    assert espera_propia(1, 0) == 0.375
    assert espera_propia(4, 0) == 3
