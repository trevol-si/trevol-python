# Generado por sdks/herramientas/fragmentos.mjs: el fragmento de la documentación, apuntando a Prism. No editar.
import os
from trevol import Trevol

trevol = Trevol(base_url=os.environ["TREVOL_PRISM_URL"], max_retries=0)  # lee TREVOL_API_KEY

resultado = trevol.balance.create_balance_top_up(
    top_up_input={"amount_cop": 50000},
    # idempotency_key="VENTA-2026-000123",  # opcional: si falta, el SDK pone una y la repite en los reintentos
)
print(resultado)
