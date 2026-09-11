"""Tests for Time Impact Delay Analysis and Price Escalation Calculation."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
import pytest
from src.schema import DelayEvent, DelayCategory, ContractClause, EscalationComponent
from src.delay_analysis_engine import delay_engine
from src.price_escalation_engine import escalation_engine


def test_delay_analysis_engine_apportionment():
    ev_employer = DelayEvent(
        event_id="EV-1",
        title="Late Drawing Issue",
        category=DelayCategory.EMPLOYER_RISK,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 31),
        duration_days=30,
        impacted_activity="Pier Foundation",
        is_critical_path=True,
    )
    ev_force_majeure = DelayEvent(
        event_id="EV-2",
        title="Unprecedented Heavy Rain Flood",
        category=DelayCategory.FORCE_MAJEURE,
        start_date=date(2025, 2, 1),
        end_date=date(2025, 2, 15),
        duration_days=15,
        impacted_activity="Earthwork",
        is_critical_path=True,
    )
    ev_contractor = DelayEvent(
        event_id="EV-3",
        title="Batch Plant Mechanical Breakdown",
        category=DelayCategory.CONTRACTOR_RISK,
        start_date=date(2025, 3, 1),
        end_date=date(2025, 3, 5),
        duration_days=5,
        impacted_activity="Deck Concreting",
        is_critical_path=False,
    )

    res = delay_engine.analyze_delays([ev_employer, ev_force_majeure, ev_contractor], custom_daily_overhead_inr=100000.0, custom_daily_ld_inr=150000.0)

    assert res.total_gross_delay_days == 50
    assert res.employer_caused_delay_days == 30
    assert res.force_majeure_days == 15
    assert res.contractor_caused_delay_days == 5
    # Net excusable days = Employer (30) + Force Majeure (15) = 45 days
    assert res.net_excusable_eot_days == 45
    # Compensable days = Employer (30)
    assert res.net_compensable_days == 30
    assert res.prolongation_claim_amount_inr == 30 * 100000.0
    assert res.ld_shielded_amount_inr == 45 * 150000.0


def test_price_escalation_clause_10ca():
    res = escalation_engine.calculate_clause_10ca_item(
        component=EscalationComponent.STEEL_TMT,
        base_rate_inr=50000.0,
        quantity_consumed=100.0,  # 100 MT
        base_index_ci0=100.0,
        current_index_cin=115.0,  # +15%
    )

    assert res.delta_index_percent == 15.0
    assert res.escalation_amount_inr == 100.0 * 50000.0 * 0.15
    assert res.is_claimable is True


def test_price_escalation_clause_10cc_composite():
    res = escalation_engine.calculate_clause_10cc_composite(
        gross_work_done_inr=10000000.0,  # 1 Cr
        labour_component_pct=25.0,
        materials_component_pct=60.0,
        pol_fuel_component_pct=15.0,
        base_labour_index=100.0,
        curr_labour_index=110.0,  # +10%
        base_mat_index=100.0,
        curr_mat_index=108.0,    # +8%
        base_pol_index=100.0,
        curr_pol_index=120.0,    # +20%
    )

    # Labour: 10,000,000 * 0.25 * 0.10 = 250,000
    # Material: 10,000,000 * 0.60 * 0.08 = 480,000
    # POL: 10,000,000 * 0.15 * 0.20 = 300,000
    # Total: 1,030,000
    assert res["labour_escalation_vl_inr"] == 250000.0
    assert res["material_escalation_vm_inr"] == 480000.0
    assert res["fuel_escalation_vf_inr"] == 300000.0
    assert res["total_escalation_inr"] == 1030000.0
