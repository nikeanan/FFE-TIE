import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.schema import ReturnPeriodYears, Subcatchment, StormConduit, RainfallEvent
from src.hydrological_preprocessor import HydrologicalProcessor
from src.physics_surrogate_model import ConduitHydraulicSurrogate
from src.intervention_comparator import SUDSInterventionComparator


def test_rational_peak_runoff():
    catchment = Subcatchment(id="C1", area_hectares=10.0, imperviousness_percent=100.0, slope_percent=1.0)
    rain = RainfallEvent(return_period=ReturnPeriodYears.FIFTY_YEAR, duration_minutes=60, intensity_mm_per_hr=100.0)
    q = HydrologicalProcessor.calculate_rational_peak_discharge(catchment, rain)
    assert q == 2.50


def test_conduit_hydraulic_surcharge():
    conduit = StormConduit(conduit_id="P1", from_node="A", to_node="B", length_meters=100.0, diameter_meters=1.0, slope=0.005)
    
    eval_low = ConduitHydraulicSurrogate.evaluate_conduit_capacity(conduit, 0.5)
    assert eval_low["is_surcharged"] is False

    eval_high = ConduitHydraulicSurrogate.evaluate_conduit_capacity(conduit, 5.0)
    assert eval_high["is_surcharged"] is True
    assert eval_high["inundation_risk"] == "CRITICAL_SURCHARGE"


def test_intervention_comparator_ranking():
    interventions = [
        {"name": "Option Expensive", "type": "GRAY", "peak_flow_reduction_m3s": 1.0, "estimated_cost_inr_lakhs": 100.0},
        {"name": "Option Cheap", "type": "BLUE_GREEN", "peak_flow_reduction_m3s": 1.0, "estimated_cost_inr_lakhs": 20.0},
    ]
    ranked = SUDSInterventionComparator.compare_options(1.0, interventions)
    assert ranked[0]["intervention_name"] == "Option Cheap"
    assert ranked[0]["cost_efficiency_lakhs_per_m3s"] == 20.0
