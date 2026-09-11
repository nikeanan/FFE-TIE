from datetime import date, timedelta
from decimal import Decimal
from typing import Any, Dict, Optional
from ..database.models import Invoice, PurchaseOrder, GoodsReceiptNote


class GeMCRACTracker:
    """Tracks GeM (Government e-Marketplace) Consignee Receipt and Acceptance Certificate (CRAC)
    timelines under Rule 149 of the General Financial Rules (GFR), 2017.
    
    Rule 149 Mandate:
      - Consignee must generate CRAC within 10 days of physical receipt.
      - If not generated within 10 days, the invoice is legally DEEMED ACCEPTED by the system.
      - Payment must be released within 10 days of CRAC generation / deemed acceptance.
    """

    STATUTORY_CRAC_WINDOW_DAYS = 10
    STATUTORY_PAYMENT_WINDOW_DAYS = 10

    @classmethod
    def evaluate_gem_milestone(
        cls,
        invoice_number: str,
        delivery_date: date,
        crac_generated: bool = False,
        crac_date: Optional[date] = None,
        as_of_date: Optional[date] = None,
    ) -> Dict[str, Any]:
        check_date = as_of_date or date.today()
        deemed_crac_date = delivery_date + timedelta(days=cls.STATUTORY_CRAC_WINDOW_DAYS)
        days_since_delivery = (check_date - delivery_date).days

        if crac_generated and crac_date:
            final_payment_due_date = crac_date + timedelta(days=cls.STATUTORY_PAYMENT_WINDOW_DAYS)
            is_payment_overdue = check_date > final_payment_due_date
            return {
                "invoice_number": invoice_number,
                "status": "CRAC_ISSUED",
                "crac_date": crac_date.isoformat(),
                "deemed_crac_applied": False,
                "payment_due_date": final_payment_due_date.isoformat(),
                "is_payment_overdue": is_payment_overdue,
                "days_overdue": max(0, (check_date - final_payment_due_date).days),
                "action_recommended": "MONITOR_PAYMENT" if not is_payment_overdue else "ESCALATE_PAYMENT_DEFAULT",
            }

        # CRAC not yet manually generated
        if check_date >= deemed_crac_date:
            # Rule 149 Deemed Acceptance active!
            final_payment_due_date = deemed_crac_date + timedelta(days=cls.STATUTORY_PAYMENT_WINDOW_DAYS)
            is_payment_overdue = check_date > final_payment_due_date
            days_overdue = max(0, (check_date - final_payment_due_date).days)
            
            return {
                "invoice_number": invoice_number,
                "status": "DEEMED_CRAC_AUTO_ACCEPTED",
                "crac_date": deemed_crac_date.isoformat(),
                "deemed_crac_applied": True,
                "days_since_delivery": days_since_delivery,
                "payment_due_date": final_payment_due_date.isoformat(),
                "is_payment_overdue": is_payment_overdue,
                "days_overdue": days_overdue,
                "action_recommended": "ISSUE_RULE_149_DEMAND_NOTICE" if is_payment_overdue else "NOTIFY_DEEMED_ACCEPTANCE",
                "statutory_rule_citation": "Rule 149 of General Financial Rules (GFR) 2017 & GeM Terms of Service Clause 12",
            }
        else:
            days_remaining_for_crac = (deemed_crac_date - check_date).days
            return {
                "invoice_number": invoice_number,
                "status": "CRAC_PENDING_CONSIGNEE",
                "crac_date": None,
                "deemed_crac_applied": False,
                "days_since_delivery": days_since_delivery,
                "days_until_auto_crac": days_remaining_for_crac,
                "payment_due_date": (deemed_crac_date + timedelta(days=cls.STATUTORY_PAYMENT_WINDOW_DAYS)).isoformat(),
                "is_payment_overdue": False,
                "days_overdue": 0,
                "action_recommended": "SOFT_REMINDER_TO_CONSIGNEE",
                "statutory_rule_citation": "Rule 149 GFR (10-day Consignee Verification Period)",
            }

    @classmethod
    def generate_rule_149_demand_notice(
        cls,
        supplier_name: str,
        supplier_udyam: str,
        buyer_entity: str,
        consignee_designation: str,
        gem_contract_no: str,
        invoice_no: str,
        invoice_amount: Decimal,
        delivery_date: date,
        days_overdue: int,
    ) -> str:
        deemed_date = delivery_date + timedelta(days=10)
        return f"""
FORMAL STATUTORY NOTICE: MANDATORY PAYMENT RELEASE UNDER RULE 149 OF GFR, 2017
(GeM Portal Contract Ref: {gem_contract_no} | Invoice No: {invoice_no})

To,
The {consignee_designation},
{buyer_entity}

From:
{supplier_name}
(Udyam Registration No.: {supplier_udyam})

Subject: Deemed CRAC Acceptance & Immediate Release of Payment for Goods Delivered against GeM Contract {gem_contract_no}

Respected Sir/Madam,

We invite your urgent reference to the supply of contracted materials successfully delivered at your consignee stores on {delivery_date.strftime('%d-%b-%Y')} against GeM Contract No. {gem_contract_no}, billed under Tax Invoice No. {invoice_no} for INR {invoice_amount:,.2f}.

1. STATUTORY DEEMED ACCEPTANCE (RULE 149 OF GFR, 2017):
Pursuant to Rule 149 of the General Financial Rules (GFR) 2017 and GeM Special Terms and Conditions Clause 12, the Consignee Receipt and Acceptance Certificate (CRAC) was required to be issued within 10 calendar days of physical delivery. As no formal rejection was logged on or before {deemed_date.strftime('%d-%b-%Y')}, the supplies stand legally and automatically DEEMED ACCEPTED by operation of law.

2. PAYMENT DEFAULT & MSMED STATUTORY TIMELINE:
Under GeM payment rules and Section 15 of the MSMED Act, 2006, payment was mandatory within 10 days of deemed CRAC generation. The payment is currently in default and OVERDUE by {days_overdue} days.

3. ACCRUAL OF PENAL INTEREST & SECTION 43B(h) TAX CONSEQUENCE:
Continued delay attracts compound penal interest at 3x the RBI Bank Rate under Section 16 of the MSMED Act, and exposes your organization to tax deduction disallowances under Section 43B(h) of the Income Tax Act.

We request you to authorize the online disbursement of INR {invoice_amount:,.2f} on the GeM portal / PFMS within 48 hours to avert formal escalation before the Ministry of Finance and the MSME Facilitation Council.

Yours faithfully,
For {supplier_name}
Authorized Signatory
"""


gem_tracker = GeMCRACTracker()
gem_crac_engine = gem_tracker
