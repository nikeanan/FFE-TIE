from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class MSMECategory(str, Enum):
    MICRO = "MICRO"
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"


class BuyerType(str, Enum):
    CPSE = "CPSE"
    STATE_PSU = "STATE_PSU"
    PRIVATE = "PRIVATE"
    GOVT_DEPT = "GOVT_DEPT"


class InvoiceLifecycleStatus(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    FIX_REQUIRED = "FIX_REQUIRED"
    BLOCKED = "BLOCKED"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    TREDS_LISTED = "TREDS_LISTED"
    DISCOUNTED = "DISCOUNTED"
    PAID_DIRECT = "PAID_DIRECT"
    OVERDUE = "OVERDUE"
    DISPUTED = "DISPUTED"
    CLOSED = "CLOSED"


class FlagSeverity(str, Enum):
    BLOCKER = "BLOCKER"
    WARN = "WARN"
    INFO = "INFO"


class LineItemModel(BaseModel):
    item_code: Optional[str] = None
    description: str
    quantity: Decimal
    unit: str = "NOS"
    unit_rate: Decimal
    gst_rate: Decimal = Decimal("18.0")
    hsn_code: Optional[str] = "8481.80"
    total_taxable: Decimal
    total_amount: Decimal


class MSME(BaseModel):
    id: str
    udyam_number: str
    gstin: str
    legal_name: str
    category: MSMECategory = MSMECategory.SMALL
    sector: str = "Manufacturing / Precision Engineering"
    treds_ids: Dict[str, str] = Field(default_factory=lambda: {
        "rxil": "RXIL-VEND-8821",
        "m1x": "M1X-MSME-3310",
        "invoicemart": "INV-MART-0912",
    })
    bank_verified: bool = True
    bank_account: str = "91802003881923"
    bank_ifsc: str = "HDFC0000123"
    whatsapp_number: str = "+919876543210"
    language_pref: str = "en"
    cash_credit_apr: Decimal = Decimal("0.125")  # 12.5% Bank OD/CC limit
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Buyer(BaseModel):
    id: str
    name: str
    type: BuyerType = BuyerType.CPSE
    gstin: str
    parent_id: Optional[str] = None
    treds_registered: bool = True
    payment_terms_days: int = 45
    division_unit: str = "Corporate"
    nodal_officer: str = "General Manager (Finance & Accounts)"
    escalation_contacts: List[str] = Field(default_factory=list)
    most_effective_channel: str = "EMAIL_FINANCE_HEAD"


class PurchaseOrder(BaseModel):
    id: str
    po_number: str
    buyer_id: str
    msme_id: str
    po_date: date
    delivery_due_date: date
    line_items: List[LineItemModel] = []
    total_amount: Decimal
    payment_terms_days: int = 45
    status: str = "RELEASED"


class GoodsReceiptNote(BaseModel):
    id: str
    grn_number: str
    po_id: str
    buyer_id: str
    msme_id: str
    grn_date: date
    inspected_by: str
    line_items: List[LineItemModel] = []
    accepted: bool = True


class ValidationFlag(BaseModel):
    id: Optional[int] = None
    invoice_id: str
    flag_code: str
    severity: FlagSeverity
    detail: str
    remedy_action: Optional[str] = None
    resolved: bool = False


class Invoice(BaseModel):
    id: str
    msme_id: str
    buyer_id: str
    po_id: Optional[str] = None
    po_number: Optional[str] = None
    irn: Optional[str] = None
    invoice_number: str
    invoice_date: date
    submitted_date: Optional[date] = None
    acceptance_date: Optional[date] = None
    amount: Decimal
    gst_amount: Decimal = Decimal("0.00")
    status: InvoiceLifecycleStatus = InvoiceLifecycleStatus.DRAFT
    due_date: Optional[date] = None
    predicted_pay_date: Optional[date] = None
    validation_score: float = 0.0
    treds_ready: bool = False
    line_items: List[LineItemModel] = []
    bank_account: Optional[str] = None
    bank_ifsc: Optional[str] = None
    vendor_code: Optional[str] = None
    hsn_code: Optional[str] = "8481.80"
    flags: List[ValidationFlag] = []


class InvoiceEvent(BaseModel):
    id: Optional[int] = None
    invoice_id: str
    event_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
    actor: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class BuyerBehaviourStats(BaseModel):
    buyer_id: str
    period: str
    avg_acceptance_days: float = 14.5
    avg_payment_days: float = 58.2
    rejection_rate: float = 0.18
    top_rejection_reasons: List[str] = Field(default_factory=lambda: [
        "Quantity mismatch with Store GRN",
        "Missing Vendor Code in billing header",
        "Disputed inspection certificate annexure",
        "HSN rate code discrepancy",
    ])
    on_time_rate: float = 0.42
    sample_size: int = 120
    most_effective_channel: str = "EMAIL_FINANCE_HEAD"
    escalation_contacts: List[str] = Field(default_factory=lambda: [
        "gm.finance@cpse.gov.in",
        "cfo@cpse.gov.in",
    ])


class BuyerLearnedRule(BaseModel):
    id: str
    buyer_id: str
    rule_code: str
    rule_name: str
    human_reason: str
    severity: FlagSeverity = FlagSeverity.BLOCKER
    rejection_count: int = 14
    check_type: str  # "VENDOR_CODE_REQUIRED" | "UDYAM_HEADER" | "INSPECTION_ATTACHMENT" | "GRN_MATCH"


class FinancingOffer(BaseModel):
    id: str
    invoice_id: str
    platform: str  # RXIL | M1X | INVOICEMART | C2FO
    financier: str
    discount_rate_apr: Decimal
    net_amount: Decimal
    valid_till: datetime
    status: str = "OPEN"
