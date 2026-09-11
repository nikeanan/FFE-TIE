"""Tests for 2D Inundation Risk, Asset Damage, and Groundwater Recharge Engines."""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.schema import InundationZone, AssetVulnerability
from src.inundation_risk_engine import inundation_engine
from src.groundwater_recharge_engine import recharge_engine


def test_inundation_damage_evaluation():
    zone = InundationZone(
        zone_id="Z1",
        zone_name="Commercial Sector 4",
        surface_area_sqm=50000.0,
        ground_elevation_m=10.0,
        water_level_m=11.5,
        inundation_depth_m=1.5,
        flood_volume_m3=75000.0,
        hazard_category="CRITICAL",
    )
    asset = AssetVulnerability(
        asset_id="A1",
        asset_name="Tech Park Tower A",
        asset_type="COMMERCIAL_OFFICE",
        replacement_cost_cr=100.0,
    )

    report = inundation_engine.evaluate_inundation_damage(zone, [asset])
    assert report.hazard_level == "CRITICAL_HAZARD"
    assert report.total_economic_loss_cr == 65.0  # 65% damage for depth > 1.2m
    assert len(report.damaged_assets) == 1
    assert "Level-3 Municipal Siren" in report.emergency_action_plan


def test_groundwater_recharge_calculation():
    res = recharge_engine.compute_recharge_potential(
        catchment_area_ha=100.0,
        annual_rainfall_mm=1000.0,
        runoff_coefficient=0.80,
        recharge_efficiency=0.50,
        water_tariff_inr_per_kl=40.0,
    )

    # Area = 100 * 10,000 = 1,000,000 m2
    # Rain = 1.0 m
    # Raw runoff = 1,000,000 * 1.0 * 0.8 = 800,000 m3
    assert res.harvestable_runoff_m3 == 800000.0
    # Recharged = 800,000 * 0.5 = 400,000 m3
    # MLD = (400,000 * 1,000 / 365) / 1,000,000 = 1.095 ~ 1.10 MLD
    assert res.annual_groundwater_recharged_mld == 1.10
    # Water value = 400,000 * 40 INR = 16,000,000 INR = 1.60 Cr
    assert res.monetary_water_value_inr_cr == 1.60
