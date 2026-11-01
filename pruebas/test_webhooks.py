import sys
from datetime import datetime, timezone

import pytest

import standardwebhooks.webhooks as sw
from conftest import datos
from trevol import ConfigurationError, Webhook, WebhookVerificationError

VECTORES = datos("webhooks.json")
CASOS = VECTORES["casos"]
OK = next(c for c in CASOS if c["nombre"] == "valido")


@pytest.fixture()
def ahora(monkeypatch):
    """El reloj de la biblioteca (standardwebhooks usa `datetime.now`), en un instante fijo."""
    def fijar(segundos: int) -> None:
        class Falso(datetime):
            @classmethod
            def now(cls, tz=None):
                return datetime.fromtimestamp(segundos, tz=tz or timezone.utc)

        monkeypatch.setattr(sw, "datetime", Falso)

    return fijar


def test_la_tolerancia_es_de_5_minutos():
    assert VECTORES["tolerancia"] == 300


@pytest.mark.parametrize("caso", CASOS, ids=[c["nombre"] for c in CASOS])
def test_vectores_de_pruebas_datos_webhooks_json(caso, ahora):
    ahora(caso["ahora"])
    wh = Webhook(caso["secreto"])
    if caso["valido"]:
        e = wh.verify(caso["cuerpo"], caso["cabeceras"])
        assert e.id == caso["evento"]["id"] and str(e.type) == caso["evento"]["type"]
    else:
        with pytest.raises(WebhookVerificationError) as info:
            wh.verify(caso["cuerpo"], caso["cabeceras"])
        assert info.value.motivo == caso["motivo"]


def test_bytes_bytearray_y_memoryview(ahora):
    ahora(OK["ahora"])
    raw = OK["cuerpo"].encode("utf-8")
    for cuerpo in (raw, bytearray(raw), memoryview(raw)):
        assert Webhook(OK["secreto"]).verify(cuerpo, OK["cabeceras"]).type == "invoice.accepted"


def test_cabeceras_de_cualquier_caja_valores_en_lista_y_pares(ahora):
    ahora(OK["ahora"])
    wh = Webhook(OK["secreto"])
    c = OK["cabeceras"]
    assert wh.verify(OK["cuerpo"], {"Webhook-Id": c["webhook-id"], "WEBHOOK-TIMESTAMP": [c["webhook-timestamp"]], "webhook-signature": c["webhook-signature"]}).id
    assert wh.verify(OK["cuerpo"], list(c.items())).id                      # una lista de pares
    assert wh.verify(OK["cuerpo"], {"webhook-id": [c["webhook-id"], "evt_otro"], **{k: v for k, v in c.items() if k != "webhook-id"}}).id


def test_un_cuerpo_ya_parseado_se_rechaza_diciendo_como_leer_el_crudo(ahora):
    import json
    ahora(OK["ahora"])
    with pytest.raises(WebhookVerificationError, match="CRUDO") as info:
        Webhook(OK["secreto"]).verify(json.loads(OK["cuerpo"]), OK["cabeceras"])
    assert "get_data" in str(info.value) and info.value.motivo == "cuerpo"


def test_un_secreto_vacio_o_con_basura_es_configurationerror_y_no_se_filtra():
    for malo in ("", "   ", "whsec_"):
        with pytest.raises(ConfigurationError):
            Webhook(malo)
    with pytest.raises(ConfigurationError) as e:
        Webhook("whsec_@@@@@")
    assert "@@@" not in str(e.value)


def test_event_data_da_el_modelo_segun_el_type_y_un_type_nuevo_da_none(ahora):
    ahora(OK["ahora"])
    wh = Webhook(OK["secreto"])
    e = wh.verify(OK["cuerpo"], OK["cabeceras"])
    d = wh.event_data(e)
    assert type(d).__name__ == "DocumentEventData" and d.status == "accepted"
    e.type = "invoice.archived"
    assert wh.event_data(e) is None


def test_el_mensaje_de_un_rechazo_no_incluye_el_secreto(ahora):
    ahora(OK["ahora"])
    with pytest.raises(WebhookVerificationError) as e:
        Webhook(OK["secreto"]).verify(OK["cuerpo"] + " ", OK["cabeceras"])
    assert OK["secreto"][6:] not in str(e.value)
