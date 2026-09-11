from collections import Counter
from typing import Iterable

from .is_code_standards import calculate_target_mean_strength
from .qc_anomaly_engine import BatchQCAnomalyEngine
from .schema import BatchTicket, ConcreteGrade, MixProportion
from .strength_predictor import HybridStrengthPredictor


def build_batch_ticket(record: dict, plant_id: str = "HISTORICAL_IMPORT") -> BatchTicket:
    """Build a validated batch ticket from the sample-history CSV shape."""
    grade = ConcreteGrade(record["grade"])
    mix = MixProportion(
        grade=grade,
        target_fck_28d=calculate_target_mean_strength(grade),
        cement_opc_kg=float(record["cement_kg"]),
        fly_ash_kg=float(record.get("fly_ash_kg", 0.0)),
        water_liters=float(record["water_liters"]),
        fine_aggregate_sand_kg=float(record["sand_kg"]),
        coarse_aggregate_10mm_kg=float(record["coarse_10mm_kg"]),
        coarse_aggregate_20mm_kg=float(record["coarse_20mm_kg"]),
    )
    return BatchTicket(
        ticket_id=str(record["ticket_id"]),
        plant_id=plant_id,
        timestamp=record["timestamp"],
        recipe_code=grade.value,
        target_proportions=mix,
        actual_cement_kg=float(record["cement_kg"]),
        actual_fly_ash_kg=float(record.get("fly_ash_kg", 0.0)),
        actual_water_liters=float(record["water_liters"]),
        actual_sand_kg=float(record["sand_kg"]),
        actual_coarse_10mm_kg=float(record["coarse_10mm_kg"]),
        actual_coarse_20mm_kg=float(record["coarse_20mm_kg"]),
        sand_moisture_percent=float(record.get("sand_moisture_pct", 0.0)),
        cube_strength_7d_actual=(
            float(record["actual_7d_strength_mpa"])
            if record.get("actual_7d_strength_mpa") is not None
            else None
        ),
        cube_strength_28d_actual=(
            float(record["actual_28d_strength_mpa"])
            if record.get("actual_28d_strength_mpa") is not None
            else None
        ),
    )


def summarize_batch_history(records: Iterable[dict]) -> dict:
    """Return operational KPIs for imported historical batches."""
    tickets = [build_batch_ticket(record) for record in records]
    if not tickets:
        return {"batch_count": 0, "alert_count": 0, "critical_alert_count": 0}

    qc = BatchQCAnomalyEngine()
    predictor = HybridStrengthPredictor()
    predictions = [predictor.predict_strength(ticket) for ticket in tickets]
    alerts = [alert for ticket in tickets for alert in qc.inspect_batch(ticket)]
    actual_28d = [
        ticket.cube_strength_28d_actual
        for ticket in tickets
        if ticket.cube_strength_28d_actual is not None
    ]
    predicted_28d = [prediction["predicted_28d_strength_mpa"] for prediction in predictions]

    return {
        "batch_count": len(tickets),
        "grades": dict(Counter(ticket.target_proportions.grade.value for ticket in tickets)),
        "alert_count": len(alerts),
        "critical_alert_count": sum(alert.severity == "CRITICAL" for alert in alerts),
        "average_predicted_28d_strength_mpa": round(sum(predicted_28d) / len(predicted_28d), 2),
        "average_actual_28d_strength_mpa": round(sum(actual_28d) / len(actual_28d), 2) if actual_28d else None,
        "mean_prediction_error_mpa": round(
            sum(predicted - actual for predicted, actual in zip(predicted_28d, actual_28d)) / len(actual_28d), 2
        ) if len(actual_28d) == len(predicted_28d) else None,
    }