import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.pilot.pilot_plants import PILOT_PLANTS
from src.pilot.pilot_evaluator import cmi_pilot_evaluator


def test_pilot_plants_count():
    assert len(PILOT_PLANTS) == 5
    assert "plant_lt_metro" in PILOT_PLANTS
    assert "plant_tata_highrise" in PILOT_PLANTS
    assert "plant_afcons_marine" in PILOT_PLANTS
    assert "plant_dilip_expressway" in PILOT_PLANTS
    assert "plant_nhpc_hydel" in PILOT_PLANTS


def test_cmi_pilot_evaluator_all():
    report = cmi_pilot_evaluator.run_all_pilots()
    assert report.total_plants_audited == 5
    assert report.total_monthly_volume_m3 > 50000.0
    assert report.average_cement_saved_kg_m3 >= 12.0
    assert report.total_monthly_savings_inr > 5000000.0
    assert report.total_annual_co2_tonnes_offset > 30000.0
    assert len(report.results) == 5


def test_lt_metro_plant_evaluation():
    lt_profile = PILOT_PLANTS["plant_lt_metro"]
    res = cmi_pilot_evaluator.evaluate_plant(lt_profile)
    assert res.target_grade == "M45"
    assert res.cement_saved_kg_m3 == 15.0
    assert res.predicted_28d_strength_mpa > res.target_28d_strength_mpa
    assert res.monthly_gross_savings_inr > 1000000.0
