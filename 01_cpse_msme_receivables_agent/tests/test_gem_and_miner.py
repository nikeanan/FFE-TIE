import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date, timedelta
from decimal import Decimal
from src.integrations.gem_crac_tracker import gem_tracker
from src.agents.email_dispute_miner import dispute_miner


def test_gem_deemed_crac_milestone():
    delivery_date = date.today() - timedelta(days=25)
    # 25 days since delivery without CRAC -> should be DEEMED_CRAC_AUTO_ACCEPTED and overdue
    res = gem_tracker.evaluate_gem_milestone(
        invoice_number="INV/GEM/2026/001",
        delivery_date=delivery_date,
        crac_generated=False,
    )
    assert res["status"] == "DEEMED_CRAC_AUTO_ACCEPTED"
    assert res["deemed_crac_applied"] is True
    assert res["is_payment_overdue"] is True
    assert res["days_overdue"] == 5 # 25 days - (10 days CRAC + 10 days payment) = 5 days overdue


def test_gem_rule_149_demand_notice():
    notice = gem_tracker.generate_rule_149_demand_notice(
        supplier_name="Precision Engineering MSME Ltd",
        supplier_udyam="UDYAM-HR-01-0012345",
        buyer_entity="NTPC Dadri",
        consignee_designation="Senior Store Manager",
        gem_contract_no="GEMC-511687729104",
        invoice_no="INV/GEM/001",
        invoice_amount=Decimal("1500000.00"),
        delivery_date=date.today() - timedelta(days=25),
        days_overdue=5,
    )
    assert "RULE 149 OF GFR, 2017" in notice
    assert "DEEMED ACCEPTED" in notice
    assert "Section 43B(h)" in notice


def test_email_dispute_miner():
    subject = "Payment on hold for Invoice 2041 - TPI stamp missing"
    body = "Please note that the QA certificate and inspection note annexure lacks third-party inspection stamp."
    
    res = dispute_miner.analyze_inbound_email(
        buyer_id="cpse_ntpc_dadri",
        subject=subject,
        body=body,
        sender_email="finance_dadri@ntpc.co.in",
    )
    assert res["is_dispute_flagged"] is True
    assert res["detected_category"] == "INSPECTION_ANNEXURE_MISSING"
    assert "TPI report" in res["human_explanation"]
    assert "rebuttal_draft" in res or "auto_drafted_rebuttal" in res
