# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

archivo: bytes = trevol.equivalent_document_adjustments.download_equivalent_document_adjustment_xml(
    id="posa_3f0c1a2b3f0c1a2b3f0c1a2b3f0c1a2b",
)
# archivo son los bytes del XML
