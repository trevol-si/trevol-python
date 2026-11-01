# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

resultado = trevol.support_documents.preview_support_document(
    support_document_input={
        "external_id": "OC-991",
        "seller": {
            "resident": True,
            "person_type": "natural",
            "document_type": "31",
            "document_number": "1020304050",
            "name": "PEREZ GOMEZ ANA MARIA",
            "address": "Vereda El Silencio, finca La Esperanza",
            "municipality_code": "25053",
            "postal_code": "252007",
            "tax_responsibilities": ["R-99-PN"],
        },
        "items": [
            {
                "description": "Leche cruda",
                "unit": "LTR",
                "quantity": "120",
                "unit_price": "1800",
            },
        ],
        "payment": {"form": "cash", "methods": [{"code": "10"}]},
        "notes": ["Compra de la semana 42 de octubre"],
    },
)
print(resultado)
