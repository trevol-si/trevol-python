import pytest

from conftest import LLAVE_LIVE, LLAVE_TEST
from trevol import ConfigurationError, Trevol


def test_tvl_test_es_test_y_tvl_live_es_live():
    assert Trevol(LLAVE_TEST).environment == "test"
    assert Trevol(LLAVE_LIVE).environment == "live"


def test_lee_trevol_api_key_si_no_se_pasa(monkeypatch):
    monkeypatch.setenv("TREVOL_API_KEY", LLAVE_LIVE)
    assert Trevol().environment == "live"


def test_sin_llave_y_sin_variable_es_error_de_configuracion(monkeypatch):
    monkeypatch.setenv("TREVOL_API_KEY", "")
    with pytest.raises(ConfigurationError):
        Trevol()
    monkeypatch.delenv("TREVOL_API_KEY")
    with pytest.raises(ConfigurationError):
        Trevol()


@pytest.mark.parametrize("mala", ["tvl_test_abc", "tvl_prod_" + "a1" * 32, "sk_live_" + "a1" * 32, "tvl_test_" + "A1" * 32,
                                  "tvl_test_" + "a1" * 33, "   ", "tvl_test_" + "zz" * 32, 12345])
def test_mal_formada_es_configurationerror_sin_red_y_sin_la_llave_en_el_mensaje(mala):
    with pytest.raises(ConfigurationError) as info:
        Trevol(mala)
    if isinstance(mala, str) and mala.strip():
        assert mala.strip() not in str(info.value)


def test_environment_que_no_coincide_es_configurationerror_antes_de_llamar():
    with pytest.raises(ConfigurationError, match="live"):
        Trevol(LLAVE_TEST, environment="live")
    with pytest.raises(ConfigurationError):
        Trevol(LLAVE_LIVE, environment="test")
    assert Trevol(LLAVE_TEST, environment="test").environment == "test"
