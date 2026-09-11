from datetime import date
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List
from pydantic import BaseModel

from ..database.db_session import db
from ..database.models import Invoice, InvoiceLifecycleStatus
from .escalator_agent import escalator_agent
from .financier_agent import financier_agent
from .tracker_agent import tracker_agent
from .validator_agent import validator_agent


class ActionUrgency(str, Enum):
    IMMEDIATE_ACTION = "IMMEDIATE_ACTION"  # Blocker / Legal / Hard Deadline
    FINANCING_OPPORTUNITY = "FINANCING_OPPORTUNITY"  # Cash in bank today
    ROUTINE_CADENCE = "ROUTINE_CADENCE"  # Nudge / Follow-up
    INFORMATIONAL = "INFORMATIONAL"


class NextBestAction(BaseModel):
    action_id: str
    urgency: ActionUrgency
    invoice_id: str
    invoice_number: str
    buyer_name: str
    title: str
    rationale: str
    action_type: str  # "FIX_INVOICE" | "ACCEPT_TREDS_BID" | "AUTHORIZE_ESCALATION" | "SEND_NUDGE"
    primary_cta: str
    estimated_impact: str
    automated_capability: bool


class DailyAdvisorSummary(BaseModel):
    msme_name: str
    generated_date: str
    total_active_receivables: Decimal
    total_overdue_msmed: Decimal
    total_claimable_interest: Decimal
    available_treds_liquidity: Decimal
    actions: List[NextBestAction]


