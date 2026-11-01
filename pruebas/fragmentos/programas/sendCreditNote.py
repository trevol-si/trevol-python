# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

resultado = trevol.credit_notes.send_credit_note(
    id="cn_3f0c1a2b3f0c1a2b3f0c1a2b3f0c1a2b",
)
print(resultado)
