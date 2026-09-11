import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from decimal import Decimal
from src.pilot.pilot_evaluator import pilot_evaluator
from src.pilot.pilot_suppliers import PILOT_SUPPLIERS


def test_pilot_suppliers_count():
    assert len(PILOT_SUPPLIERS) == 5
    assert "pilot_bhel_turbine" in PILOT_SUPPLIERS
    assert "pilot_pgcil_transformers" in PILOT_SUPPLIERS
    assert "pilot_ntpc_boilers" in PILOT_SUPPLIERS
    assert "pilot_ongc_petrochem" in PILOT_SUPPLIERS
    assert "pilot_railways_forgings" in PILOT_SUPPLIERS


def test_pilot_evaluator_all_suppliers():
    report = pilot_evaluator.run_all_pilots()
    assert report.total_suppliers_audited == 5
    assert report.total_invoice_book_audited == Decimal("13550000.00")
    assert report.total_traps_neutralized >= 10
    assert report.average_first_pass_score_before < 0.50
    assert report.average_first_pass_score_after == 1.00  # 100% Zero-Rejection Guarantee
    assert report.total_working_capital_savings > Decimal("50000.00")
    assert len(report.results) == 5


def test_bhel_pilot_specific_remediation():
    bhel_profile = PILOT_SUPPLIERS["pilot_bhel_turbine"]
    results = pilot_evaluator.evaluate_supplier(bhel_profile)
    assert len(results) == 1
    r = results[0]
    assert r.invoice_number == "INV/2026/BHEL-091"
    assert len(r.auto_remediation_actions) == 3
    assert r.gatekeeper_final_score == 1.00
    assert r.dso_days_compressed == 32
    assert r.treds_factoring_apr == 0.0785


def test_ntpc_gem_crac_pilot_remediation():
    ntpc_profile = PILOT_SUPPLIERS["pilot_ntpc_boilers"]
    results = pilot_evaluator.evaluate_supplier(ntpc_profile)
    r = results[0]
    assert r.invoice_number == "INV/2026/NTPC-08"
    assert r.claimable_sec16_interest > 0
    assert "GeM GFR Rule 149 Deemed Acceptance" in r.statutory_leverage_applied
