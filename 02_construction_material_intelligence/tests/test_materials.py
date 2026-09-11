import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
import pytest
from src.schema import ConcreteGrade, ExposureCondition, MixProportion, BatchTicket
from src.is_code_standards import calculate_target_mean_strength, check_is456_compliance
from src.strength_predictor import HybridStrengthPredictor
from src.qc_anomaly_engine import BatchQCAnomalyEngine
from src.batch_history import summarize_batch_history


def test_target_mean_strength_is10262():
    fck_target = calculate_target_mean_strength(ConcreteGrade.M30)
    assert fck_target == 38.25

    fck_target_m25 = calculate_target_mean_strength(ConcreteGrade.M25)
    assert fck_target_m25 == 31.60


def test_is456_durability_violation():
    violations = check_is456_compliance(
        total_cementitious_kg=290.0,
        water_cement_ratio=0.52,
        grade=ConcreteGrade.M30,
        exposure=ExposureCondition.SEVERE,
    )
    assert len(violations) == 2


def test_abrams_strength_prediction_with_uncertainty():
    mix = MixProportion(
        grade=ConcreteGrade.M30,
        target_fck_28d=38.25,
        cement_opc_kg=360.0,
        water_liters=160.0,
        fine_aggregate_sand_kg=720.0,
        coarse_aggregate_10mm_kg=480.0,
        coarse_aggregate_20mm_kg=680.0,
    )
    batch = BatchTicket(
        ticket_id="TICKET-01",
        plant_id="PLANT-01",
        timestamp=datetime.now(),
        recipe_code="M30",
        target_proportions=mix,
        actual_cement_kg=360.0,
        actual_water_liters=160.0,
        actual_sand_kg=720.0,
        actual_coarse_10mm_kg=480.0,
        actual_coarse_20mm_kg=680.0,
        sand_moisture_percent=0.0,
    )
    predictor = HybridStrengthPredictor()
    res = predictor.predict_strength(batch)
    
    assert res["predicted_28d_strength_mpa"] > 38.25
    assert res["safety_margin_mpa"] > 0
    assert "prediction_interval_28d_90" in res
    assert res["prediction_interval_28d_90"][0] < res["predicted_28d_strength_mpa"] < res["prediction_interval_28d_90"][1]
    assert res["operational_flag"] == "NORMAL_PRODUCTION"


def test_qc_moisture_anomaly_detection():
    mix = MixProportion(
        grade=ConcreteGrade.M30,
        target_fck_28d=38.25,
        cement_opc_kg=350.0,
        water_liters=168.0,
        fine_aggregate_sand_kg=720.0,
        coarse_aggregate_10mm_kg=480.0,
        coarse_aggregate_20mm_kg=680.0,
    )
    batch = BatchTicket(
        ticket_id="TICKET-02",
        plant_id="PLANT-01",
        timestamp=datetime.now(),
        recipe_code="M30",
        target_proportions=mix,
        actual_cement_kg=350.0,
        actual_water_liters=168.0,
        actual_sand_kg=720.0,
        actual_coarse_10mm_kg=480.0,
        actual_coarse_20mm_kg=680.0,
        sand_moisture_percent=5.0,
    )
    qc = BatchQCAnomalyEngine()
    alerts = qc.inspect_batch(batch)
    assert len(alerts) >= 1
    assert any("Water" in a.parameter for a in alerts)
    assert hasattr(alerts[0], "recommended_engineer_action")


def test_aggregate_absorption_is_excluded_from_free_water():
    mix = MixProportion(
        grade=ConcreteGrade.M30,
        target_fck_28d=38.25,
        cement_opc_kg=350.0,
        water_liters=168.0,
        fine_aggregate_sand_kg=720.0,
        coarse_aggregate_10mm_kg=480.0,
        coarse_aggregate_20mm_kg=680.0,
    )
    batch = BatchTicket(
        ticket_id="TICKET-03",
        plant_id="PLANT-01",
        timestamp=datetime.now(),
        recipe_code="M30",
        target_proportions=mix,
        actual_cement_kg=350.0,
        actual_water_liters=168.0,
        actual_sand_kg=720.0,
        actual_coarse_10mm_kg=480.0,
        actual_coarse_20mm_kg=680.0,
        sand_moisture_percent=2.0,
        sand_absorption_percent=1.5,
    )

    assert batch.free_water_from_sand_liters == pytest.approx(3.6)
    result = HybridStrengthPredictor().predict_strength(batch)
    assert result["free_water_from_sand_liters"] == 3.6


def test_historical_batch_summary_reports_prediction_error_and_alerts():
    record = {
        "ticket_id": "BATCH-001",
        "timestamp": datetime.now(),
        "grade": "M30",
        "cement_kg": 352.0,
        "fly_ash_kg": 70.0,
        "water_liters": 165.0,
        "sand_kg": 725.0,
        "coarse_10mm_kg": 478.0,
        "coarse_20mm_kg": 682.0,
        "sand_moisture_pct": 1.2,
        "actual_7d_strength_mpa": 35.2,
        "actual_28d_strength_mpa": 42.8,
    }

    summary = summarize_batch_history([record])

    assert summary["batch_count"] == 1
    assert summary["grades"] == {"M30": 1}
    assert summary["average_actual_28d_strength_mpa"] == 42.8
    assert summary["mean_prediction_error_mpa"] is not None
