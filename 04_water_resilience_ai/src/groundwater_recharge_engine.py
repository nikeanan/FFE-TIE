"""Groundwater Recharge & Managed Aquifer Recharge (MAR) Engine.
Computes annual storm runoff harvest potential, aquifer recharge volumes, and water security valuation.
"""
from typing import Dict, Any
from .schema import GroundwaterRechargeResult


class GroundwaterRechargeEngine:
    """Calculates urban runoff harvesting and Managed Aquifer Recharge (MAR) impact."""

    def compute_recharge_potential(
        self,
        catchment_area_ha: float,
        annual_rainfall_mm: float,
        runoff_coefficient: float = 0.75,
        recharge_efficiency: float = 0.65,
        water_tariff_inr_per_kl: float = 45.0,
    ) -> GroundwaterRechargeResult:
        """Annual Harvestable Runoff = Area (m²) * Rainfall (m) * Runoff_Coeff
        1 ha = 10,000 m²
        Rainfall (m) = mm / 1000
        """
        area_sqm = catchment_area_ha * 10000.0
        rain_m = annual_rainfall_mm / 1000.0
        total_raw_runoff_m3 = area_sqm * rain_m * runoff_coefficient

        recharged_m3 = total_raw_runoff_m3 * recharge_efficiency
        # 1 m³ = 1,000 Liters = 1 kL
        # Convert to MLD (Million Liters per Day) averaged over 365 days
        annual_liters = recharged_m3 * 1000.0
        recharged_mld = (annual_liters / 365.0) / 1000000.0

        # Financial value of water harvested
        water_value_inr = recharged_m3 * water_tariff_inr_per_kl
        water_value_cr = water_value_inr / 10000000.0

        return GroundwaterRechargeResult(
            annual_rainfall_mm=annual_rainfall_mm,
            catchment_area_ha=catchment_area_ha,
            harvestable_runoff_m3=round(total_raw_runoff_m3, 1),
            recharge_efficiency_percent=round(recharge_efficiency * 100.0, 1),
            annual_groundwater_recharged_mld=round(recharged_mld, 2),
            monetary_water_value_inr_cr=round(water_value_cr, 2),
        )


recharge_engine = GroundwaterRechargeEngine()
