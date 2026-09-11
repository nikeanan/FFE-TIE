import os
import sys
from datetime import date
from decimal import Decimal

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.db_session import db
from src.database.seed_data import seed_database
from src.agents.validator_agent import validator_agent
from src.agents.tracker_agent import tracker_agent, InboundEmailParser, ActionType
from src.agents.escalator_agent import escalator_agent
from src.agents.financier_agent import financier_agent
from src.agents.forecaster_agent import forecaster_agent
from src.agents.advisor_agent import advisor_agent
from src.agents.orchestrator import orchestrator


def setup_function():
    """Reset database before each test run."""
    seed_database()


def test_agent_1_validator_discrepancy_and_moat():
    # INV-2041 has quantity mismatch (480 vs 450) and missing Udyam on NTPC Dadri
    state = validator_agent.run_sync("inv_ntpc_2041")
    assert state.verdict in ["BLOCKED", "FIX_REQUIRED"]
    assert state.score < 0.85
    # Should catch QTY_MISMATCH and learned rule
    flag_codes = [f["code"] for f in state.flags]
    assert "QTY_MISMATCH" in flag_codes
    assert state.whatsapp_message is not None
    assert "NTPC Dadri" in state.whatsapp_message
    assert "FIX" in state.whatsapp_message


def test_agent_1_auto_remediation():
    # Test orchestrator auto-remediation
    rem = orchestrator.auto_remediate_invoice("inv_ntpc_2041")
    assert rem["success"] is True
    assert rem["new_score"] >= 0.90

    # Re-verify with Validator
    state = validator_agent.run_sync("inv_ntpc_2041")
    assert state.score >= 0.90
    assert state.verdict in ["READY", "FIX_REQUIRED"]


def test_agent_2_tracker_cadence_and_thresholds():
    # Check invoice pending for days
    inv = db.get_invoice("inv_ongc_112")
    act = tracker_agent.evaluate_invoice(inv.id)
    assert act.type in [ActionType.SOFT_NUDGE, ActionType.FORMAL_REMINDER, ActionType.WAIT]
    assert act.t1_threshold > 0
    assert act.t2_threshold > act.t1_threshold


def test_agent_2_inbound_email_learning_loop():
    # Simulate buyer rejection email
    res = InboundEmailParser.process_buyer_email(
        from_email="accounts@ntpc.co.in",
        subject="Rejection Notice for INV/2026/045",
        body="Invoice rejected because internal vendor code was missing in billing header.",
    )
    assert res["detected_status"] == "REJECTED"
    assert res["learned_pattern_injected"] is True
    # Verify new rule exists in buyer rules
    rules = db.get_buyer_rules("cpse_ntpc_dadri")
    assert any("Auto-mined" in r.rule_name or "VENDOR" in r.rule_code or "LEARNED" in r.rule_code for r in rules)


def test_agent_3_escalator_ladder_and_human_gate():
    # Overdue invoice 142 days
    rec = escalator_agent.recommend_escalation("inv_ntpc_045")
    assert rec.days_overdue > 45
    assert rec.accrued_interest > Decimal("0.00")
    assert rec.total_claimable > rec.principal_amount
    # Steps 3-5 require human approval
    if rec.recommended_step.step_number >= 3:
        assert rec.recommended_step.requires_human_approval is True
        assert rec.human_approval_status == "PENDING_HUMAN_APPROVAL"
        assert rec.whatsapp_prompt is not None


def test_agent_4_financier_multi_rail_rate_shopping():
    # BHEL invoice with live TReDS offers
    fin = financier_agent.evaluate_financing("inv_bhel_088")
    assert fin.treds_ready is True
    assert len(fin.all_offers) >= 3
    assert fin.best_offer is not None
    # Best APR should be lower than MSME Bank OD APR (12.5%)
    assert fin.best_offer.discount_rate_apr < fin.msme_cc_od_apr
    assert fin.net_working_capital_savings > Decimal("0.00")
    assert fin.recommended_action == "ACCEPT_TREDS_BID"


def test_agent_5_forecaster_p10_p50_p90_and_cashflow():
    pred = forecaster_agent.predict_settlement("inv_bhel_088")
    assert pred.predicted_p10_date <= pred.predicted_p50_date
    assert pred.predicted_p50_date <= pred.predicted_p90_date

    # 12-week cash-flow simulation
    sim = forecaster_agent.simulate_cash_flow("msme_precision_01")
    assert len(sim.weeks) == 12
    assert sim.total_treds_inflow > 0


def test_agent_6_advisor_daily_nba_agenda():
    summary = advisor_agent.generate_daily_actions("msme_precision_01")
    assert summary.total_active_receivables > Decimal("0.00")
    assert len(summary.actions) > 0
    # Actions should be prioritized
    action_types = [a.action_type for a in summary.actions]
    assert any(t in ["FIX_INVOICE", "ACCEPT_TREDS_BID", "AUTHORIZE_ESCALATION"] for t in action_types)
