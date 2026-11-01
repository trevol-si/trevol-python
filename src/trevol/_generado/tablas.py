"""Generado por sdks/herramientas/tablas.mjs desde la especificación. No editar: se borra y se vuelve a escribir."""

from __future__ import annotations

from trevol._generado.models.balance_event_data import BalanceEventData
from trevol._generado.models.certificate_event_data import CertificateEventData
from trevol._generado.models.document_event_data import DocumentEventData
from trevol._generado.models.equivalent_document_event_data import EquivalentDocumentEventData
from trevol._generado.models.numbering_expiring_event_data import NumberingExpiringEventData
from trevol._generado.models.numbering_low_event_data import NumberingLowEventData
from trevol._generado.models.payroll_event_data import PayrollEventData
from trevol._generado.models.radian_event_data import RadianEventData
from trevol._generado.models.support_document_event_data import SupportDocumentEventData
from trevol._generado.models.test_event_data import TestEventData

VERSION = "0.1.0"
API_VERSION = "2026-10-22"

# seguro: GET, preview, PATCH y todo POST/PUT con Idempotency-Key. solo_429: el resto.
OPERACIONES = [
    {
        "operationId": "correctCreditNote",
        "metodo": "PUT",
        "ruta": "/credit_notes/{id}",
        "recurso": "CreditNotes",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "correctDebitNote",
        "metodo": "PUT",
        "ruta": "/debit_notes/{id}",
        "recurso": "DebitNotes",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "correctEquivalentDocument",
        "metodo": "PUT",
        "ruta": "/equivalent_documents/{id}",
        "recurso": "EquivalentDocuments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "correctEquivalentDocumentAdjustment",
        "metodo": "PUT",
        "ruta": "/equivalent_document_adjustments/{id}",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "correctInvoice",
        "metodo": "PUT",
        "ruta": "/invoices/{id}",
        "recurso": "Invoices",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "correctPayroll",
        "metodo": "PUT",
        "ruta": "/payrolls/{id}",
        "recurso": "Payrolls",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "correctPayrollAdjustment",
        "metodo": "PUT",
        "ruta": "/payroll_adjustments/{id}",
        "recurso": "PayrollAdjustments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "correctSupportDocument",
        "metodo": "PUT",
        "ruta": "/support_documents/{id}",
        "recurso": "SupportDocuments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "correctSupportDocumentAdjustment",
        "metodo": "PUT",
        "ruta": "/support_document_adjustments/{id}",
        "recurso": "SupportDocumentAdjustments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createBalanceTopUp",
        "metodo": "POST",
        "ruta": "/balance/top_ups",
        "recurso": "Balance",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createCreditNote",
        "metodo": "POST",
        "ruta": "/credit_notes",
        "recurso": "CreditNotes",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createDebitNote",
        "metodo": "POST",
        "ruta": "/debit_notes",
        "recurso": "DebitNotes",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createEquivalentDocument",
        "metodo": "POST",
        "ruta": "/equivalent_documents",
        "recurso": "EquivalentDocuments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createEquivalentDocumentAdjustment",
        "metodo": "POST",
        "ruta": "/equivalent_document_adjustments",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createInvoice",
        "metodo": "POST",
        "ruta": "/invoices",
        "recurso": "Invoices",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createPayroll",
        "metodo": "POST",
        "ruta": "/payrolls",
        "recurso": "Payrolls",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createPayrollAdjustment",
        "metodo": "POST",
        "ruta": "/payroll_adjustments",
        "recurso": "PayrollAdjustments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createRadianEvent",
        "metodo": "POST",
        "ruta": "/radian_events",
        "recurso": "RadianEvents",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createSupportDocument",
        "metodo": "POST",
        "ruta": "/support_documents",
        "recurso": "SupportDocuments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createSupportDocumentAdjustment",
        "metodo": "POST",
        "ruta": "/support_document_adjustments",
        "recurso": "SupportDocumentAdjustments",
        "idempotente": True,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "createWebhookEndpoint",
        "metodo": "POST",
        "ruta": "/webhook_endpoints",
        "recurso": "WebhookEndpoints",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "deleteWebhookEndpoint",
        "metodo": "DELETE",
        "ruta": "/webhook_endpoints/{id}",
        "recurso": "WebhookEndpoints",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "downloadCreditNoteDianResponse",
        "metodo": "GET",
        "ruta": "/credit_notes/{id}/dian_response",
        "recurso": "CreditNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadCreditNotePdf",
        "metodo": "GET",
        "ruta": "/credit_notes/{id}/pdf",
        "recurso": "CreditNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "pdf"
    },
    {
        "operationId": "downloadCreditNoteXml",
        "metodo": "GET",
        "ruta": "/credit_notes/{id}/xml",
        "recurso": "CreditNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadCreditNoteZip",
        "metodo": "GET",
        "ruta": "/credit_notes/{id}/zip",
        "recurso": "CreditNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "zip"
    },
    {
        "operationId": "downloadDebitNoteDianResponse",
        "metodo": "GET",
        "ruta": "/debit_notes/{id}/dian_response",
        "recurso": "DebitNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadDebitNotePdf",
        "metodo": "GET",
        "ruta": "/debit_notes/{id}/pdf",
        "recurso": "DebitNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "pdf"
    },
    {
        "operationId": "downloadDebitNoteXml",
        "metodo": "GET",
        "ruta": "/debit_notes/{id}/xml",
        "recurso": "DebitNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadDebitNoteZip",
        "metodo": "GET",
        "ruta": "/debit_notes/{id}/zip",
        "recurso": "DebitNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "zip"
    },
    {
        "operationId": "downloadEquivalentDocumentAdjustmentDianResponse",
        "metodo": "GET",
        "ruta": "/equivalent_document_adjustments/{id}/dian_response",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadEquivalentDocumentAdjustmentPdf",
        "metodo": "GET",
        "ruta": "/equivalent_document_adjustments/{id}/pdf",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "pdf"
    },
    {
        "operationId": "downloadEquivalentDocumentAdjustmentXml",
        "metodo": "GET",
        "ruta": "/equivalent_document_adjustments/{id}/xml",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadEquivalentDocumentAdjustmentZip",
        "metodo": "GET",
        "ruta": "/equivalent_document_adjustments/{id}/zip",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "zip"
    },
    {
        "operationId": "downloadEquivalentDocumentDianResponse",
        "metodo": "GET",
        "ruta": "/equivalent_documents/{id}/dian_response",
        "recurso": "EquivalentDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadEquivalentDocumentPdf",
        "metodo": "GET",
        "ruta": "/equivalent_documents/{id}/pdf",
        "recurso": "EquivalentDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "pdf"
    },
    {
        "operationId": "downloadEquivalentDocumentXml",
        "metodo": "GET",
        "ruta": "/equivalent_documents/{id}/xml",
        "recurso": "EquivalentDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadEquivalentDocumentZip",
        "metodo": "GET",
        "ruta": "/equivalent_documents/{id}/zip",
        "recurso": "EquivalentDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "zip"
    },
    {
        "operationId": "downloadInvoiceDianResponse",
        "metodo": "GET",
        "ruta": "/invoices/{id}/dian_response",
        "recurso": "Invoices",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadInvoicePdf",
        "metodo": "GET",
        "ruta": "/invoices/{id}/pdf",
        "recurso": "Invoices",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "pdf"
    },
    {
        "operationId": "downloadInvoiceXml",
        "metodo": "GET",
        "ruta": "/invoices/{id}/xml",
        "recurso": "Invoices",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadInvoiceZip",
        "metodo": "GET",
        "ruta": "/invoices/{id}/zip",
        "recurso": "Invoices",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "zip"
    },
    {
        "operationId": "downloadPayrollAdjustmentDianResponse",
        "metodo": "GET",
        "ruta": "/payroll_adjustments/{id}/dian_response",
        "recurso": "PayrollAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadPayrollAdjustmentXml",
        "metodo": "GET",
        "ruta": "/payroll_adjustments/{id}/xml",
        "recurso": "PayrollAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadPayrollAdjustmentZip",
        "metodo": "GET",
        "ruta": "/payroll_adjustments/{id}/zip",
        "recurso": "PayrollAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "zip"
    },
    {
        "operationId": "downloadPayrollDianResponse",
        "metodo": "GET",
        "ruta": "/payrolls/{id}/dian_response",
        "recurso": "Payrolls",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadPayrollXml",
        "metodo": "GET",
        "ruta": "/payrolls/{id}/xml",
        "recurso": "Payrolls",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadPayrollZip",
        "metodo": "GET",
        "ruta": "/payrolls/{id}/zip",
        "recurso": "Payrolls",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "zip"
    },
    {
        "operationId": "downloadRadianEventXml",
        "metodo": "GET",
        "ruta": "/radian_events/{id}/xml",
        "recurso": "RadianEvents",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadSupportDocumentAdjustmentDianResponse",
        "metodo": "GET",
        "ruta": "/support_document_adjustments/{id}/dian_response",
        "recurso": "SupportDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadSupportDocumentAdjustmentXml",
        "metodo": "GET",
        "ruta": "/support_document_adjustments/{id}/xml",
        "recurso": "SupportDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadSupportDocumentDianResponse",
        "metodo": "GET",
        "ruta": "/support_documents/{id}/dian_response",
        "recurso": "SupportDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "downloadSupportDocumentXml",
        "metodo": "GET",
        "ruta": "/support_documents/{id}/xml",
        "recurso": "SupportDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": "xml"
    },
    {
        "operationId": "getHealth",
        "metodo": "GET",
        "ruta": "/health",
        "recurso": "General",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listBalanceTransactions",
        "metodo": "GET",
        "ruta": "/balance/transactions",
        "recurso": "Balance",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listCreditNotes",
        "metodo": "GET",
        "ruta": "/credit_notes",
        "recurso": "CreditNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listDebitNotes",
        "metodo": "GET",
        "ruta": "/debit_notes",
        "recurso": "DebitNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listEquivalentDocumentAdjustments",
        "metodo": "GET",
        "ruta": "/equivalent_document_adjustments",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listEquivalentDocuments",
        "metodo": "GET",
        "ruta": "/equivalent_documents",
        "recurso": "EquivalentDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listEvents",
        "metodo": "GET",
        "ruta": "/events",
        "recurso": "Events",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listInvoices",
        "metodo": "GET",
        "ruta": "/invoices",
        "recurso": "Invoices",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listPayrollAdjustments",
        "metodo": "GET",
        "ruta": "/payroll_adjustments",
        "recurso": "PayrollAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listPayrolls",
        "metodo": "GET",
        "ruta": "/payrolls",
        "recurso": "Payrolls",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listRadianEvents",
        "metodo": "GET",
        "ruta": "/radian_events",
        "recurso": "RadianEvents",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listRequests",
        "metodo": "GET",
        "ruta": "/requests",
        "recurso": "Requests",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listSupportDocumentAdjustments",
        "metodo": "GET",
        "ruta": "/support_document_adjustments",
        "recurso": "SupportDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listSupportDocuments",
        "metodo": "GET",
        "ruta": "/support_documents",
        "recurso": "SupportDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listWebhookEndpointDeliveries",
        "metodo": "GET",
        "ruta": "/webhook_endpoints/{id}/deliveries",
        "recurso": "WebhookEndpoints",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "listWebhookEndpoints",
        "metodo": "GET",
        "ruta": "/webhook_endpoints",
        "recurso": "WebhookEndpoints",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "previewCreditNote",
        "metodo": "POST",
        "ruta": "/credit_notes/preview",
        "recurso": "CreditNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "previewDebitNote",
        "metodo": "POST",
        "ruta": "/debit_notes/preview",
        "recurso": "DebitNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "previewEquivalentDocument",
        "metodo": "POST",
        "ruta": "/equivalent_documents/preview",
        "recurso": "EquivalentDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "previewEquivalentDocumentAdjustment",
        "metodo": "POST",
        "ruta": "/equivalent_document_adjustments/preview",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "previewInvoice",
        "metodo": "POST",
        "ruta": "/invoices/preview",
        "recurso": "Invoices",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "previewPayroll",
        "metodo": "POST",
        "ruta": "/payrolls/preview",
        "recurso": "Payrolls",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "previewPayrollAdjustment",
        "metodo": "POST",
        "ruta": "/payroll_adjustments/preview",
        "recurso": "PayrollAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "previewSupportDocument",
        "metodo": "POST",
        "ruta": "/support_documents/preview",
        "recurso": "SupportDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "previewSupportDocumentAdjustment",
        "metodo": "POST",
        "ruta": "/support_document_adjustments/preview",
        "recurso": "SupportDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "resendEvent",
        "metodo": "POST",
        "ruta": "/events/{id}/resend",
        "recurso": "Events",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "retrieveBalance",
        "metodo": "GET",
        "ruta": "/balance",
        "recurso": "Balance",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveCompany",
        "metodo": "GET",
        "ruta": "/company",
        "recurso": "General",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveCreditNote",
        "metodo": "GET",
        "ruta": "/credit_notes/{id}",
        "recurso": "CreditNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveDebitNote",
        "metodo": "GET",
        "ruta": "/debit_notes/{id}",
        "recurso": "DebitNotes",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveDianAcquirer",
        "metodo": "GET",
        "ruta": "/dian/acquirer",
        "recurso": "General",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveEquivalentDocument",
        "metodo": "GET",
        "ruta": "/equivalent_documents/{id}",
        "recurso": "EquivalentDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveEquivalentDocumentAdjustment",
        "metodo": "GET",
        "ruta": "/equivalent_document_adjustments/{id}",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveEvent",
        "metodo": "GET",
        "ruta": "/events/{id}",
        "recurso": "Events",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveInvoice",
        "metodo": "GET",
        "ruta": "/invoices/{id}",
        "recurso": "Invoices",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveInvoiceTacitAcceptance",
        "metodo": "GET",
        "ruta": "/invoices/{id}/tacit_acceptance",
        "recurso": "Invoices",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrievePayroll",
        "metodo": "GET",
        "ruta": "/payrolls/{id}",
        "recurso": "Payrolls",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrievePayrollAdjustment",
        "metodo": "GET",
        "ruta": "/payroll_adjustments/{id}",
        "recurso": "PayrollAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveRadianEvent",
        "metodo": "GET",
        "ruta": "/radian_events/{id}",
        "recurso": "RadianEvents",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveSupportDocument",
        "metodo": "GET",
        "ruta": "/support_documents/{id}",
        "recurso": "SupportDocuments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveSupportDocumentAdjustment",
        "metodo": "GET",
        "ruta": "/support_document_adjustments/{id}",
        "recurso": "SupportDocumentAdjustments",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveTacitAcceptanceByCufe",
        "metodo": "GET",
        "ruta": "/radian_events/tacit_acceptance",
        "recurso": "RadianEvents",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "retrieveWebhookEndpoint",
        "metodo": "GET",
        "ruta": "/webhook_endpoints/{id}",
        "recurso": "WebhookEndpoints",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    },
    {
        "operationId": "rotateWebhookEndpointSecret",
        "metodo": "POST",
        "ruta": "/webhook_endpoints/{id}/rotate_secret",
        "recurso": "WebhookEndpoints",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendCreditNote",
        "metodo": "POST",
        "ruta": "/credit_notes/{id}/send",
        "recurso": "CreditNotes",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendDebitNote",
        "metodo": "POST",
        "ruta": "/debit_notes/{id}/send",
        "recurso": "DebitNotes",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendEquivalentDocument",
        "metodo": "POST",
        "ruta": "/equivalent_documents/{id}/send",
        "recurso": "EquivalentDocuments",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendEquivalentDocumentAdjustment",
        "metodo": "POST",
        "ruta": "/equivalent_document_adjustments/{id}/send",
        "recurso": "EquivalentDocumentAdjustments",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendInvoice",
        "metodo": "POST",
        "ruta": "/invoices/{id}/send",
        "recurso": "Invoices",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendPayroll",
        "metodo": "POST",
        "ruta": "/payrolls/{id}/send",
        "recurso": "Payrolls",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendPayrollAdjustment",
        "metodo": "POST",
        "ruta": "/payroll_adjustments/{id}/send",
        "recurso": "PayrollAdjustments",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendRadianEvent",
        "metodo": "POST",
        "ruta": "/radian_events/{id}/send",
        "recurso": "RadianEvents",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendSupportDocument",
        "metodo": "POST",
        "ruta": "/support_documents/{id}/send",
        "recurso": "SupportDocuments",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "sendSupportDocumentAdjustment",
        "metodo": "POST",
        "ruta": "/support_document_adjustments/{id}/send",
        "recurso": "SupportDocumentAdjustments",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "testWebhookEndpoint",
        "metodo": "POST",
        "ruta": "/webhook_endpoints/{id}/test",
        "recurso": "WebhookEndpoints",
        "idempotente": False,
        "reintento": "solo_429",
        "binario": None
    },
    {
        "operationId": "updateWebhookEndpoint",
        "metodo": "PATCH",
        "ruta": "/webhook_endpoints/{id}",
        "recurso": "WebhookEndpoints",
        "idempotente": False,
        "reintento": "seguro",
        "binario": None
    }
]

