"""Tests for CECI 5-Contractor Pilot Evaluator and PoV Engine."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.pilot.pilot_contractors import PILOT_CONTRACTORS
from src.pilot.pilot_evaluator import ceci_pilot_evaluator, CECIPilotReport


def test_ceci_all_contractors_configured():
    assert len(PILOT_CONTRACTORS) == 5
    assert "CONTRACTOR_LNT_METRO" in PILOT_CONTRACTORS
    assert "CONTRACTOR_TATA_COASTAL" in PILOT_CONTRACTORS
    assert "CONTRACTOR_DILIP_NHAI" in PILOT_CONTRACTORS
    assert "CONTRACTOR_AFCONS_JETTY" in PILOT_CONTRACTORS
    assert "CONTRACTOR_MEGHA_TUNNEL" in PILOT_CONTRACTORS


def test_ceci_individual_contractor_evaluation():
    profile = PILOT_CONTRACTORS["CONTRACTOR_LNT_METRO"]
    res = ceci_pilot_evaluator.evaluate_contractor(profile)

    assert res.contractor_id == "CONTRACTOR_LNT_METRO"
    assert res.variation_claim_amount_inr > 0
    assert res.eot_days_approved == 68
    assert res.prolongation_cost_recovered_inr > 0
    assert res.ld_liability_shielded_inr > 0
    assert res.total_financial_impact_inr > 0


def test_ceci_run_all_pilots_aggregate_report():
    report: CECIPilotReport = ceci_pilot_evaluator.run_all_pilots()

    assert report.total_contractors_audited == 5
    assert report.total_contract_value_cr > 5000.0  # ₹ 7,590 Cr portfolio
    assert report.total_variation_claims_inr > 300000000.0  # > ₹ 30 Cr
    assert report.total_prolongation_claims_inr > 40000000.0  # > ₹ 4 Cr
    assert report.total_escalation_claims_inr > 30000000.0   # > ₹ 3 Cr
    assert report.total_ld_liability_shielded_inr > 80000000.0  # > ₹ 8 Cr
    assert report.total_monetary_value_unlocked_inr > 500000000.0  # > ₹ 50 Cr
