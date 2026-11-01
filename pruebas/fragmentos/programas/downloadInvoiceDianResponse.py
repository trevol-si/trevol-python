# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

archivo: bytes = trevol.invoices.download_invoice_dian_response(
    id="inv_3f0c1a2b3f0c1a2b3f0c1a2b3f0c1a2b",
)
# archivo son los bytes del XML
