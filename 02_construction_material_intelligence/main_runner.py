from datetime import datetime
from src.schema import ConcreteGrade, MixProportion, BatchTicket
from src.is_code_standards import calculate_target_mean_strength, check_is456_compliance, ExposureCondition
from src.strength_predictor import HybridStrengthPredictor
from src.qc_anomaly_engine import BatchQCAnomalyEngine


def main():
    print("=" * 70)
    print("02. Construction Material Intelligence - QC & Strength Engine (v3.0)")
    print("=" * 70)

    # 1. Define Design Mix (M30 Grade as per IS 10262:2019)
    target_fck = calculate_target_mean_strength(ConcreteGrade.M30)
    mix = MixProportion(
        grade=ConcreteGrade.M30,
        target_fck_28d=target_fck,
        cement_opc_kg=350.0,
        fly_ash_kg=70.0,
        water_liters=168.0,
        fine_aggregate_sand_kg=720.0,
        coarse_aggregate_10mm_kg=480.0,
        coarse_aggregate_20mm_kg=680.0,
        chemical_admixture_kg=3.5,
    )

    print(f"\n[1] Mix Specification:")
    print(f"    Grade: {mix.grade.value} | Target Mean Strength: {mix.target_fck_28d} MPa")
    print(f"    Total Binder: {mix.total_binder_kg} kg/m3 | W/B Ratio: {mix.water_binder_ratio:.3f}")

    # Check IS 456 Durability Compliance
    violations = check_is456_compliance(
        total_cementitious_kg=mix.total_binder_kg,
        water_cement_ratio=mix.water_binder_ratio,
        grade=mix.grade,
        exposure=ExposureCondition.SEVERE,
    )
    print(f"    IS 456 Severe Exposure Compliance: {'PASSED' if not violations else 'VIOLATIONS: ' + str(violations)}")

    # 2. Simulate an actual Batch Ticket with high sand moisture
    batch = BatchTicket(
        ticket_id="BATCH-NCR-2026-9081",
        plant_id="PLANT_GURUGRAM_01",
        timestamp=datetime.now(),
        recipe_code="M30_PUMPABLE_400",
        target_proportions=mix,
        actual_cement_kg=344.0,
        actual_fly_ash_kg=70.0,
        actual_water_liters=165.0,
        actual_sand_kg=730.0,
        actual_coarse_10mm_kg=478.0,
        actual_coarse_20mm_kg=682.0,
        actual_admixture_kg=3.5,
        sand_moisture_percent=4.8,  # Rain surge: 4.8% moisture!
    )

    # 3. Anomaly Detection
    qc_engine = BatchQCAnomalyEngine()
    alerts = qc_engine.inspect_batch(batch)
    print(f"\n[2] Real-time Batch QC Alerts: {len(alerts)} alert(s) triggered:")
    for a in alerts:
        print(f"    [{a.severity}] {a.parameter}: Actual={a.actual_value}, Target={a.target_value} ({a.deviation_percent:+0.1f}%)")
        print(f"      -> Diagnosis: {a.explanation}")
        print(f"      -> Action: {a.recommended_engineer_action}")

    # 4. Compressive Strength Prediction with Uncertainty Quantification
    predictor = HybridStrengthPredictor()
    pred = predictor.predict_strength(batch)
    print(f"\n[3] Strength Predictions & Uncertainty Quantification (90% PI):")
    print(f"    Effective W/C Ratio: {pred['effective_water_cement_ratio']} (+{pred['free_water_from_sand_liters']}L unmetered aggregate water)")
    print(f"    Predicted 7-Day Strength: {pred['predicted_7d_strength_mpa']} MPa (90% PI: {pred['prediction_interval_7d_90'][0]} - {pred['prediction_interval_7d_90'][1]} MPa)")
    print(f"    Predicted 28-Day Strength: {pred['predicted_28d_strength_mpa']} MPa (90% PI: {pred['prediction_interval_28d_90'][0]} - {pred['prediction_interval_28d_90'][1]} MPa)")
    print(f"    Target Mean Strength: {pred['target_mean_strength_mpa']} MPa | Margin: {pred['safety_margin_mpa']:+0.2f} MPa")
    print(f"    Calibration Status: {pred['confidence_level']} | Operational Flag: [{pred['operational_flag']}]")
    print(f"    Governance: {pred['governance_note']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
