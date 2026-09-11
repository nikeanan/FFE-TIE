from datetime import date
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class ArtifactType(str, Enum):
    BOQ_ITEM = "BOQ_ITEM"
    DRAWING_REVISION = "DRAWING_REVISION"
    MEASUREMENT_BOOK_ENTRY = "MEASUREMENT_BOOK_ENTRY"
    SITE_PHOTO = "SITE_PHOTO"
    RFI_INSPECTION = "RFI_INSPECTION"
    CORRESPONDENCE_LETTER = "CORRESPONDENCE_LETTER"
    VARIATION_ORDER = "VARIATION_ORDER"


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
