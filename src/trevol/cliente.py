"""El cliente: `Trevol(api_key, ...)` (docs/api/43 §2.6.1)."""

from __future__ import annotations

import os
import platform
from typing import Any, Callable, Iterator, Optional

from trevol._generado.api.balance_api import BalanceApi
from trevol._generado.api.credit_notes_api import CreditNotesApi
from trevol._generado.api.debit_notes_api import DebitNotesApi
from trevol._generado.api.equivalent_document_adjustments_api import EquivalentDocumentAdjustmentsApi
from trevol._generado.api.equivalent_documents_api import EquivalentDocumentsApi
from trevol._generado.api.events_api import EventsApi
from trevol._generado.api.general_api import GeneralApi
from trevol._generado.api.invoices_api import InvoicesApi
from trevol._generado.api.payroll_adjustments_api import PayrollAdjustmentsApi
from trevol._generado.api.payrolls_api import PayrollsApi
from trevol._generado.api.radian_events_api import RadianEventsApi
from trevol._generado.api.requests_api import RequestsApi
from trevol._generado.api.support_document_adjustments_api import SupportDocumentAdjustmentsApi
from trevol._generado.api.support_documents_api import SupportDocumentsApi
from trevol._generado.api.webhook_endpoints_api import WebhookEndpointsApi
from trevol._generado.tablas import API_VERSION, VERSION

from .errores import ConfigurationError
from .llave import Entorno, entorno_de_la_llave
from .paginacion import paginar
from .transporte import ClienteApi, Opciones, configuracion

URL_BASE = "https://api.trevol.si/v1"


class Trevol:
    """El cliente de la API de Trevol. Una propiedad por recurso (`invoices`, `credit_notes`, …), cada una con los métodos generados de la
    especificación (`create_invoice`, `list_invoices`, `retrieve_invoice`…).

    Args:
        api_key: `tvl_test_…` o `tvl_live_…`; si falta se lee `TREVOL_API_KEY`.
        api_version: el valor de `Trevol-Version` en cada petición. Por defecto la versión con que se generó este SDK (`API_VERSION`).
        max_retries: reintentos tras el primer intento (3 intentos en total por defecto). 0 los apaga.
        timeout: segundos por intento. Por defecto 65, como el playground.
        max_retry_after: si `Retry-After` pide esperar más segundos que esto, no se espera: se lanza el error con `retry_after`.
        base_url: por defecto https://api.trevol.si/v1 (para un servidor simulado en las pruebas).
        environment: si se pasa y la llave no coincide, `ConfigurationError` ANTES de llamar.
        proxy: URL de un proxy HTTP(S) o SOCKS (p. ej. "http://proxy.miempresa.co:3128").
    """

    environment: Entorno
    api_version: str

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        api_version: Optional[str] = None,
        max_retries: int = 2,
        timeout: float = 65.0,
        max_retry_after: float = 60.0,
        base_url: str = URL_BASE,
        environment: Optional[Entorno] = None,
        proxy: Optional[str] = None,
        _internos: Optional[dict[str, Callable[..., Any]]] = None,
    ) -> None:
        llave = api_key if api_key is not None else os.environ.get("TREVOL_API_KEY")
        if llave is None or llave == "":
            raise ConfigurationError("Falta la llave de la API: pásala a Trevol(api_key=...) o define la variable de entorno TREVOL_API_KEY.")
        self.environment = entorno_de_la_llave(llave)
        if environment is not None and environment != self.environment:
            raise ConfigurationError(
                f"Pediste el entorno «{environment}» pero la llave es de «{self.environment}»"
                f" ({'tvl_test_ = habilitación' if self.environment == 'test' else 'tvl_live_ = producción'})."
            )
        self.api_version = api_version or API_VERSION
        i = _internos or {}
        extra = {k: v for k, v in {"sleep": i.get("sleep"), "random": i.get("random"), "uuid": i.get("uuid")}.items() if v is not None}
        opciones = Opciones(
            llave=llave.strip(), api_version=self.api_version,
            user_agent=f"trevol-python/{VERSION} (python {platform.python_version()}; +https://platform.trevol.si/docs)",
            max_reintentos=max_retries, timeout=timeout, max_retry_after=max_retry_after, **extra,
        )
        cliente = ClienteApi(configuracion(base_url.rstrip("/"), proxy), opciones)
        self._cliente = cliente
        self.balance = BalanceApi(cliente)
        self.credit_notes = CreditNotesApi(cliente)
        self.debit_notes = DebitNotesApi(cliente)
        self.equivalent_document_adjustments = EquivalentDocumentAdjustmentsApi(cliente)
        self.equivalent_documents = EquivalentDocumentsApi(cliente)
        self.events = EventsApi(cliente)
        self.general = GeneralApi(cliente)
        self.invoices = InvoicesApi(cliente)
        self.payroll_adjustments = PayrollAdjustmentsApi(cliente)
        self.payrolls = PayrollsApi(cliente)
        self.radian_events = RadianEventsApi(cliente)
        self.requests = RequestsApi(cliente)
        self.support_document_adjustments = SupportDocumentAdjustmentsApi(cliente)
        self.support_documents = SupportDocumentsApi(cliente)
        self.webhook_endpoints = WebhookEndpointsApi(cliente)

    def paginate(self, pagina: Callable[[Optional[str]], Any]) -> Iterator[Any]:
        """Recorre todas las páginas de un listado, perezosamente:
        `for f in trevol.paginate(lambda cursor: trevol.invoices.list_invoices(limit=100, starting_after=cursor)): ...`"""
        return paginar(pagina)

    def __repr__(self) -> str:                      # la llave no se guarda en el objeto, pero un repr nunca debe enseñar nada sensible
        return f"<Trevol environment={self.environment!r} api_version={self.api_version!r}>"
