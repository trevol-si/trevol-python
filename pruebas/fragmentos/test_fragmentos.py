"""Los fragmentos de la documentación, como programas (docs/api/43 §2.9): se COMPILAN y se CORREN contra Prism. Un fragmento que no compila,
o que Prism rechaza porque el cuerpo no cumple la especificación, rompe esta suite."""

import json
import os
import py_compile
import runpy
from pathlib import Path

import pytest

AQUI = Path(__file__).parent
DATOS = json.loads((AQUI.parent / "datos" / "fragmentos.json").read_text(encoding="utf-8"))
OPERACIONES = sorted(DATOS["fragmentos"])
PROGRAMAS = AQUI / "programas"


def test_la_estructura():
    assert len(OPERACIONES) == 109 and DATOS["lenguajes"] == ["curl", "node", "python"]
    assert sorted(p.stem for p in PROGRAMAS.glob("*.py")) == OPERACIONES
    for op in OPERACIONES:
        assert "Trevol()" in DATOS["fragmentos"][op]["python"] and "TREVOL_API_KEY" in DATOS["fragmentos"][op]["python"]


@pytest.mark.parametrize("op", OPERACIONES)
def test_el_fragmento_compila(op, tmp_path):
    py_compile.compile(str(PROGRAMAS / f"{op}.py"), cfile=str(tmp_path / "x.pyc"), doraise=True)


@pytest.mark.skipif(not os.environ.get("TREVOL_PRISM_URL"), reason="necesita Prism: sdks/herramientas/prism.sh -- pytest pruebas/fragmentos")
@pytest.mark.parametrize("op", OPERACIONES)
def test_el_fragmento_corre_contra_prism(op, capsys):
    runpy.run_path(str(PROGRAMAS / f"{op}.py"), run_name="__main__")
