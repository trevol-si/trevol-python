"""La llave de la API: su formato y el entorno que se deduce de su prefijo (docs/api/43 §2.6.1)."""

from __future__ import annotations

import re
from typing import Any, Literal

from .errores import ConfigurationError

Entorno = Literal["test", "live"]
_FORMATO = re.compile(r"tvl_(test|live)_[0-9a-f]{64}")


def entorno_de_la_llave(llave: Any) -> Entorno:
    """Valida la llave y devuelve su entorno: `test` (habilitación de la DIAN) o `live` (producción). El mensaje NUNCA incluye la llave."""
    m = _FORMATO.fullmatch(llave.strip()) if isinstance(llave, str) else None
    if not m:
        raise ConfigurationError(
            "La llave de la API no tiene el formato esperado (tvl_test_… o tvl_live_… con 64 caracteres hexadecimales). "
            "Créala en https://platform.trevol.si/llaves y pásala completa o define TREVOL_API_KEY."
        )
    return m.group(1)  # type: ignore[return-value]
