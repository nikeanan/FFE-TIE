import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from decimal import Decimal
import pytest
from src.schema import DocumentType, ExtractedDocument, LineItem
from src.reconciliation_engine import PreSubmissionAuditor
from src.msmed_compliance import MSMEDInterestCalculator
from src.financing_optimizer import evaluate_treds_bid


def test_reconciliation_exact_match():
    po = ExtractedDocument(
        doc_type=DocumentType.PURCHASE_ORDER,
        doc_number="PO-100",
        doc_date=date(2026, 1, 1),
        buyer_gstin="07AAACN0255D1ZQ",
        buyer_name="NTPC",
        seller_gstin="06ABCDE1234F1Z5",
        seller_name="MSME Vendor",
        line_items=[
            LineItem(description="Flange", quantity=Decimal("10"), unit="NOS", unit_rate=Decimal("1000"), gst_rate=Decimal("18"), total_taxable=Decimal("10000"), total_amount=Decimal("11800"))
        ],
        total_amount=Decimal("11800"),
    )
    inv = ExtractedDocument(
        doc_type=DocumentType.TAX_INVOICE,
        doc_number="INV-100",
        doc_date=date(2026, 1, 15),
        buyer_gstin="07AAACN0255D1ZQ",
        buyer_name="NTPC",
        seller_gstin="06ABCDE1234F1Z5",
        seller_name="MSME Vendor",
        po_reference="PO-100",
        line_items=[
            LineItem(description="Flange", quantity=Decimal("10"), unit="NOS", unit_rate=Decimal("1000"), gst_rate=Decimal("18"), total_taxable=Decimal("10000"), total_amount=Decimal("11800"))
        ],
        total_amount=Decimal("11800"),
        payment_terms_days=45,
    )
    auditor = PreSubmissionAuditor()
    issues = auditor.audit(po=po, invoice=inv)
    assert len(issues) == 0


def test_reconciliation_rate_mismatch_blocker():
    po = ExtractedDocument(
        doc_type=DocumentType.PURCHASE_ORDER,
        doc_number="PO-100",
        doc_date=date(2026, 1, 1),
        buyer_gstin="07AAACN0255D1ZQ",
        buyer_name="NTPC",
        seller_gstin="06ABCDE1234F1Z5",
        seller_name="MSME Vendor",
        line_items=[
            LineItem(description="Flange", quantity=Decimal("10"), unit="NOS", unit_rate=Decimal("1000"), gst_rate=Decimal("18"), total_taxable=Decimal("10000"), total_amount=Decimal("11800"))
        ],
        total_amount=Decimal("11800"),
    )
    inv = ExtractedDocument(
        doc_type=DocumentType.TAX_INVOICE,
        doc_number="INV-100",
        doc_date=date(2026, 1, 15),
        buyer_gstin="07AAACN0255D1ZQ",
        buyer_name="NTPC",
        seller_gstin="06ABCDE1234F1Z5",
        seller_name="MSME Vendor",
        po_reference="PO-100",
        line_items=[
            LineItem(description="Flange", quantity=Decimal("10"), unit="NOS", unit_rate=Decimal("1200"), gst_rate=Decimal("18"), total_taxable=Decimal("12000"), total_amount=Decimal("14160"))
        ],
        total_amount=Decimal("14160"),
    )
    auditor = PreSubmissionAuditor()
    issues = auditor.audit(po=po, invoice=inv)
    assert len(issues) == 1
    assert issues[0].severity == "BLOCKER"
    assert issues[0].field == "unit_rate"


def test_msmed_interest_calculation():
    calc = MSMEDInterestCalculator(rbi_bank_rate_annual=Decimal("0.065"))
    dues = calc.calculate_dues(
        principal=Decimal("100000.00"),
        invoice_date=date(2026, 1, 1),
        as_of_date=date(2026, 4, 16),
    )
    assert dues["is_overdue"] is True
    assert dues["days_overdue"] == 60
    assert dues["statutory_interest"] > Decimal("0.00")
    assert dues["total_claimable"] > Decimal("100000.00")


def test_treds_financing_decision():
    res = evaluate_treds_bid(
        invoice_amount=Decimal("1000000.00"),
        days_to_maturity=45,
        treds_annual_discount_bid=Decimal("0.08"),
        msme_cc_od_annual_rate=Decimal("0.12"),
    )
    assert res["recommended_action"] == "ACCEPT_TREDS_BID"
    assert res["net_working_capital_savings"] > Decimal("0.00")
