from typing import List, Dict
from fastapi import FastAPI
from pydantic import BaseModel
from src.schema import Subcatchment, StormConduit, RainfallEvent
from src.hydrological_preprocessor import HydrologicalProcessor
from src.physics_surrogate_model import ConduitHydraulicSurrogate
from src.intervention_comparator import SUDSInterventionComparator

app = FastAPI(
    title="WaterResilience AI API",
    description="REST API for rapid physics-informed urban flood simulation and Sponge City (SUDS) ROI optimization.",
    version="1.0.0",
)

class FloodSimRequest(BaseModel):
    catchment: Subcatchment
    storm: RainfallEvent
    conduit: StormConduit
    interventions: List[Dict] = []

@app.get("/")
def root():
    return {"service": "WaterResilience AI API", "status": "ONLINE"}

@app.post("/api/flood/simulate")
def simulate_catchment_flood(req: FloodSimRequest):
    q_peak = HydrologicalProcessor.calculate_rational_peak_discharge(req.catchment, req.storm)
    pipe_eval = ConduitHydraulicSurrogate.evaluate_conduit_capacity(req.conduit, q_peak)
    excess_flood = max(0.0, q_peak - pipe_eval["full_capacity_m3s"])

    ranked_interventions = []
    if req.interventions:
        ranked_interventions = SUDSInterventionComparator.compare_options(excess_flood, req.interventions)

    return {
        "peak_inflow_m3s": q_peak,
        "conduit_evaluation": pipe_eval,
        "excess_flood_m3s": round(excess_flood, 3),
        "sponge_city_recommendations": ranked_interventions,
    }
