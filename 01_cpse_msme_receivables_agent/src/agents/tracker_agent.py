from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from ..database.db_session import db
from ..database.models import BuyerLearnedRule, FlagSeverity, Invoice, InvoiceLifecycleStatus


class ActionType(str, Enum):
    WAIT = "WAIT"
    SOFT_NUDGE = "SOFT_NUDGE"
    FORMAL_REMINDER = "FORMAL_REMINDER"
    ESCALATE_TO_AGENT_3 = "ESCALATE_TO_AGENT_3"


class TrackerAction(BaseModel):
    type: ActionType
    channel: str = "EMAIL"
    template: Optional[str] = None
    cc: List[str] = []
    cite: List[str] = []
    message_content: Optional[str] = None
    days_pending: int = 0
    t1_threshold: int = 3
    t2_threshold: int = 7
    t3_threshold: int = 12


class TrackerPolicy:
    """Adaptive follow-up cadence per buyer, learned from what actually moves each buyer unit."""

    @classmethod
    def next_action(cls, invoice: Invoice) -> TrackerAction:
        ref_date = invoice.submitted_date or invoice.invoice_date
        days_pending = (date.today() - ref_date).days

        buyer_stats = db.get_buyer_stats(invoice.buyer_id)
        avg_acc = buyer_stats.avg_acceptance_days if buyer_stats else 14.0

        # Dynamic thresholds: act at 60% of this buyer's median, not fixed days
        t1 = max(3, int(avg_acc * 0.6))
        t2 = max(7, int(avg_acc * 1.0))
        t3 = max(12, int(avg_acc * 1.5))

        channel = buyer_stats.most_effective_channel if buyer_stats else "EMAIL_FINANCE_HEAD"
        cc_contacts = buyer_stats.escalation_contacts if buyer_stats else []

        buyer = db.get_buyer(invoice.buyer_id)
        buyer_name = buyer.name if buyer else "CPSE Buyer"

        if days_pending >= t3:
            return TrackerAction(
                type=ActionType.ESCALATE_TO_AGENT_3,
                channel=channel,
                days_pending=days_pending,
                t1_threshold=t1,
                t2_threshold=t2,
                t3_threshold=t3,
                message_content=(
                    f"Invoice {invoice.invoice_number} pending for {days_pending} days without acceptance "
                    f"(exceeds 150% threshold of {t3} days). Handoff to Agent 3 (Escalator) initiated."
                ),
            )

        if days_pending >= t2:
            msg = (
                f"Subject: URGENT: Acceptance status for Invoice {invoice.invoice_number} (PO: {invoice.po_number or 'PO-REF'}) - Statutory Citations\n\n"
                f"Dear Accounts Officer,\n\n"
                f"Our Tax Invoice No. {invoice.invoice_number} dated {invoice.invoice_date.strftime('%d-%b-%Y')} "
                f"for INR {invoice.amount:,.2f} has been pending acceptance for {days_pending} days at {buyer_name}.\n\n"
                f"Please note statutory guidelines:\n"
                f"1. Under Section 2(b) of the MSMED Act, 2006, deemed acceptance takes effect after 15 days unless a formal dispute is submitted in writing.\n"
                f"2. Section 43B(h) of the Income Tax Act disallows expense deductions if payment exceeds 45 days.\n\n"
                f"Kindly expedite formal portal acceptance or advise any documentation clarification."
            )
            return TrackerAction(
                type=ActionType.FORMAL_REMINDER,
                channel=channel,
                template="reminder_with_statutory_cite",
                cc=cc_contacts,
                cite=["MSMED Act §15 (45-day rule)", "MSMED Act §2(b) (15-day deemed acceptance)", "IT Act §43B(h)"],
                message_content=msg,
                days_pending=days_pending,
                t1_threshold=t1,
                t2_threshold=t2,
                t3_threshold=t3,
            )

        if days_pending >= t1:
            msg = (
                f"Subject: Status check: Invoice {invoice.invoice_number} submitted to {buyer_name}\n\n"
                f"Dear Team,\n\n"
                f"Gentle follow-up regarding invoice verification for {invoice.invoice_number} (PO: {invoice.po_number or 'PO-REF'}), "
                f"submitted on {ref_date.strftime('%d-%b-%Y')}. Please confirm if store GRN reconciliation is complete.\n\n"
                f"Thank you,\nFinance Team"
            )
            return TrackerAction(
                type=ActionType.SOFT_NUDGE,
                channel=channel,
                template="polite_status_query",
                days_pending=days_pending,
                t1_threshold=t1,
                t2_threshold=t2,
                t3_threshold=t3,
                message_content=msg,
            )

        return TrackerAction(
            type=ActionType.WAIT,
            days_pending=days_pending,
            t1_threshold=t1,
            t2_threshold=t2,
            t3_threshold=t3,
            message_content=f"Invoice is within standard processing window ({days_pending} days pending < T1 threshold of {t1} days).",
        )


