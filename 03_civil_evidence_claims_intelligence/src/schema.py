from datetime import date
from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel


class ArtifactType(str, Enum):
    BOQ_ITEM = "BOQ_ITEM"
    DRAWING_REVISION = "DRAWING_REVISION"
    MEASUREMENT_BOOK_ENTRY = "MEASUREMENT_BOOK_ENTRY"
    SITE_PHOTO = "SITE_PHOTO"
    RFI_INSPECTION = "RFI_INSPECTION"
    CORRESPONDENCE_LETTER = "CORRESPONDENCE_LETTER"
    VARIATION_ORDER = "VARIATION_ORDER"
    HINDRANCE_REGISTER_ENTRY = "HINDRANCE_REGISTER_ENTRY"
    SITE_ORDER_BOOK = "SITE_ORDER_BOOK"
    WEATHER_REPORT = "WEATHER_REPORT"


class ContractClause(str, Enum):
    CPWD_CLAUSE_12_VARIATIONS = "CPWD_CLAUSE_12_VARIATIONS"
    CPWD_CLAUSE_5_EOT = "CPWD_CLAUSE_5_EOT"
    CPWD_CLAUSE_10CA_MATERIAL = "CPWD_CLAUSE_10CA_MATERIAL"
    CPWD_CLAUSE_10CC_ESCALATION = "CPWD_CLAUSE_10CC_ESCALATION"
    FIDIC_RED_CLAUSE_13_VARIATIONS = "FIDIC_RED_CLAUSE_13_VARIATIONS"
    FIDIC_RED_CLAUSE_8_4_EOT = "FIDIC_RED_CLAUSE_8_4_EOT"
    FIDIC_RED_CLAUSE_13_7_ESCALATION = "FIDIC_RED_CLAUSE_13_7_ESCALATION"
    NHAI_EPC_SCHEDULE_J_VARIATIONS = "NHAI_EPC_SCHEDULE_J_VARIATIONS"


class DelayCategory(str, Enum):
    EMPLOYER_RISK = "EMPLOYER_RISK"            # e.g., delay in handing over site, drawing delay, unmapped utilities
    CONTRACTOR_RISK = "CONTRACTOR_RISK"        # e.g., equipment breakdown, labor shortage
    FORCE_MAJEURE = "FORCE_MAJEURE"            # e.g., extraordinary flood, pandemic, state lockdown
    CONCURRENT_DELAY = "CONCURRENT_DELAY"      # Overlapping contractor + employer delays


class BOQItem(BaseModel):
    item_id: str
    item_no: str
    description: str
    unit: str
    tender_quantity: float
    tender_rate: float
    executed_quantity: float = 0.0
    billed_quantity: float = 0.0

    @property
    def tender_amount(self) -> float:
        return self.tender_quantity * self.tender_rate

    @property
    def executed_amount(self) -> float:
        return self.executed_quantity * self.tender_rate


class MeasurementEntry(BaseModel):
    entry_id: str
    mb_book_no: str
    page_no: int
    boq_item_id: str
    date_recorded: date
    location: str  # e.g., "Pier P-04 to P-05 Deck Slab"
    quantity: float
    unit: str
    recorded_by: str
    verified_by_consultant: bool = False


class EvidenceNode(BaseModel):
    node_id: str
    artifact_type: ArtifactType
    title: str
    date_created: date
    reference_path: str
    metadata: dict = {}


class DelayEvent(BaseModel):
    event_id: str
    title: str
    category: DelayCategory
    start_date: date
    end_date: date
    duration_days: int
    impacted_activity: str
    is_critical_path: bool
    evidence_nodes: List[str] = []
    daily_site_overhead_inr: float = 85000.0  # Daily site idling cost for prolongation
    ld_liability_risk_inr_per_day: float = 120000.0


class EscalationComponent(str, Enum):
    CEMENT = "CEMENT"
    STEEL_TMT = "STEEL_TMT"
    BITUMEN = "BITUMEN"
    POL_FUEL = "POL_FUEL"
    LABOUR = "LABOUR"


class EscalationCalculationResult(BaseModel):
    component: EscalationComponent
    base_index_ci0: float
    current_index_cin: float
    delta_index_percent: float
    base_rate_inr: float
    escalation_amount_inr: float
    clause_reference: str
    is_claimable: bool


class ProlongationClaim(BaseModel):
    total_eot_days_requested: int
    employer_delay_days: int
    concurrent_delay_days: int
    daily_overhead_cost_inr: float
    total_prolongation_cost_inr: float
    ld_liability_shielded_inr: float
    applicable_clause: ContractClause