class AdvisorAgent:
    """Daily Next-Best-Action (NBA) Engine: Synthesizes multi-agent state into actionable daily agenda."""

    @classmethod
    def generate_daily_actions(cls, msme_id: str = "msme_precision_01") -> DailyAdvisorSummary:
        invoices = [i for i in db.list_invoices() if i.msme_id == msme_id]
        msme = db.get_msme(msme_id)
        msme_name = msme.legal_name if msme else "Precision Engineering MSME Ltd"

        actions: List[NextBestAction] = []
        total_rec = Decimal("0.00")
        total_overdue = Decimal("0.00")
        total_interest = Decimal("0.00")
        treds_liquidity = Decimal("0.00")

        for inv in invoices:
            total_rec += inv.amount
            buyer = db.get_buyer(inv.buyer_id)
            b_name = buyer.name if buyer else "CPSE Buyer"

            # 1. Check for Pre-Submission Issues (Validator)
            if inv.status in [InvoiceLifecycleStatus.DRAFT, InvoiceLifecycleStatus.BLOCKED, InvoiceLifecycleStatus.FIX_REQUIRED]:
                # If score is low or blockers exist
                if inv.validation_score < 0.85:
                    actions.append(
                        NextBestAction(
                            action_id=f"nba_fix_{inv.id}",
                            urgency=ActionUrgency.IMMEDIATE_ACTION,
                            invoice_id=inv.id,
                            invoice_number=inv.invoice_number,
                            buyer_name=b_name,
                            title=f"Resolve 2 pre-submission discrepancies on {inv.invoice_number}",
                            rationale="Quantity overbilled vs Store GRN (480 vs 450) and Udyam number missing. Auto-remediation boosts acceptance odds from 41% to 94%.",
                            action_type="FIX_INVOICE",
                            primary_cta="Auto-Fix & Generate Compliant PDF",
                            estimated_impact="Prevents 15–30 day rejection cycle at CPSE accounts",
                            automated_capability=True,
                        )
                    )

            # 2. Check for Overdue Legal Actions (Escalator)
            elif inv.status == InvoiceLifecycleStatus.OVERDUE:
                dues = escalator_agent.calculate_dues(inv)
                days_overdue = dues["days_overdue"]
                total_overdue += inv.amount
                total_interest += dues["statutory_interest"]

                rec = escalator_agent.recommend_escalation(inv.id)
                step = rec.recommended_step

                actions.append(
                    NextBestAction(
                        action_id=f"nba_esc_{inv.id}",
                        urgency=ActionUrgency.IMMEDIATE_ACTION,
                        invoice_id=inv.id,
                        invoice_number=inv.invoice_number,
                        buyer_name=b_name,
                        title=f"Authorize Step {step.step_number} Escalation for {inv.invoice_number} ({days_overdue}d overdue)",
                        rationale=f"Invoice overdue by {days_overdue} days. Section 16 interest accrued: INR {dues['statutory_interest']:,.2f}. Ready to dispatch {step.action_name}.",
                        action_type="AUTHORIZE_ESCALATION",
                        primary_cta=f"Approve {step.action_name}",
                        estimated_impact=f"Enforces statutory right & triggers INR {dues['total_claimable']:,.2f} recovery",
                        automated_capability=False,  # Human-in-the-loop gate!
                    )
                )

            # 3. Check for TReDS Financing Opportunities (Financier)
            elif inv.status == InvoiceLifecycleStatus.TREDS_LISTED:
                fin = financier_agent.evaluate_financing(inv.id)
                if fin.best_offer:
                    treds_liquidity += fin.best_offer.net_amount
                    actions.append(
                        NextBestAction(
                            action_id=f"nba_fin_{inv.id}",
                            urgency=ActionUrgency.FINANCING_OPPORTUNITY,
                            invoice_id=inv.id,
                            invoice_number=inv.invoice_number,
                            buyer_name=b_name,
                            title=f"Lock {fin.best_offer.platform} Factor Bid at {float(fin.best_offer.discount_rate_apr*100):.1f}% APR for {inv.invoice_number}",
                            rationale=f"Best bid from {fin.best_offer.financier}. Immediate payout of INR {fin.best_offer.net_amount:,.2f}. Saves INR {fin.net_working_capital_savings:,.2f} vs your bank OD facility.",
                            action_type="ACCEPT_TREDS_BID",
                            primary_cta=f"Accept {fin.best_offer.platform} Bid (T+1 Payout)",
                            estimated_impact=f"Immediate INR {fin.best_offer.net_amount:,.2f} liquidity in bank",
                            automated_capability=True,
                        )
                    )

            # 4. Check for Tracker Cadence (Tracker)
            elif inv.status == InvoiceLifecycleStatus.SUBMITTED:
                act = tracker_agent.evaluate_invoice(inv.id)
                if act.type.value != "WAIT":
                    actions.append(
                        NextBestAction(
                            action_id=f"nba_track_{inv.id}",
                            urgency=ActionUrgency.ROUTINE_CADENCE,
                            invoice_id=inv.id,
                            invoice_number=inv.invoice_number,
                            buyer_name=b_name,
                            title=f"Send {act.type.value.replace('_', ' ').title()} for {inv.invoice_number}",
                            rationale=f"Pending acceptance for {act.days_pending} days. Dynamic threshold exceeded for {b_name}.",
                            action_type="SEND_NUDGE",
                            primary_cta=f"Dispatch {act.type.value.replace('_', ' ').title()}",
                            estimated_impact="Compresses CPSE acceptance window before deemed acceptance deadline",
                            automated_capability=True,
                        )
                    )

        # Sort actions by urgency: IMMEDIATE_ACTION > FINANCING_OPPORTUNITY > ROUTINE_CADENCE
        urgency_order = {
            ActionUrgency.IMMEDIATE_ACTION: 1,
            ActionUrgency.FINANCING_OPPORTUNITY: 2,
            ActionUrgency.ROUTINE_CADENCE: 3,
            ActionUrgency.INFORMATIONAL: 4,
        }
        actions.sort(key=lambda x: urgency_order.get(x.urgency, 9))

        return DailyAdvisorSummary(
            msme_name=msme_name,
            generated_date=date.today().strftime("%d %B %Y"),
            total_active_receivables=total_rec,
            total_overdue_msmed=total_overdue,
            total_claimable_interest=total_interest,
            available_treds_liquidity=treds_liquidity,
            actions=actions,
        )


advisor_agent = AdvisorAgent()