class InboundEmailParser:
    """Parses buyer replies, extracts acceptance / query / rejection, and updates the buyer graph.
       'The agents teach each other.'"""

    @classmethod
    def process_buyer_email(cls, from_email: str, subject: str, body: str) -> Dict[str, Any]:
        body_lower = body.lower()

        # Find referenced invoice
        matched_invoice = None
        for inv in db.list_invoices():
            clean_no = inv.invoice_number.replace("/", "").replace("-", "").lower()
            if clean_no in body.replace("/", "").replace("-", "").lower() or inv.invoice_number.lower() in body_lower:
                matched_invoice = inv
                break

        if not matched_invoice:
            # Fallback to first invoice for simulation
            matched_invoice = db.list_invoices()[0]

        extracted_status = "UNKNOWN"
        reason = None

        if any(w in body_lower for w in ["accepted", "approved", "processed for payment", "passed for payment"]):
            extracted_status = "ACCEPTED"
            matched_invoice.status = InvoiceLifecycleStatus.ACCEPTED
            matched_invoice.acceptance_date = date.today()
            db.log_event(
                invoice_id=matched_invoice.id,
                event_type="BUYER_REPLY_ACCEPTED",
                payload={"subject": subject, "from": from_email},
                actor="AGENT_TRACKER_EMAIL_PARSER",
            )
        elif any(w in body_lower for w in ["rejected", "returned", "discrepancy", "correction required", "mismatch"]):
            extracted_status = "REJECTED"
            matched_invoice.status = InvoiceLifecycleStatus.DISPUTED

            # Extract reason
            if "vendor code" in body_lower:
                reason = "Vendor code absent in billing header"
            elif "quantity" in body_lower or "grn" in body_lower:
                reason = "Quantity billed exceeds store physical GRN"
            elif "stamp" in body_lower or "inspection" in body_lower:
                reason = "Inspection certificate missing QA stamp"
            else:
                reason = "General billing documentation discrepancy"

            # FEED BACK INTO BUYER GRAPH ("THE MOAT") -> Agents teach each other!
            new_rule = BuyerLearnedRule(
                id=f"rule_learned_{len(db.buyer_rules.get(matched_invoice.buyer_id, [])) + 1}",
                buyer_id=matched_invoice.buyer_id,
                rule_code=f"LEARNED_{extracted_status}_{len(db.buyer_rules.get(matched_invoice.buyer_id, [])) + 1}",
                rule_name="Auto-mined Buyer Rejection Pattern",
                human_reason=f"Parsed from buyer email: '{reason}'. Auto-injected to prevent future rejections.",
                severity=FlagSeverity.BLOCKER,
                rejection_count=1,
                check_type="PARSED_EMAIL_PATTERN",
            )
            db.save_buyer_rule(new_rule)

            db.log_event(
                invoice_id=matched_invoice.id,
                event_type="BUYER_REPLY_REJECTED",
                payload={"subject": subject, "extracted_reason": reason, "new_learned_rule": new_rule.dict()},
                actor="AGENT_TRACKER_EMAIL_PARSER",
            )

        return {
            "invoice_id": matched_invoice.id,
            "invoice_number": matched_invoice.invoice_number,
            "detected_status": extracted_status,
            "extracted_reason": reason,
            "learned_pattern_injected": reason is not None,
        }


class TrackerAgent:
    """Acceptance Velocity Engine executing adaptive follow-up cadences and email feedback loops."""

    @classmethod
    def evaluate_invoice(cls, invoice_id: str) -> TrackerAction:
        inv = db.get_invoice(invoice_id)
        if not inv:
            return TrackerAction(type=ActionType.WAIT, message_content="Invoice not found")

        action = TrackerPolicy.next_action(inv)

        # Log event
        db.log_event(
            invoice_id=invoice_id,
            event_type=f"TRACKER_{action.type.value}",
            payload=action.dict(),
            actor="AGENT_TRACKER",
        )

        return action

    @classmethod
    def run_daily_tick(cls) -> List[Dict[str, Any]]:
        """Durable workflow evaluation tick across all pending invoices."""
        results = []
        for inv in db.list_invoices():
            if inv.status in [InvoiceLifecycleStatus.SUBMITTED, InvoiceLifecycleStatus.DRAFT]:
                act = cls.evaluate_invoice(inv.id)
                results.append({
                    "invoice_id": inv.id,
                    "invoice_number": inv.invoice_number,
                    "buyer_id": inv.buyer_id,
                    "action": act.type.value,
                    "days_pending": act.days_pending,
                })
        return results


tracker_agent = TrackerAgent()
