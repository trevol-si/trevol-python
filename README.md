# trevol

SDK de Python para la **API de Trevol**: facturación electrónica, documento soporte, documento equivalente, nómina electrónica y eventos
RADIAN ante la DIAN (Colombia). Documentación: <https://platform.trevol.si/docs>.

> **In English.** Python SDK for the Trevol API (Colombian e-invoicing, DIAN). Python ≥ 3.10, typed (pydantic v2) models generated from the
> OpenAPI spec (OpenAPI Generator), plus a thin hand-written layer: automatic `Idempotency-Key` (the same one on retries), retries with
> exponential backoff honouring `Retry-After`, typed errors by problem+json `code`, environment inferred from the key prefix (`tvl_test_` =
> DIAN test environment, `tvl_live_` = production), pinned `Trevol-Version`, Standard Webhooks signature verification, cursor pagination
> iterators and PDF/XML/ZIP downloads (as `bytes`). Docs are in Spanish like the API.

**Versión 0.1.0** — API `2026-10-22`. Licencia MIT.

## Instalación

```sh
pip install trevol
```

Necesita Python 3.10 o más nuevo. Dependencias: `urllib3`, `pydantic>=2`, `python-dateutil`, `typing-extensions` y
[`standardwebhooks`](https://pypi.org/project/standardwebhooks/).

## Uso

La llave de la API se crea en la consola de desarrolladores (<https://platform.trevol.si/llaves>) y se guarda en el entorno de tu **servidor**:
`TREVOL_API_KEY`. Una llave `tvl_test_…` llama a la habilitación de la DIAN; una `tvl_live_…`, a producción. El SDK deduce el entorno del
prefijo (`trevol.environment`).

```python
import os
from trevol import Trevol, TrevolError, ValidationError, Webhook

trevol = Trevol()  # lee TREVOL_API_KEY; tvl_test_… → trevol.environment == "test"

try:
    factura = trevol.invoices.create_invoice(
        invoice_input={
            "external_id": "VENTA-2026-000123",
            "customer": {"final_consumer": True},
            "items": [{"description": "Café especial 500 g", "quantity": "1", "unit_price": "32000", "taxes": [{"code": "01", "rate": "19"}]}],
            "payment": {"form": "cash", "methods": [{"code": "10"}]},
        },
        idempotency_key="VENTA-2026-000123",  # opcional: si falta, el SDK pone una y la repite en los reintentos
    )
    if factura.status == "processing":
        pass  # 202: la DIAN no contestó; Trevol lo termina y avisa por webhook. NO crees otro documento para la misma venta.
except ValidationError as e:
    for x in e.errors:
        print(x.pointer, x.message)
except TrevolError as e:
    print(e.code, e.request_id)

# Todas las páginas de un listado, perezosamente
for f in trevol.paginate(lambda cursor: trevol.invoices.list_invoices(limit=100, starting_after=cursor)):
    print(f.id, f.status)

# Los archivos llegan como bytes
pdf: bytes = trevol.invoices.download_invoice_pdf(id="inv_…")

# Un webhook: verifica sobre el CUERPO CRUDO
evento = Webhook(os.environ["TREVOL_WEBHOOK_SECRET"]).verify(request.get_data(), request.headers)
```

Los métodos son los `operationId` de la [especificación](https://platform.trevol.si/docs/api) en `snake_case` (`create_invoice`,
`list_invoices`, `retrieve_invoice`, `correct_invoice`, `send_invoice`, `download_invoice_pdf`…) y el cuerpo es el nombre del esquema en
`snake_case` (`invoice_input`). Puedes pasar un `dict` (como arriba) o el modelo (`InvoiceInput(...)`). Los campos se escriben **igual que en la
API** (`external_id`), y los importes y las fechas viajan como texto (`"32000.50"`, `"2026-10-31"`).

## Lo que conviene saber

### Idempotencia: manda `external_id` y tu propia clave

El SDK genera una `Idempotency-Key` por llamada y **la repite en todos los reintentos de esa llamada**. Pero si tu proceso muere y vuelves a
llamar, saldrá otra clave y, si no mandaste `external_id` (es opcional), podría duplicarse el documento. Por eso:

- manda siempre `external_id` (tu id de la venta), y
- pasa una `idempotency_key` derivada de tu venta (`idempotency_key="VENTA-2026-000123"`).

Ante un `ConflictError` con `code == "external_id_in_use"`, el documento ya existe: usa `error.problem["existing_id"]`. Todo error lleva la
`idempotency_key` que se usó (`error.idempotency_key`) para reintentar más tarde con la misma. Un `APIConnectionError` también.

### Respuestas 202 (`processing`, `sending`, `validating`, `contingency`)

No son errores ni se reintentan: se devuelven como el modelo de la respuesta. **No crees otro documento**: espera el webhook o consulta con
`retrieve_invoice`; repetir la misma llamada con la misma `Idempotency-Key` continúa el mismo documento. El PDF y el ZIP llegan después del
`201` (evento `invoice.delivered`, o `delivery.status == "completed"`).

### Reintentos

Hasta 2 reintentos (3 intentos) con espera creciente (0,5 s, 1 s, 2 s… con tope de 8 s y un poco de azar) ante un error de red, 429, 500,
502, 503, 504, un 409 `request_in_progress` o `previous_event_pending`, y todo problema que diga `retryable: true` (salvo el 402). Respeta
`Retry-After`; si pide más de `max_retry_after` (60 s) no espera y lanza el error con `error.retry_after`. Las operaciones sin
`Idempotency-Key` (crear un endpoint, `…/send`, `DELETE`) solo se reintentan con 429. Los 202 y los errores finales (400, 401, 402, 403, 404,
422 y los 409 `invalid_state`, `external_id_in_use`, `duplicate_document`) **nunca** se reintentan. Los reintentos de `urllib3` están apagados:
el SDK es el único que reintenta.

### La versión de la API

El SDK fija `Trevol-Version: 2026-10-22` en cada petición. **Ojo:** una llave creada con la versión `2026-10-21` que empiece a usar este SDK
pasa a `2026-10-22` (el encabezado manda): recibe `202 processing` donde antes recibía `503`. Si todavía no quieres ese cambio:
`Trevol(api_version="2026-10-21")`. Más en <https://platform.trevol.si/docs/versiones>.

### Errores tipados

`TrevolError` es la base; las clases salen del `code` del problem+json: `AuthenticationError`, `PermissionDeniedError`, `NotFoundError`,
`InvalidRequestError`, `IdempotencyError`, `ValidationError` (con `errors`: `field`, `pointer`, `message`), `ConflictError`,
`PreconditionError`, `DianRejectedError` (con `problem["document"]` y `problem["rules"]`), `BalanceError`, `RateLimitError`,
`DianUnavailableError` e `InternalServerError`. Un `code` que el SDK todavía no conoce llega como `TrevolError` con ese `code`: nunca
rompe. Además: `APIConnectionError` (no hubo respuesta), `ConfigurationError` (mal uso, antes de llamar) y `WebhookVerificationError`.
Cada error tiene `status`, `code`, `type`, `title`, `detail`, `request_id`, `retryable`, `retry_after`, `errors`, `idempotency_key`,
`problem` (el cuerpo completo) y `headers` (los de la respuesta). Ninguno incluye tu llave (ni su `repr`, ni su traceback).

### Webhooks

```python
from flask import Flask, request
from trevol import Webhook, WebhookVerificationError

app = Flask(__name__)
wh = Webhook(os.environ["TREVOL_WEBHOOK_SECRET"])  # whsec_…

@app.post("/webhooks/trevol")
def recibir():
    try:
        evento = wh.verify(request.get_data(), request.headers)   # el cuerpo CRUDO, no request.json
    except WebhookVerificationError:
        return "", 400
    # Deduplica por evento.id (también llega en la cabecera webhook-id): la verificación no evita repeticiones.
    datos = wh.event_data(evento)   # el modelo según evento.type (p. ej. DocumentEventData)
    return "", 200
```

En FastAPI usa `await request.body()`; en Django, `request.body`. La firma se calcula sobre los **bytes exactos**. `verify` acepta cualquier mapa de
cabeceras (Flask, Django, Starlette, `dict`) y el cuerpo como `str` o `bytes`; tolera 5 minutos hacia atrás y hacia adelante en `webhook-timestamp`.

### Estado y cabeceras de la respuesta

Cada método tiene una variante `…_with_http_info` que devuelve `ApiResponse` con `status_code`, `headers` y `data`:
`r = trevol.invoices.create_invoice_with_http_info(...); r.headers["request-id"]; r.headers["idempotent-replayed"]; r.data`.

### Cabeceras propias por llamada

Cada método acepta `_headers={...}` (se mezcla con las del SDK) y `_request_timeout=` (segundos).

## Opciones

```python
Trevol(
    api_key,
    api_version="2026-10-22",   # Trevol-Version en cada petición
    max_retries=2,              # 0 los apaga
    timeout=65.0,               # segundos por intento
    max_retry_after=60.0,       # segundos
    base_url="https://api.trevol.si/v1",
    environment="test",         # si la llave no coincide: ConfigurationError antes de llamar
)
```

## Cómo está hecho

- `src/trevol/_generado/` lo escribe [OpenAPI Generator](https://openapi-generator.tech) 7.26.0 (`python`, pydantic v2, urllib3) desde la
  especificación pública y **no se edita** (ver `GENERADO.md`). Para que un valor nuevo de un `enum` en lo que la API devuelve no rompa a quien
  ya integró, los modelos de respuesta se generan sin `enum` (los valores conocidos quedan en la descripción).
- Lo propio (`cliente.py`, `transporte.py`, `errores.py`, `paginacion.py`, `webhooks.py`) vive fuera y solo usa los puntos de extensión del
  código generado (una subclase de `ApiClient`).
- Las pruebas: `pip install -e ".[dev]" && pytest` (unitarias sin red contra un servidor HTTP local, con los mismos casos de los demás SDK en
  `pruebas/datos/`); `TREVOL_PRISM_URL=http://127.0.0.1:4010 pytest pruebas/prism pruebas/fragmentos` contra un servidor simulado
  (`npx @stoplight/prism-cli mock pruebas/datos/openapi.json -p 4010`) que valida cada petición contra la especificación, y que además corre
  como programa cada fragmento de código de la documentación.
- `python pruebas/humo/humo.py` es la prueba de humo **real** (solo con una llave `tvl_test_`; no emite documentos).

## Licencia

MIT © 2026 Trevol.
