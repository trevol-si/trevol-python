# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

for item in trevol.paginate(lambda cursor: trevol.equivalent_documents.list_equivalent_documents(limit=100, starting_after=cursor)):
    print(item.id)
