# Registro de cambios

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y el versionado, [SemVer](https://semver.org/lang/es/): antes
de la 1.0, un cambio incompatible sube el número menor.

## [0.1.0] — sin publicar

Primera versión (API `2026-10-22`).

- Cliente `Trevol` con un recurso por etiqueta de la API (`invoices`, `credit_notes`, `debit_notes`, `support_documents`, `payrolls`,
  `radian_events`, `webhook_endpoints`, `events`, `requests`, `balance`, `general`…), modelos pydantic generados de la especificación.
- `Idempotency-Key` automática (la misma en los reintentos), reintentos con espera creciente que respetan `Retry-After`, errores tipados por
  `code`, entorno deducido del prefijo de la llave, `Trevol-Version` fijada.
- `paginate` (iterador), descargas de PDF, XML y ZIP como `bytes`, `Webhook.verify` y `Webhook.event_data` (Standard Webhooks).
