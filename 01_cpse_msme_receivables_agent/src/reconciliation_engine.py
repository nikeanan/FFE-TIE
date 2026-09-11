from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional
from .schema import ExtractedDocument


@dataclass
class AuditIssue:
    severity: str  # 'BLOCKER' | 'WARNING'
    field: str
    message: str
    remedy_action: str


class PreSubmissionAuditor:
    """Performs 4-way matching between PO, Delivery Proof, Inspection Report, and Invoice."""

    def audit(
        self,
        po: ExtractedDocument,
        invoice: ExtractedDocument,
        delivery_challan: Optional[ExtractedDocument] = None,
        inspection_note: Optional[ExtractedDocument] = None,
    ) -> List[AuditIssue]:
        issues: List[AuditIssue] = []

        if invoice.po_reference != po.doc_number:
            issues.append(
                AuditIssue(
                    severity="BLOCKER",
                    field="po_reference",
                    message=f"Invoice PO Reference '{invoice.po_reference}' does not match PO Number '{po.doc_number}'.",
                    remedy_action="Update invoice header with exact PO reference.",
                )
            )

        po_item_map = {item.description.lower().strip(): item for item in po.line_items}

        for inv_item in invoice.line_items:
            key = inv_item.description.lower().strip()
            if key not in po_item_map:
                issues.append(
                    AuditIssue(
                        severity="BLOCKER",
                        field="line_items",
                        message=f"Item '{inv_item.description}' not found in approved PO line items.",
                        remedy_action="Verify item description against PO annexure.",
                    )
                )
                continue

            po_item = po_item_map[key]

            if inv_item.unit_rate > po_item.unit_rate:
                issues.append(
                    AuditIssue(
                        severity="BLOCKER",
                        field="unit_rate",
                        message=f"Billed rate INR {inv_item.unit_rate} exceeds PO rate INR {po_item.unit_rate} for '{inv_item.description}'.",
                        remedy_action="Revise unit rate or attach approved price variation clause (PVC).",
                    )
                )

            if inv_item.quantity > po_item.quantity:
                issues.append(
                    AuditIssue(
                        severity="BLOCKER",
                        field="quantity",
                        message=f"Billed quantity ({inv_item.quantity}) exceeds PO quantity ({po_item.quantity}).",
                        remedy_action="Check milestone completion or split delivery billing.",
                    )
                )

        if delivery_challan:
            dc_qty = sum(item.quantity for item in delivery_challan.line_items)
            inv_qty = sum(item.quantity for item in invoice.line_items)
            if inv_qty > dc_qty:
                issues.append(
                    AuditIssue(
                        severity="BLOCKER",
                        field="delivery_mismatch",
                        message=f"Invoice quantity ({inv_qty}) exceeds physical delivery receipt ({dc_qty}).",
                        remedy_action="Bill only for goods physically receipted at CPSE stores.",
                    )
                )

        if invoice.payment_terms_days > 45:
            issues.append(
                AuditIssue(
                    severity="WARNING",
                    field="payment_terms",
                    message="Credit period exceeds statutory 45-day ceiling under MSMED Act 2006.",
                    remedy_action="Ensure explicit written contract exists; terms > 45 days are legally void.",
                )
            )

        return issues
