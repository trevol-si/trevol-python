from conftest import LLAVE_TEST, datos
from trevol import Trevol
from trevol._generado.tablas import ETIQUETAS, OPERACIONES


def snake(s: str) -> str:
    import re
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", s).lower()


def test_la_tabla_generada_y_la_especificacion_tienen_las_mismas_etiquetas():
    assert list(ETIQUETAS) == datos("tags.json")


def test_cada_etiqueta_de_openapi_sdk_json_tiene_su_propiedad_en_el_cliente():
    t = Trevol(LLAVE_TEST)
    for etiqueta in datos("tags.json"):
        assert hasattr(t, snake(etiqueta)), etiqueta     # si la API suma un recurso, esto falla hasta agregarlo


def test_cada_operation_id_existe_como_metodo_en_su_recurso():
    t = Trevol(LLAVE_TEST)
    for o in OPERACIONES:
        assert callable(getattr(getattr(t, snake(o["recurso"])), snake(o["operationId"]))), o["operationId"]
