# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

resultado = trevol.webhook_endpoints.create_webhook_endpoint(
    webhook_endpoint_input={
        "url": "https://tu-servidor.co/webhooks/trevol",
        "description": "Producción: facturación",
        "events": ["invoice.accepted", "invoice.rejected", "credit_note.accepted"],
    },
)
print(resultado)
