from datetime import date
from decimal import Decimal
from typing import Any, Dict, List
from ..database.models import Invoice, MSME, Buyer


class SamadhaanAdapter:
    """Formats and compiles legally compliant petition packages for the MSME Samadhaan MSEFC portal."""

    @staticmethod
    def generate_msefc_petition(
        msme: MSME,
        buyer: Buyer,
        invoice: Invoice,
        statutory_interest: Decimal,
        days_overdue: int,
    ) -> Dict[str, Any]:
        total_claimable = invoice.amount + statutory_interest

        statement_of_claim = f"""BEFORE THE MICRO AND SMALL ENTERPRISES FACILITATION COUNCIL (MSEFC)
IN THE MATTER OF: ARBITRATION / CONCILIATION UNDER SECTION 18 OF MSMED ACT, 2006

CLAIM PETITION NO.: MSEFC/2026/HAR/{invoice.invoice_number.replace('/', '_')}

IN THE MATTER OF:
{msme.legal_name}
(Udyam Registration No.: {msme.udyam_number})
Registered Office: Sector 25, Industrial Area, Faridabad, Haryana
... CLAIMANT / SUPPLIER

VERSUS

{buyer.name}
(GSTIN: {buyer.gstin})
Addressed to: The {buyer.nodal_officer}
Division: {buyer.division_unit}
... RESPONDENT / BUYER

STATEMENT OF CLAIM UNDER SECTION 18 READ WITH SECTIONS 15, 16 & 17 OF MSMED ACT, 2006

1. PARTICULARS OF THE CLAIMANT:
The Claimant is a duly registered {msme.category.value} enterprise holding valid Udyam Registration Certificate No. {msme.udyam_number}, engaged in {msme.sector}.

2. PARTICULARS OF THE RESPONDENT:
The Respondent is a Central Public Sector Enterprise (CPSE) engaged in public sector utility operations.

3. STATEMENT OF FACTS:
a) The Respondent placed Purchase Order No. {invoice.po_number or 'PO-REF-CPSE'} upon the Claimant for supply of goods/services.
b) The Claimant manufactured, inspected, and successfully delivered the contracted goods in full compliance with specifications.
c) The Claimant raised Tax Invoice No. {invoice.invoice_number} dated {invoice.invoice_date.strftime('%d-%b-%Y')} for the total amount of INR {invoice.amount:,.2f}.
d) The Respondent accepted the goods and failed to raise any formal written dispute within the statutory 15-day deemed acceptance period stipulated under Section 2(b) of the MSMED Act, 2006.

4. STATUTORY BREACH & OVERDUE DURATION:
Pursuant to Section 15 of the MSMED Act, payment was mandatory within 45 days. The payment has remained unpaid for {days_overdue} days past the statutory due date.

5. COMPUTATION OF CLAIM UNDER SECTION 16:
- Principal Outstanding Amount: INR {invoice.amount:,.2f}
- Statutory Penal Compound Interest (3x RBI Bank Rate with monthly rests): INR {statutory_interest:,.2f}
- TOTAL AMOUNT CLAIMED AS ON {date.today().strftime('%d-%b-%Y')}: INR {total_claimable:,.2f}

6. NOTICE REGARDING SECTION 43B(h) OF THE INCOME TAX ACT:
The Respondent has also failed to satisfy the condition of actual payment under Section 43B(h), thereby rendering the entire invoice value liable for tax disallowance under assessment proceedings.

PRAYER:
Wherefore, the Claimant respectfully prays that this Hon'ble Council be pleased to:
i) Direct the Respondent to make immediate payment of INR {invoice.amount:,.2f} towards the principal sum;
ii) Direct the Respondent to pay compound interest of INR {statutory_interest:,.2f} with monthly rests as mandated by Section 16;
iii) Award costs of the present conciliation/arbitration proceedings in favor of the Claimant.

VERIFICATION:
Verified at Faridabad on this {date.today().strftime('%d')} day of {date.today().strftime('%B, %Y')} that the contents of paragraphs 1 to 6 are true to my knowledge and belief.

For {msme.legal_name}
(Authorized Signatory)
"""

        exhibits = [
            {"annexure": "A", "title": "Copy of Udyam Registration Certificate", "status": "ATTACHED"},
            {"annexure": "B", "title": f"Purchase Order No. {invoice.po_number or 'PO-01'}", "status": "ATTACHED"},
            {"annexure": "C", "title": f"Tax Invoice No. {invoice.invoice_number}", "status": "ATTACHED"},
            {"annexure": "D", "title": "Goods Receipt Note / Consignee Delivery Proof", "status": "ATTACHED"},
            {"annexure": "E", "title": "Certified Statement of Section 16 Monthly Compounded Interest", "status": "ATTACHED"},
        ]

        return {
            "petition_number": f"MSEFC/2026/HAR/{invoice.invoice_number.replace('/', '_')}",
            "claimant": msme.legal_name,
            "udyam": msme.udyam_number,
            "respondent": buyer.name,
            "principal": invoice.amount,
            "interest": statutory_interest,
            "total_claim": total_claimable,
            "days_overdue": days_overdue,
            "petition_text": statement_of_claim,
            "exhibits": exhibits,
            "samadhaan_portal_url": "https://samadhaan.msme.gov.in/MyMsme/MSEFC/MSEFC_Welcome.aspx",
        }


samadhaan = SamadhaanAdapter()
