"""trevol — SDK de Python para la API de Trevol. Documentación: https://platform.trevol.si/docs

    from trevol import Trevol, TrevolError, ValidationError, Webhook
"""

import warnings

with warnings.catch_warnings():
    # El modelo `Pos` tiene un campo `register` (así lo llama la API) que pydantic avisa que "tapa" un atributo de BaseModel.
    warnings.filterwarnings("ignore", message='Field name "register"', category=UserWarning)
    from trevol._generado.models import *  # noqa: F401,F403 - los modelos para tipar tu código
    from trevol._generado.tablas import API_VERSION, VERSION

from .cliente import Trevol
from .errores import (
    APIConnectionError,
    AuthenticationError,
    BalanceError,
    ConfigurationError,
    ConflictError,
    DianRejectedError,
    DianUnavailableError,
    ErrorDeCampo,
    IdempotencyError,
    InternalServerError,
    InvalidRequestError,
    NotFoundError,
    PermissionDeniedError,
    PreconditionError,
    RateLimitError,
    TrevolError,
    ValidationError,
    WebhookVerificationError,
)
from .llave import Entorno
from .paginacion import paginar
from .transporte import Decision, Resultado, decidir, espera_propia
from .webhooks import Webhook

__version__ = VERSION

__all__ = [
    "Trevol", "Webhook", "paginar", "decidir", "espera_propia", "Decision", "Resultado", "Entorno", "VERSION", "API_VERSION",
    "TrevolError", "AuthenticationError", "PermissionDeniedError", "NotFoundError", "InvalidRequestError", "IdempotencyError",
    "ValidationError", "ConflictError", "PreconditionError", "DianRejectedError", "BalanceError", "RateLimitError",
    "DianUnavailableError", "InternalServerError", "APIConnectionError", "ConfigurationError", "WebhookVerificationError", "ErrorDeCampo",
]
