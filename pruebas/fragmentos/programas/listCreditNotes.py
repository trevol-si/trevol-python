# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

for item in trevol.paginate(lambda cursor: trevol.credit_notes.list_credit_notes(limit=100, starting_after=cursor)):
    print(item.id)
