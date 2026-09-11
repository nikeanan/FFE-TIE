import math
from .schema import StormConduit


class ConduitHydraulicSurrogate:
    """Surrogate model using Manning's open/pressurized pipe flow to predict conveyance capacity and surcharge."""

    @staticmethod
    def evaluate_conduit_capacity(conduit: StormConduit, peak_inflow_m3s: float) -> dict:
        # Full-pipe Manning capacity: Q_full = (1/n) * A * R^(2/3) * S^(1/2)
        radius = conduit.diameter_meters / 2.0
        area_full = math.pi * (radius ** 2)
        hydraulic_radius = conduit.diameter_meters / 4.0 # R = D/4 for full pipe
        
        q_full = (1.0 / conduit.manning_roughness) * area_full * (hydraulic_radius ** (2.0 / 3.0)) * math.sqrt(conduit.slope)
        
        surcharge_ratio = peak_inflow_m3s / q_full if q_full > 0 else 999.0
        is_surcharged = surcharge_ratio > 1.0

        inundation_risk = "CRITICAL_SURCHARGE" if surcharge_ratio > 1.25 else ("SURCHARGED" if is_surcharged else "ADEQUATE")

        return {
            "conduit_id": conduit.conduit_id,
            "peak_inflow_m3s": round(peak_inflow_m3s, 3),
            "full_capacity_m3s": round(q_full, 3),
            "surcharge_ratio": round(surcharge_ratio, 2),
            "is_surcharged": is_surcharged,
            "inundation_risk": inundation_risk,
        }
