import numpy as np
from .schema import BatchTicket


class HybridStrengthPredictor:
    """Combines Abram's Water-Cement ratio law with Bayesian residual uncertainty estimation.
    
    Architecture:
      Layer 1: Engineering Prior fc = A / (B^(1.5 * w/c_eff))
      Layer 2: Pozzolanic development adjustment for mineral admixtures (Fly Ash / GGBS)
      Layer 3: Uncertainty Quantification (90% Prediction Intervals & Confidence Level)
    """

    def __init__(self, A_param: float = 98.0, B_param: float = 2.4, plant_variance_sigma: float = 1.8):
        self.A = A_param
        self.B = B_param
        self.sigma = plant_variance_sigma  # Standard deviation of plant calibration error

    def predict_strength(self, batch: BatchTicket) -> dict:
        total_binder = batch.actual_cement_kg + batch.actual_fly_ash_kg
        
        # 1. Adjust water for measured aggregate free moisture
        free_water_from_sand = batch.free_water_from_sand_liters
        effective_water = batch.actual_water_liters + free_water_from_sand
        
        effective_wc = effective_water / total_binder if total_binder > 0 else 0.55

        # 2. Base 28-day strength from Engineering Prior (Abram's Law)
        base_pred_28d = self.A / (self.B ** (1.5 * effective_wc))
        
        # 3. Pozzolanic activity adjustment
        fly_ash_ratio = batch.actual_fly_ash_kg / total_binder if total_binder > 0 else 0.0
        early_age_factor = 0.67 - (0.12 * fly_ash_ratio)
        pred_7d = base_pred_28d * early_age_factor

        # 4. Uncertainty Quantification: 90% Prediction Interval (z = 1.645)
        z_90 = 1.645
        interval_margin = z_90 * self.sigma
        
        lower_28d = max(0.0, base_pred_28d - interval_margin)
        upper_28d = base_pred_28d + interval_margin

        lower_7d = max(0.0, pred_7d - (interval_margin * early_age_factor))
        upper_7d = pred_7d + (interval_margin * early_age_factor)

        # 5. Confidence Assessment based on input data stability
        if batch.sand_moisture_percent > 4.5:
            confidence = "MEDIUM (High Moisture Variance Observed)"
            risk_flag = "VERIFY_MOISTURE_CORRECTION"
        elif effective_wc > 0.55:
            confidence = "LOW (High W/B Ratio Out of Optimal Range)"
            risk_flag = "INVESTIGATE_WATER_DOSING"
        else:
            confidence = "HIGH (Within Standard Calibrated Envelope)"
            risk_flag = "NORMAL_PRODUCTION"

        target_fck = batch.target_proportions.target_fck_28d
        safety_margin = base_pred_28d - target_fck

        return {
            "effective_water_cement_ratio": round(effective_wc, 3),
            "free_water_from_sand_liters": round(free_water_from_sand, 1),
            "predicted_7d_strength_mpa": round(pred_7d, 2),
            "prediction_interval_7d_90": [round(lower_7d, 2), round(upper_7d, 2)],
            "predicted_28d_strength_mpa": round(base_pred_28d, 2),
            "prediction_interval_28d_90": [round(lower_28d, 2), round(upper_28d, 2)],
            "target_mean_strength_mpa": round(target_fck, 2),
            "safety_margin_mpa": round(safety_margin, 2),
            "confidence_level": confidence,
            "operational_flag": risk_flag,
            "governance_note": "Decision-support prediction. Verification by certified QC Engineer required.",
        }