# El nombre de cada etiqueta del SDK (una propiedad del cliente por etiqueta, en snake_case).
ETIQUETAS = [
    "Balance",
    "CreditNotes",
    "DebitNotes",
    "EquivalentDocumentAdjustments",
    "EquivalentDocuments",
    "Events",
    "General",
    "Invoices",
    "PayrollAdjustments",
    "Payrolls",
    "RadianEvents",
    "Requests",
    "SupportDocumentAdjustments",
    "SupportDocuments",
    "WebhookEndpoints"
]

# code de problem+json -> clase de error
CLASE_POR_CODE = {
    "authentication_required": "AuthenticationError",
    "invalid_api_key": "AuthenticationError",
    "permission_denied": "PermissionDeniedError",
    "not_found": "NotFoundError",
    "method_not_allowed": "InvalidRequestError",
    "unsupported_version": "InvalidRequestError",
    "invalid_json": "InvalidRequestError",
    "invalid_request": "InvalidRequestError",
    "idempotency_key_required": "InvalidRequestError",
    "idempotency_key_reused": "IdempotencyError",
    "validation_error": "ValidationError",
    "external_id_in_use": "ConflictError",
    "invalid_state": "ConflictError",
    "duplicate_document": "ConflictError",
    "request_in_progress": "ConflictError",
    "previous_event_pending": "ConflictError",
    "file_unavailable": "ConflictError",
    "webhook_limit_reached": "ConflictError",
    "company_not_enabled": "PreconditionError",
    "numbering_unavailable": "PreconditionError",
    "certificate_problem": "PreconditionError",
    "tacit_acceptance_not_due": "PreconditionError",
    "dian_rejected": "DianRejectedError",
    "insufficient_balance": "BalanceError",
    "top_up_below_minimum": "BalanceError",
    "top_up_above_maximum": "BalanceError",
    "top_ups_unavailable": "BalanceError",
    "rate_limited": "RateLimitError",
    "dian_unavailable": "DianUnavailableError",
    "internal_error": "InternalServerError"
}

