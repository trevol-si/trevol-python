import re

from conftest import DOCUMENTO, LLAVE_LIVE, LLAVE_TEST, Respuesta, json_
from trevol import API_VERSION, VERSION


def test_authorization_trevol_version_fija_user_agent_y_ninguna_x_trevol(banco):
    b = banco(json_(200, DOCUMENTO))
    b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    c = b.peticiones[0]["cabeceras"]
    assert c["authorization"] == f"Bearer {LLAVE_TEST}"
    assert c["trevol-version"] == API_VERSION == "2026-10-22"
    assert re.fullmatch(rf"trevol-python/{re.escape(VERSION)} \(python \d+\.\d+\.\d+; \+https://platform\.trevol\.si/docs\)", c["user-agent"])
    assert c["accept"] == "application/json, application/problem+json"
    assert not [k for k in c if k.startswith("x-trevol-")] and not {"trevol-empresa", "trevol-entorno", "trevol-escenario"} & set(c)


def test_api_version_es_configurable_y_viaja_en_cada_peticion(banco):
    b = banco(json_(200, DOCUMENTO), api_version="2026-10-21")
    b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    assert [p["cabeceras"]["trevol-version"] for p in b.peticiones] == ["2026-10-21", "2026-10-21"]


def test_el_accept_de_una_descarga_es_el_del_archivo_y_los_bytes_llegan_intactos(banco):
    binario = bytes([37, 80, 68, 70, 0, 255, 1, 2])
    b = banco(Respuesta(200, crudo=binario, tipo="application/pdf"))
    pdf = b.trevol.invoices.download_invoice_pdf(id=DOCUMENTO["id"])
    assert b.peticiones[0]["cabeceras"]["accept"] == "application/pdf, application/problem+json"
    assert bytes(pdf) == binario and isinstance(pdf, (bytes, bytearray))
    assert b.peticiones[0]["ruta"] == f"/v1/invoices/{DOCUMENTO['id']}/pdf"


def test_la_llave_live_se_usa_tal_cual(banco):
    b = banco(json_(200, DOCUMENTO), llave=LLAVE_LIVE)
    b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"])
    assert b.peticiones[0]["cabeceras"]["authorization"] == f"Bearer {LLAVE_LIVE}" and b.trevol.environment == "live"


def test_una_cabecera_prefer_de_la_persona_pasa(banco):
    b = banco(json_(200, DOCUMENTO))
    b.trevol.invoices.retrieve_invoice(id=DOCUMENTO["id"], _headers={"Prefer": "code=404"})
    assert b.peticiones[0]["cabeceras"]["prefer"] == "code=404"


def test_urllib3_no_reintenta_por_su_cuenta(banco):
    """C14: `Configuration.retries = 0`, el SDK es el único que reintenta (si no, 3 intentos del SDK × 4 de urllib3)."""
    b = banco(json_(200, DOCUMENTO))
    assert b.trevol._cliente.configuration.retries == 0
