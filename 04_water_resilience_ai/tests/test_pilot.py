"""Tests for WRAI 5-City Pilot Evaluator and Smart Resilience Engine."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.pilot.pilot_cities import PILOT_CITIES
from src.pilot.pilot_evaluator import wrai_pilot_evaluator, WRAIPilotReport


def test_wrai_all_cities_configured():
    assert len(PILOT_CITIES) == 5
    assert "CITY_BENGALURU_BBMP" in PILOT_CITIES
    assert "CITY_MUMBAI_BMC" in PILOT_CITIES
    assert "CITY_CHENNAI_GCC" in PILOT_CITIES
    assert "CITY_GURUGRAM_GMDA" in PILOT_CITIES
    assert "CITY_HYDERABAD_GHMC" in PILOT_CITIES


def test_wrai_individual_city_simulation():
    profile = PILOT_CITIES["CITY_BENGALURU_BBMP"]
    res = wrai_pilot_evaluator.evaluate_city(profile)

    assert res.city_id == "CITY_BENGALURU_BBMP"
    assert res.peak_inflow_discharge_m3s > 0
    assert res.baseline_economic_loss_cr > 0
    assert res.flood_damage_prevented_cr > 0
    assert res.annual_groundwater_recharge_mld > 0
    assert res.benefit_cost_ratio_bcr > 1.0


def test_wrai_run_all_pilots_aggregate_report():
    report: WRAIPilotReport = wrai_pilot_evaluator.run_all_pilots()

    assert report.total_cities_audited == 5
    assert report.total_catchment_area_ha > 1500.0
    assert report.total_baseline_damage_risk_cr > 2000.0  # > ₹ 2,000 Cr risk
    assert report.total_flood_damage_prevented_cr > 2000.0
    assert report.total_annual_water_harvested_mld > 20.0  # > 20 MLD
    assert report.average_benefit_cost_ratio > 10.0  # > 10x ROI
