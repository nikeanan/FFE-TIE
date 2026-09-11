from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel
from src.schema import ConcreteGrade, ExposureCondition, MixProportion, BatchTicket
from src.is_code_standards import calculate_target_mean_strength, check_is456_compliance
from src.strength_predictor import HybridStrengthPredictor
from src.qc_anomaly_engine import BatchQCAnomalyEngine
from src.batch_history import summarize_batch_history

app = FastAPI(
    title="Construction Material Intelligence (CMI) API",
    description="REST API for Ready-Mix Concrete batch anomaly inspection, IS 10262 target mean strength, and Abrams compressive strength forecasting.",
    version="1.0.0",
)

class MixCheckRequest(BaseModel):
    grade: ConcreteGrade
    exposure: ExposureCondition = ExposureCondition.MODERATE
    total_cementitious_kg: float
    water_binder_ratio: float

@app.get("/")
def root():
    return {"service": "Construction Material Intelligence API", "status": "ONLINE"}

@app.post("/api/mix/target-strength")
def get_target_strength(grade: ConcreteGrade):
    target = calculate_target_mean_strength(grade)
    return {"grade": grade.value, "target_mean_strength_mpa": target}

@app.post("/api/mix/validate-is456")
def validate_is456(req: MixCheckRequest):
    violations = check_is456_compliance(
        total_cementitious_kg=req.total_cementitious_kg,
        water_cement_ratio=req.water_binder_ratio,
        grade=req.grade,
        exposure=req.exposure,
    )
    return {
        "is_compliant": len(violations) == 0,
        "violations": violations,
    }

@app.post("/api/batch/inspect")
def inspect_batch_ticket(batch: BatchTicket):
    qc = BatchQCAnomalyEngine()
    alerts = qc.inspect_batch(batch)
    
    predictor = HybridStrengthPredictor()
    pred = predictor.predict_strength(batch)

    return {
        "ticket_id": batch.ticket_id,
        "qc_alerts": [{"severity": a.severity, "parameter": a.parameter, "deviation_percent": a.deviation_percent, "explanation": a.explanation} for a in alerts],
        "strength_predictions": pred,
    }


class HistoricalBatchRecord(BaseModel):
    ticket_id: str
    timestamp: datetime
    grade: ConcreteGrade
    cement_kg: float
    fly_ash_kg: float = 0.0
    water_liters: float
    sand_kg: float
    coarse_10mm_kg: float
    coarse_20mm_kg: float
    sand_moisture_pct: float = 0.0
    actual_7d_strength_mpa: float | None = None
    actual_28d_strength_mpa: float | None = None


@app.post("/api/batches/summary")
def summarize_historical_batches(records: list[HistoricalBatchRecord]):
    """Summarize imported batch history for offline pilot validation."""
    return summarize_batch_history([record.model_dump() for record in records])
