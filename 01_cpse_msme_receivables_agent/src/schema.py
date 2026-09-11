from datetime import date
from decimal import Decimal
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class DocumentType(str, Enum):
    PURCHASE_ORDER = "PURCHASE_ORDER"
    TAX_INVOICE = "TAX_INVOICE"
    DELIVERY_CHALLAN = "DELIVERY_CHALLAN"
    INSPECTION_NOTE = "INSPECTION_NOTE"
    GOODS_RECEIPT_NOTE = "GOODS_RECEIPT_NOTE"


class InvoiceStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    DISCREPANCY_FOUND = "DISCREPANCY_FOUND"
    SUBMITTED_TO_CPSE = "SUBMITTED_TO_CPSE"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    TREDS_UPLOADED = "TREDS_UPLOADED"
    TREDS_FACTORING_ACTIVE = "TREDS_FACTORING_ACTIVE"
    SETTLED = "SETTLED"
    OVERDUE_MSMED_BREACH = "OVERDUE_MSMED_BREACH"


class LineItem(BaseModel):
    item_code: Optional[str] = None
    description: str
    quantity: Decimal
    unit: str
    unit_rate: Decimal
    gst_rate: Decimal
    total_taxable: Decimal
    total_amount: Decimal


class ExtractedDocument(BaseModel):
    doc_type: DocumentType
    doc_number: str
    doc_date: date
    buyer_gstin: str
    buyer_name: str
    seller_gstin: str
    seller_name: str
    po_reference: Optional[str] = None
    line_items: List[LineItem] = []
    total_amount: Decimal
    payment_terms_days: int = 45
