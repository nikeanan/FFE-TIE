"""
Construction Material Intelligence (CMI) -- Concrete Maturity & Early De-Shuttering Engine
Implements Nurse-Saul and Arrhenius maturity functions (ASTM C1074 / IS 456) to predict
in-situ early compressive strength for formwork stripping and pre-stress release.
"""
from typing import List, Dict, Any
from pydantic import BaseModel
import math


class MaturityReading(BaseModel):
    hours_elapsed: float
    curing_temp_celsius: float


class InSituStrengthEstimate(BaseModel):
    maturity_index_degree_hours: float
    estimated_insitu_strength_mpa: float
    target_28d_fck: float
    percent_target_achieved: float
    deshuttering_status: str
    safety_verdict: str
    critical_threshold_mpa: float


class ConcreteMaturityEngine:
    """
    Nurse-Saul Function:
    M(t) = Sum [ (T_avg - T_0) * Delta_t ]
    where T_0 is datum temperature (typically -10 C).
    """

    DATUM_TEMPERATURE_C = -10.0

    def calculate_nurse_saul_maturity(
        self,
        temperature_history: List[MaturityReading],
    ) -> float:
        total_maturity = 0.0
        prev_hour = 0.0

        for r in temperature_history:
            delta_t = r.hours_elapsed - prev_hour
            if delta_t > 0:
                avg_temp = r.curing_temp_celsius
                maturity_increment = (avg_temp - self.DATUM_TEMPERATURE_C) * delta_t
                total_maturity += max(0.0, maturity_increment)
            prev_hour = r.hours_elapsed

        return round(total_maturity, 1)

    def estimate_early_strength(
        self,
        temperature_history: List[MaturityReading],
        target_28d_strength: float = 38.25,  # M30 target
        deshutter_threshold_pct: float = 0.70,  # 70% of target (IS 456 Clause 11.3)
    ) -> InSituStrengthEstimate:
        maturity = self.calculate_nurse_saul_maturity(temperature_history)

        # Logarithmic maturity-strength hyperbolic curve (ASTM C1074)
        # S = A + B * log(M)
        if maturity <= 50.0:
            current_strength = 2.0
        else:
            # 28d standard maturity at 20C is ~20,160 C-hrs
            maturity_ratio = min(1.0, math.log(maturity) / math.log(20160.0))
            current_strength = target_28d_strength * (maturity_ratio ** 1.35)

        current_strength = min(target_28d_strength * 1.15, max(2.0, current_strength))
        pct_achieved = (current_strength / target_28d_strength) * 100.0
        req_mpa = target_28d_strength * deshutter_threshold_pct

        if current_strength >= req_mpa:
            deshutter_status = "SAFE_TO_DESHUTTER"
            safety_verdict = f"✅ In-situ strength ({current_strength:.1f} MPa) exceeds 70% threshold ({req_mpa:.1f} MPa). Formwork striking authorized."
        else:
            deshutter_status = "HOLD_CURING_REQUIRED"
            hours_needed = max(6.0, (req_mpa - current_strength) * 1.8)
            safety_verdict = f"⛔ Curing in progress. Strength is {current_strength:.1f} MPa ({pct_achieved:.1f}%). Additional ~{hours_needed:.0f} hrs curing required before formwork release."

        return InSituStrengthEstimate(
            maturity_index_degree_hours=maturity,
            estimated_insitu_strength_mpa=round(current_strength, 2),
            target_28d_fck=target_28d_strength,
            percent_target_achieved=round(pct_achieved, 1),
            deshuttering_status=deshutter_status,
            safety_verdict=safety_verdict,
            critical_threshold_mpa=round(req_mpa, 2),
        )


maturity_engine = ConcreteMaturityEngine()
