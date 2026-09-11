from datetime import date
from decimal import Decimal


class ActionDraftAgent:
    """Generates legally structured, executive notices tailored for CPSE finance & project officers."""

    @staticmethod
    def generate_msmed_statutory_notice(
        supplier_name: str,
        supplier_udyam_reg: str,
        cpse_name: str,
        cpse_officer_designation: str,
        invoice_no: str,
        invoice_date: date,
        po_no: str,
        principal_amt: Decimal,
        interest_amt: Decimal,
        days_overdue: int,
    ) -> str:
        return f"""
FORMAL DEMAND NOTICE: SETTLEMENT OF OVERDUE RECEIVABLES UNDER MSMED ACT, 2006

To,
The {cpse_officer_designation},
{cpse_name}

Subject: Urgent settlement of outstanding dues against Invoice No. {invoice_no} (PO: {po_no})
Udyam Registration No.: {supplier_udyam_reg}

Dear Sir/Madam,

This is with reference to supply delivered against Purchase Order No. {po_no}, billed under Tax Invoice No. {invoice_no} dated {invoice_date.strftime('%d-%b-%Y')} for the amount of INR {principal_amt:,.2f}.

1. STATUTORY TIMELINE BREACH:
As per Section 15 of the Micro, Small and Medium Enterprises Development (MSMED) Act, 2006, payment was due within 45 days from the date of acceptance. The invoice is currently overdue by {days_overdue} days.

2. ACCRUED STATUTORY INTEREST:
Pursuant to Section 16 of the MSMED Act, failure to make payment within the statutory timeline attracts compound interest with monthly rests at 3 times the RBI bank rate.
- Principal Outstanding: INR {principal_amt:,.2f}
- Accumulated Interest (MSMED Sec 16): INR {interest_amt:,.2f}
- Total Amount Payable: INR {(principal_amt + interest_amt):,.2f}

3. TAX DISALLOWANCE NOTICE (SECTION 43B(h)):
Please note that pursuant to Section 43B(h) of the Income Tax Act, overdue payments to MSMEs cannot be claimed as a deductible business expense unless paid within the statutory period.

We request you to expedite the release of payment or approve the invoice on the designated TReDS platform (RXIL/M1xchange/Invoicemart) within 7 working days to avoid formal filing before the MSME Micro and Small Enterprises Facilitation Council (MSEFC).

Sincerely,
Finance & Accounts Department
{supplier_name}
"""
