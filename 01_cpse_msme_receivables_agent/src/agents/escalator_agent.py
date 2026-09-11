from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from ..database.db_session import db
from ..database.models import Invoice, InvoiceLifecycleStatus
from ..integrations.samadhaan_adapter import samadhaan
from ..integrations.whatsapp_adapter import whatsapp
from ..msmed_compliance import MSMEDInterestCalculator


class EscalationStep(BaseModel):
    step_number: int
    action_code: str
    action_name: str
    relationship_risk: str  # LOW | MEDIUM | HIGH
    typical_effectiveness: float
    requires_human_approval: bool
    description: str


class EscalationRecommendation(BaseModel):
    invoice_id: str
    invoice_number: str
    buyer_name: str
    days_overdue: int
    principal_amount: Decimal
    accrued_interest: Decimal
    total_claimable: Decimal
    recommended_step: EscalationStep
    relationship_value_score: str  # LOW | MEDIUM | HIGH
    human_approval_status: str     # PENDING_HUMAN_APPROVAL | AUTO_APPROVED | EXECUTED
    escalation_content: str
    whatsapp_prompt: Optional[str] = None


class EscalatorAgent:
    """Rights-Enforcement Engine: Translates statutory legal leverage into automated recovery."""

    ESCALATION_LADDER = [
        EscalationStep(
            step_number=1,
            action_code="SENIOR_CONTACT_EMAIL",
            action_name="Senior Officer Polite Inquiry",
            relationship_risk="LOW",
            typical_effectiveness=0.35,
            requires_human_approval=False,
            description="Polite note addressed to Department Head citing mutual partnership and request for clearance.",
        ),
        EscalationStep(
            step_number=2,
            action_code="INTEREST_MEMO",
            action_name="Statutory MSMED Interest Calculation Statement",
            relationship_risk="LOW",
            typical_effectiveness=0.45,
            requires_human_approval=False,
            description="Certified calculation memo showing daily compounding interest accumulating at 3x RBI Bank Rate.",
        ),
        EscalationStep(
            step_number=3,
            action_code="FORMAL_DEMAND_NOTICE",
            action_name="Statutory Demand Notice (MSMED Act §15/16)",
            relationship_risk="MEDIUM",
            typical_effectiveness=0.60,
            requires_human_approval=True,
            description="Executive legal demand giving 7 working days to settle or accept on TReDS before statutory filing.",
        ),
        EscalationStep(
            step_number=4,
            action_code="SAMADHAAN_FILING",
            action_name="MSME Samadhaan (MSEFC) Formal Petition",
            relationship_risk="MEDIUM",
            typical_effectiveness=0.70,
            requires_human_approval=True,
            description="Fully assembled arbitration/conciliation claim dossier ready for digital submission to Facilitation Council.",
        ),
        EscalationStep(
            step_number=5,
            action_code="43BH_CFO_NOTICE",
            action_name="Section 43B(h) Audit & Tax Disallowance Notice",
            relationship_risk="HIGH",
            typical_effectiveness=0.80,
            requires_human_approval=True,
            description="Formal communication to CPSE CFO and statutory auditors alerting to mandatory tax disallowance under Income Tax Act.",
        ),
    ]

    @classmethod
    def calculate_dues(cls, invoice: Invoice, as_of: Optional[date] = None) -> Dict[str, Any]:
        """Computes MSMED Section 16 penal compound interest with monthly rests at 3x RBI Bank Rate."""
        calc = MSMEDInterestCalculator(rbi_bank_rate_annual=Decimal("0.065"))
        inv_date = invoice.invoice_date
        return calc.calculate_dues(
            principal=invoice.amount,
            invoice_date=inv_date,
            payment_due_days=45,
            as_of_date=as_of or date.today(),
        )

    @classmethod
    def estimate_future_business(cls, msme_id: str, buyer_id: str) -> str:
        """Estimates forward pipeline value from PO history and open tenders."""
        # Check PO count
        pos = [p for p in db.pos.values() if p.msme_id == msme_id and p.buyer_id == buyer_id]
        if len(pos) >= 3:
            return "HIGH"
        elif len(pos) >= 1:
            return "MEDIUM"
        return "LOW"

    @classmethod
    def recommend_escalation(cls, invoice_id: str) -> EscalationRecommendation:
        inv = db.get_invoice(invoice_id)
        if not inv:
            raise ValueError(f"Invoice {invoice_id} not found")

        msme = db.get_msme(inv.msme_id)
        buyer = db.get_buyer(inv.buyer_id)
        buyer_name = buyer.name if buyer else "CPSE Buyer"

        dues = cls.calculate_dues(inv)
        days_overdue = dues["days_overdue"]
        rel_value = cls.estimate_future_business(inv.msme_id, inv.buyer_id)

        # Decide step based on overdue duration and relationship risk
        if days_overdue >= 90 and rel_value == "LOW":
            target_step_idx = 4  # Step 5: 43B(h) CFO notice
        elif days_overdue >= 60:
            target_step_idx = 3  # Step 4: Samadhaan Filing
        elif days_overdue >= 30:
            target_step_idx = 2  # Step 3: Formal Demand Notice
        elif days_overdue >= 15:
            target_step_idx = 1  # Step 2: Interest Memo
        else:
            target_step_idx = 0  # Step 1: Senior Contact Email

        step = cls.ESCALATION_LADDER[target_step_idx]

        # Generate specific document draft
        doc_content = cls._generate_document_for_step(
            step=step,
            msme=msme,
            buyer=buyer,
            invoice=inv,
            dues=dues,
        )

        approval_status = "PENDING_HUMAN_APPROVAL" if step.requires_human_approval else "AUTO_APPROVED"

        # WhatsApp alert for human-in-the-loop gate
        wa_prompt = None
        if step.requires_human_approval:
            wa_prompt = (
                f"⚖️ *RECEIVX Escalator Recommendation:* Invoice {inv.invoice_number} ({buyer_name})\n"
                f"Status: *{days_overdue} days overdue* | Claimable Interest: *INR {dues['statutory_interest']:,.2f}*\n"
                f"Recommended Action: *Step {step.step_number} — {step.action_name}* (Risk: {step.relationship_risk})\n\n"
                f"Reply *APPROVE* to authorize digital dispatch, or *HOLD* to defer."
            )

        rec = EscalationRecommendation(
            invoice_id=inv.id,
            invoice_number=inv.invoice_number,
            buyer_name=buyer_name,
            days_overdue=days_overdue,
            principal_amount=dues["principal"],
            accrued_interest=dues["statutory_interest"],
            total_claimable=dues["total_claimable"],
            recommended_step=step,
            relationship_value_score=rel_value,
            human_approval_status=approval_status,
            escalation_content=doc_content,
            whatsapp_prompt=wa_prompt,
        )
        return rec

    @classmethod
    def execute_escalation_step(cls, invoice_id: str, step_number: int, actor: str = "MSME_USER") -> Dict[str, Any]:
        """Executes the approved escalation step and logs the audit event."""
        rec = cls.recommend_escalation(invoice_id)
        step = [s for s in cls.ESCALATION_LADDER if s.step_number == step_number][0]

        db.log_event(
            invoice_id=invoice_id,
            event_type=f"ESCALATION_STEP_{step.step_number}_EXECUTED",
            payload={
                "action_code": step.action_code,
                "action_name": step.action_name,
                "risk": step.relationship_risk,
                "claimed_principal": float(rec.principal_amount),
                "claimed_interest": float(rec.accrued_interest),
            },
            actor=actor,
        )

        return {
            "success": True,
            "step_executed": step.dict(),
            "message": f"Escalation Step {step.step_number} ({step.action_name}) executed successfully.",
            "document_preview": rec.escalation_content,
        }

    @classmethod
    def _generate_document_for_step(cls, step: EscalationStep, msme, buyer, invoice: Invoice, dues: Dict[str, Any]) -> str:
        msme_name = msme.legal_name if msme else "MSME Supplier"
        udyam = msme.udyam_number if msme else "UDYAM-REG-XX"
        buyer_name = buyer.name if buyer else "CPSE Buyer"
        nodal = buyer.nodal_officer if buyer else "General Manager (Finance)"
        days = dues["days_overdue"]
        principal = dues["principal"]
        interest = dues["statutory_interest"]
        total = dues["total_claimable"]

        if step.step_number == 1:
            return (
                f"Subject: Status of Overdue Supply Account — Invoice {invoice.invoice_number} — {msme_name}\n\n"
                f"To:\n{nodal},\n{buyer_name}\n\n"
                f"Dear Sir/Madam,\n\n"
                f"We value our long-standing association supplying quality components to {buyer_name}. "
                f"We respectfully bring to your kind attention that Tax Invoice No. {invoice.invoice_number} "
                f"dated {invoice.invoice_date.strftime('%d-%b-%Y')} for INR {principal:,.2f} is currently overdue by {days} days.\n\n"
                f"As a registered MSME entity (Udyam: {udyam}), timely working capital replenishment is vital for our manufacturing schedules. "
                f"We request your kind intervention to verify the clearance status.\n\n"
                f"Thank you,\nFinance & Accounts\n{msme_name}"
            )

        elif step.step_number == 2:
            return (
                f"MEMORANDUM: STATUTORY ACCRUED INTEREST STATEMENT UNDER SECTION 16 OF MSMED ACT, 2006\n"
                f"------------------------------------------------------------------------------------\n"
                f"Supplier: {msme_name} (Udyam: {udyam})\n"
                f"Buyer: {buyer_name}\n"
                f"Invoice Reference: {invoice.invoice_number} dated {invoice.invoice_date.strftime('%d-%b-%Y')}\n"
                f"Agreed Statutory Credit Ceiling: 45 Days\n"
                f"Days in Default Beyond Statutory Period: {days} Days\n\n"
                f"INTEREST COMPUTATION SUMMARY:\n"
                f"• Principal Outstanding Amount: INR {principal:,.2f}\n"
                f"• Applicable Statutory Rate: 3x RBI Bank Rate (19.5% p.a., compounded monthly)\n"
                f"• Total Compounded Penal Interest: INR {interest:,.2f}\n"
                f"• Current Total Amount Recoverable: INR {total:,.2f}\n\n"
                f"Note: Pursuant to Section 23 of the MSMED Act, this interest is NOT deductible from income for tax purposes by the buyer.\n"
                f"Date of Generation: {date.today().strftime('%d-%b-%Y')}"
            )

        elif step.step_number == 3:
            return (
                f"FORMAL DEMAND NOTICE BEFORE LEGAL PROCEEDINGS\n"
                f"UNDER SECTIONS 15, 16 & 17 OF THE MSMED ACT, 2006\n\n"
                f"To:\n{nodal},\n{buyer_name}\n\n"
                f"Subject: FINAL DEMAND FOR PAYMENT: Outstanding dues against Invoice {invoice.invoice_number} (PO: {invoice.po_number or 'PO-REF'})\n\n"
                f"Dear Sir/Madam,\n\n"
                f"1. You have defaulted on payment for supplies delivered under PO {invoice.po_number or 'PO-REF'} and billed under Invoice {invoice.invoice_number}.\n"
                f"2. The statutory period of 45 days mandated under Section 15 of the MSMED Act expired {days} days ago.\n"
                f"3. Outstanding Principal: INR {principal:,.2f} | Accrued Penal Interest: INR {interest:,.2f} | Total: INR {total:,.2f}.\n"
                f"4. TAKE NOTICE that unless the full amount is remitted or accepted on TReDS within SEVEN (7) WORKING DAYS of this notice, "
                f"we shall initiate arbitration proceedings before the Micro and Small Enterprises Facilitation Council (MSEFC) "
                f"and report non-compliance under Section 43B(h) of the Income Tax Act.\n\n"
                f"Authorized Signatory,\n{msme_name}"
            )

        elif step.step_number == 4:
            petition_data = samadhaan.generate_msefc_petition(
                msme=msme,
                buyer=buyer,
                invoice=invoice,
                statutory_interest=interest,
                days_overdue=days,
            )
            return petition_data["petition_text"]

        elif step.step_number == 5:
            return (
                f"STATUTORY TAX COMPLIANCE ALERT: SECTION 43B(h) OF THE INCOME TAX ACT, 1961\n"
                f"--------------------------------------------------------------------------\n"
                f"Addressed To: The Chief Financial Officer & Statutory Auditors\n"
                f"Entity: {buyer_name}\n\n"
                f"Dear Sir/Madam,\n\n"
                f"Re: Mandatory Disallowance of Expenditure on Overdue MSME Payables for FY 2025-26\n\n"
                f"This is an official compliance communication regarding outstanding dues owed to {msme_name} "
                f"(Udyam Registration: {udyam}) against Invoice {invoice.invoice_number} for INR {principal:,.2f}.\n\n"
                f"As per Section 43B(h) of the Income Tax Act, any sum payable to a micro or small enterprise beyond the time limit "
                f"specified in Section 15 of the MSMED Act (45 days) CANNOT be allowed as a tax deduction in computing taxable business profits "
                f"unless actually paid before the close of the financial year.\n\n"
                f"The invoice is currently {days} days overdue. Non-settlement exposes {buyer_name} to direct tax disallowance on INR {principal:,.2f}, "
                f"incurring corporate tax and interest penalties during statutory tax audit.\n\n"
                f"We urge immediate clearance or TReDS discounting approval.\n\n"
                f"Head of Tax & Legal Compliance\n{msme_name}"
            )

        return "Standard communication notice."


escalator_agent = EscalatorAgent()
