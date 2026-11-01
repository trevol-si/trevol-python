from types import SimpleNamespace as NS

from conftest import json_
from trevol import paginar


def doc(n):
    return NS(id=f"inv_{n}")


def test_recorre_tres_paginas_falsas_con_next_cursor_y_se_detiene():
    pedidos = []
    paginas = [NS(data=[doc(1), doc(2)], has_more=True, next_cursor="inv_2"), NS(data=[doc(3), doc(4)], has_more=True, next_cursor="inv_4"),
               NS(data=[doc(5)], has_more=False, next_cursor=None)]

    def pagina(c):
        pedidos.append(c)
        return paginas[len(pedidos) - 1]

    assert [x.id for x in paginar(pagina)] == ["inv_1", "inv_2", "inv_3", "inv_4", "inv_5"]
    assert pedidos == [None, "inv_2", "inv_4"]


def test_si_has_more_viene_sin_next_cursor_usa_el_id_del_ultimo():
    pedidos = []
    paginas = [NS(data=[doc(1), doc(2)], has_more=True, next_cursor=None), NS(data=[doc(3)], has_more=False, next_cursor=None)]

    def pagina(c):
        pedidos.append(c)
        return paginas[len(pedidos) - 1]

    assert len(list(paginar(pagina))) == 3 and pedidos == [None, "inv_2"]


def test_es_perezosa():
    llamadas = []

    def pagina(c):
        llamadas.append(c)
        return NS(data=[doc(1), doc(2)], has_more=True, next_cursor="inv_2")

    it = paginar(pagina)
    next(it)
    assert len(llamadas) == 1
    it.close()
    assert len(llamadas) == 1


def test_un_cursor_que_no_avanza_o_una_pagina_vacia_no_dejan_el_bucle_girando():
    n = []

    def pagina(c):
        n.append(c)
        return NS(data=[doc(1)], has_more=True, next_cursor="inv_1")

    assert len(list(paginar(pagina))) <= 3
    assert list(paginar(lambda c: NS(data=[], has_more=True, next_cursor="x"))) == []


def test_client_paginate_con_un_metodo_generado_y_el_servidor_falso(banco):
    b = banco(json_(200, {"object": "list", "data": [{"id": "inv_1"}, {"id": "inv_2"}], "has_more": True, "next_cursor": "inv_2"}),
              json_(200, {"object": "list", "data": [{"id": "inv_3"}], "has_more": False, "next_cursor": None}))
    t = b.trevol
    ids = [f.id for f in t.paginate(lambda cursor: t.invoices.list_invoices(limit=2, starting_after=cursor))]
    assert ids == ["inv_1", "inv_2", "inv_3"]
    assert "starting_after" not in b.peticiones[0]["ruta"]
    assert "starting_after=inv_2" in b.peticiones[1]["ruta"] and "limit=2" in b.peticiones[1]["ruta"]
