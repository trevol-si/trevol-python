# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

resultado = trevol.equivalent_document_adjustments.preview_equivalent_document_adjustment(
    equivalent_document_adjustment_input={
        "external_id": "TIQ-1-DEV",
        "note_type": "credit",
        "concept": "1",
        "equivalent_document": {"id": "pos_3f0c1a2b3f0c1a2b3f0c1a2b3f0c1a2b"},
        "items": [
            {
                "description": "Devolución gaseosa",
                "unit": "94",
                "quantity": "1",
                "unit_price": "3000",
                "taxes": [{"code": "01", "rate": "19"}],
            },
        ],
    },
)
print(resultado)
