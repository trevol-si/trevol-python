# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

resultado = trevol.radian_events.retrieve_tacit_acceptance_by_cufe(
    cufe="abababababababababababababababababababababababababababababababababababababababababababababababab",
)
print(resultado)
