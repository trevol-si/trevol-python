"""Los errores del SDK (docs/api/43-sdks-y-documentacion.md §2.6.5).

Toda respuesta que no es 2xx se convierte en uno de estos, con el `code` del problem+json: es el mismo vocabulario que la documentación
(https://platform.trevol.si/docs/errores). Ningún error lleva la llave ni las cabeceras de la PETICIÓN.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field as _campo
from typing import Any, Mapping, Optional


@dataclass(frozen=True)
class ErrorDeCampo:
    """Una de las `errors[]` de un problema 422: qué campo falló (`pointer`) y por qué."""

    field: Optional[str] = None
    pointer: Optional[str] = None
    message: Optional[str] = None
    extra: Mapping[str, Any] = _campo(default_factory=dict)


class TrevolError(Exception):
    """La base de todos los errores del SDK: un `except TrevolError` ya lo atrapa todo."""

    def __init__(
        self,
        mensaje: str,
        *,
        status: Optional[int] = None,
        code: Optional[str] = None,
        type: Optional[str] = None,  # noqa: A002 - el nombre del campo de problem+json
        title: Optional[str] = None,
        detail: Optional[str] = None,
        request_id: Optional[str] = None,
        retryable: Optional[bool] = None,
        retry_after: Optional[float] = None,
        errors: Optional[list[ErrorDeCampo]] = None,
        idempotency_key: Optional[str] = None,
        problem: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(mensaje)
        self.status = status
        self.code = code
        self.type = type
        self.title = title
        self.detail = detail
        self.request_id = request_id
        self.retryable = retryable
        self.retry_after = retry_after
        self.errors: list[ErrorDeCampo] = errors or []
        #: La Idempotency-Key de la llamada: úsala para reintentar más tarde con la MISMA clave.
        self.idempotency_key = idempotency_key
        #: El cuerpo problem+json completo, con los campos extra (`existing_id`, `reason`, `document`, `rules`…).
        self.problem = problem
        #: Las cabeceras de la RESPUESTA.
        self.headers = headers

    def __str__(self) -> str:
        partes = [type(self).__name__]
        if self.code:
            partes.append(self.code)
        if self.status is not None:
            partes.append(f"HTTP {self.status}")
        cola = f" [request_id={self.request_id}]" if self.request_id else ""
        return f"{' '.join(partes)}: {self.detail or self.title or self.args[0]}{cola}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} code={self.code!r} status={self.status!r} request_id={self.request_id!r}>"


class AuthenticationError(TrevolError):
    pass


class PermissionDeniedError(TrevolError):
    pass


class NotFoundError(TrevolError):
    pass


class InvalidRequestError(TrevolError):
    pass


class IdempotencyError(TrevolError):
    pass


class ValidationError(TrevolError):
    """422 `validation_error`: `errors` dice qué campo (`pointer`) y por qué."""


class ConflictError(TrevolError):
    pass


class PreconditionError(TrevolError):
    pass


class DianRejectedError(TrevolError):
    """422 `dian_rejected`: `problem["document"]` trae el documento y `problem["rules"]` las reglas que la DIAN aplicó."""


class BalanceError(TrevolError):
    pass


class RateLimitError(TrevolError):
    pass


class DianUnavailableError(TrevolError):
    pass


class InternalServerError(TrevolError):
    pass


class APIConnectionError(TrevolError):
    """No hubo respuesta: red, DNS, TLS o tiempo agotado. Lleva la `idempotency_key` para reintentar sin duplicar."""


class ConfigurationError(TrevolError):
    """Mal uso del SDK, antes de llamar: llave mal formada, entorno que no coincide. Nunca incluye la llave."""


class WebhookVerificationError(TrevolError):
    """La firma, la fecha o las cabeceras de un webhook no son válidas. `motivo`: firma, fecha, cabeceras o cuerpo."""

    def __init__(self, mensaje: str, motivo: str) -> None:
        super().__init__(mensaje)
        self.motivo = motivo


_CLASES: dict[str, type[TrevolError]] = {
    c.__name__: c
    for c in (AuthenticationError, PermissionDeniedError, NotFoundError, InvalidRequestError, IdempotencyError, ValidationError,
              ConflictError, PreconditionError, DianRejectedError, BalanceError, RateLimitError, DianUnavailableError,
              InternalServerError)
}

_RECORTE = 2048


def _numero(v: Any) -> Optional[float]:
    if isinstance(v, bool):
        return None
    try:
        n = float(v)
    except (TypeError, ValueError):
        return None
    return n if n >= 0 and n == n and n != float("inf") else None


def leer_retry_after(valor: Optional[str], ahora: Optional[float] = None) -> Optional[float]:
    """El valor de `Retry-After`: segundos o una fecha HTTP. None si no está o no se entiende."""
    if not valor:
        return None
    n = _numero(valor)
    if n is not None:
        return n
    from email.utils import parsedate_to_datetime
    from time import time

    try:
        fecha = parsedate_to_datetime(valor).timestamp()
    except (TypeError, ValueError):
        return None
    return max(0.0, float(int(fecha - (ahora if ahora is not None else time()) + 0.999)))


def error_de_respuesta(
    estado: int,
    texto: str,
    cabeceras: Mapping[str, str],
    por_code: Mapping[str, str],
    por_estado: Mapping[str, str],
    idempotency_key: Optional[str],
) -> TrevolError:
    """Convierte una respuesta que no es 2xx en su error tipado. El cuerpo se lee como un mapa TOLERANTE (nunca con el modelo generado:
    un `code` nuevo o un campo que falta no puede romper el manejo de errores)."""
    cab = {k.lower(): v for k, v in cabeceras.items()}
    cuerpo: Optional[dict[str, Any]] = None
    try:
        j = json.loads(texto)
        if isinstance(j, dict):
            cuerpo = j
    except ValueError:
        cuerpo = None

    def cadena(clave: str) -> Optional[str]:
        v = cuerpo.get(clave) if cuerpo else None
        return v if isinstance(v, str) else None

    code = cadena("code")
    detail = cadena("detail")
    title = cadena("title")
    errores = []
    if cuerpo and isinstance(cuerpo.get("errors"), list):
        for x in cuerpo["errors"]:
            if isinstance(x, dict):
                extra = {k: v for k, v in x.items() if k not in ("field", "pointer", "message")}
                errores.append(ErrorDeCampo(x.get("field"), x.get("pointer"), x.get("message"), extra))
    retryable = cuerpo.get("retryable") if cuerpo and isinstance(cuerpo.get("retryable"), bool) else None
    retry_after = leer_retry_after(cab.get("retry-after"))
    if retry_after is None and cuerpo:
        retry_after = _numero(cuerpo.get("retry_after"))
    mensaje = detail or title or (f"La API respondió {estado}" if cuerpo else f"La API respondió {estado} sin problem+json")
    if code:
        clase = por_code.get(code)             # un code que el SDK no conoce (la API sumó uno) da la base, nunca rompe
    else:
        clase = por_estado.get(str(estado)) or (por_estado.get("5xx") if estado >= 500 else None)
    ctor = _CLASES.get(clase or "", TrevolError)
    return ctor(
        mensaje, status=estado, code=code, type=cadena("type"), title=title,
        detail=detail if cuerpo is not None else (texto.strip()[:_RECORTE] or None),
        request_id=cadena("request_id") or cab.get("request-id"), retryable=retryable, retry_after=retry_after,
        errors=errores, idempotency_key=idempotency_key, problem=cuerpo, headers=dict(cabeceras),
    )