# Estado HTTP -> clase de error (cuando no hay un code conocido; 5xx en general)
CLASE_POR_ESTADO = {
    "400": "InvalidRequestError",
    "401": "AuthenticationError",
    "402": "BalanceError",
    "403": "PermissionDeniedError",
    "404": "NotFoundError",
    "409": "ConflictError",
    "422": "ValidationError",
    "429": "RateLimitError",
    "5xx": "InternalServerError"
}

# Event.type -> el modelo de su `data`
EVENTO_MODELOS = {
    "balance.low": BalanceEventData,
    "certificate.expiring": CertificateEventData,
    "credit_note.accepted": DocumentEventData,
    "credit_note.delivered": DocumentEventData,
    "credit_note.email_bounced": DocumentEventData,
    "credit_note.email_failed": DocumentEventData,
    "credit_note.error": DocumentEventData,
    "credit_note.rejected": DocumentEventData,
    "debit_note.accepted": DocumentEventData,
    "debit_note.delivered": DocumentEventData,
    "debit_note.email_bounced": DocumentEventData,
    "debit_note.email_failed": DocumentEventData,
    "debit_note.error": DocumentEventData,
    "debit_note.rejected": DocumentEventData,
    "equivalent_document.accepted": EquivalentDocumentEventData,
    "equivalent_document.delivered": EquivalentDocumentEventData,
    "equivalent_document.email_bounced": EquivalentDocumentEventData,
    "equivalent_document.email_failed": EquivalentDocumentEventData,
    "equivalent_document.error": EquivalentDocumentEventData,
    "equivalent_document.rejected": EquivalentDocumentEventData,
    "equivalent_document_adjustment.accepted": EquivalentDocumentEventData,
    "equivalent_document_adjustment.delivered": EquivalentDocumentEventData,
    "equivalent_document_adjustment.email_bounced": EquivalentDocumentEventData,
    "equivalent_document_adjustment.email_failed": EquivalentDocumentEventData,
    "equivalent_document_adjustment.error": EquivalentDocumentEventData,
    "equivalent_document_adjustment.rejected": EquivalentDocumentEventData,
    "invoice.accepted": DocumentEventData,
    "invoice.delivered": DocumentEventData,
    "invoice.email_bounced": DocumentEventData,
    "invoice.email_failed": DocumentEventData,
    "invoice.error": DocumentEventData,
    "invoice.rejected": DocumentEventData,
    "numbering.expiring": NumberingExpiringEventData,
    "numbering.low": NumberingLowEventData,
    "payroll.accepted": PayrollEventData,
    "payroll.error": PayrollEventData,
    "payroll.rejected": PayrollEventData,
    "payroll_adjustment.accepted": PayrollEventData,
    "payroll_adjustment.error": PayrollEventData,
    "payroll_adjustment.rejected": PayrollEventData,
    "radian_event.accepted": RadianEventData,
    "radian_event.error": RadianEventData,
    "radian_event.rejected": RadianEventData,
    "support_document.accepted": SupportDocumentEventData,
    "support_document.error": SupportDocumentEventData,
    "support_document.rejected": SupportDocumentEventData,
    "support_document_adjustment.accepted": SupportDocumentEventData,
    "support_document_adjustment.error": SupportDocumentEventData,
    "support_document_adjustment.rejected": SupportDocumentEventData,
    "webhook.test": TestEventData,
}
