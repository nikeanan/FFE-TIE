import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.carbon_intelligence import carbon_engine, CarbonProfile
from src.cure_maturity_engine import maturity_engine, MaturityReading
from src.qa_certificate_exporter import qa_exporter


def test_carbon_intelligence_computation():
    profile = CarbonProfile(
        opc_kg=280.0,
        fly_ash_kg=90.0,
        ggbs_kg=40.0,
        micro_silica_kg=0.0,
        water_liters=160.0,
        sand_kg=720.0,
        coarse_aggregate_kg=1150.0,
        admixture_kg=3.5,
    )
    res = carbon_engine.compute_embodied_carbon(profile, monthly_volume_m3=8000.0)
    assert res.total_co2e_kg_per_m3 > 0
    assert res.scm_replacement_percentage > 30.0
    assert res.co2e_reduction_percentage > 25.0
    assert res.griha_points_eligible >= 3
    assert res.annual_plant_carbon_offset_tonnes > 1000.0


def test_concrete_maturity_early_strength():
    # 48 hours curing at 28 C (hot weather)
    history = [
        MaturityReading(hours_elapsed=12.0, curing_temp_celsius=28.0),
        MaturityReading(hours_elapsed=24.0, curing_temp_celsius=30.0),
        MaturityReading(hours_elapsed=36.0, curing_temp_celsius=29.0),
        MaturityReading(hours_elapsed=48.0, curing_temp_celsius=28.0),
    ]
    est = maturity_engine.estimate_early_strength(
        temperature_history=history,
        target_28d_strength=38.25,
    )
    assert est.maturity_index_degree_hours > 1500.0
    assert est.estimated_insitu_strength_mpa > 15.0
    assert est.percent_target_achieved > 40.0


def test_qa_certificate_exporter():
    cert = qa_exporter.generate_batch_certificate(
        ticket_id="TICKET-2026-001",
        plant_id="PLANT-DELHI-01",
        project_name="Delhi-Meerut RRTS Corridor Package 3",
        client_name="Larsen & Toubro Ltd",
        grade="M35",
        recipe_code="M35_FLYASH_PUMP",
        batched_volume_m3=6.0,
        target_fck=43.25,
        predicted_28d_fck=46.50,
        effective_wc_ratio=0.385,
        co2e_per_m3=248.5,
        qc_verdict="PASSED_AND_CERTIFIED",
    )
    assert "DIGITAL READY-MIX CONCRETE QUALITY & COMPLIANCE CERTIFICATE" in cert
    assert "Larsen & Toubro Ltd" in cert
    assert "SHA256-CMI-TICKET-2026-001" in cert
