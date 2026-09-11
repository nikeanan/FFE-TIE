"""
Construction Material Intelligence (CMI) -- Embodied Carbon & SCM Intelligence Engine
Calculates Scope 3 Embodied Carbon (kg CO2e / m3), SCM replacement ratios,
and green building credits (GRIHA, IGBC, LEED).
"""
from decimal import Decimal
from typing import Dict, Any, List
from pydantic import BaseModel


class CarbonProfile(BaseModel):
    opc_kg: float
    fly_ash_kg: float
    ggbs_kg: float
    micro_silica_kg: float
    water_liters: float
    sand_kg: float
    coarse_aggregate_kg: float
    admixture_kg: float


class CarbonAuditResult(BaseModel):
    total_co2e_kg_per_m3: float
    baseline_opc_co2e_kg_per_m3: float
    co2e_reduction_kg_per_m3: float
    co2e_reduction_percentage: float
    scm_replacement_percentage: float
    griha_points_eligible: int
    igbc_rating_tier: str
    breakdown_by_material: Dict[str, float]
    annual_plant_carbon_offset_tonnes: float


class CarbonIntelligenceEngine:
    """
    Standard Emission Factors (kg CO2e / kg material):
    - OPC 53 Cement: 0.860 kg CO2e / kg
    - Fly Ash (Class F): 0.020 kg CO2e / kg
    - GGBS (Ground Granulated Blast-furnace Slag): 0.075 kg CO2e / kg
    - Micro Silica: 0.025 kg CO2e / kg
    - Natural / M-Sand: 0.005 kg CO2e / kg
    - Crushed Coarse Aggregate: 0.005 kg CO2e / kg
    - Chemical Admixture (PCE): 0.250 kg CO2e / kg
    """

    EMISSION_FACTORS = {
        "opc": 0.860,
        "fly_ash": 0.020,
        "ggbs": 0.075,
        "micro_silica": 0.025,
        "sand": 0.005,
        "coarse_agg": 0.005,
        "admixture": 0.250,
    }

    def compute_embodied_carbon(
        self,
        profile: CarbonProfile,
        monthly_volume_m3: float = 7500.0,
    ) -> CarbonAuditResult:
        opc_co2 = profile.opc_kg * self.EMISSION_FACTORS["opc"]
        fa_co2 = profile.fly_ash_kg * self.EMISSION_FACTORS["fly_ash"]
        ggbs_co2 = profile.ggbs_kg * self.EMISSION_FACTORS["ggbs"]
        ms_co2 = profile.micro_silica_kg * self.EMISSION_FACTORS["micro_silica"]
        sand_co2 = profile.sand_kg * self.EMISSION_FACTORS["sand"]
        coarse_co2 = profile.coarse_aggregate_kg * self.EMISSION_FACTORS["coarse_agg"]
        admix_co2 = profile.admixture_kg * self.EMISSION_FACTORS["admixture"]

        total_co2 = opc_co2 + fa_co2 + ggbs_co2 + ms_co2 + sand_co2 + coarse_co2 + admix_co2

        total_binder = profile.opc_kg + profile.fly_ash_kg + profile.ggbs_kg + profile.micro_silica_kg
        total_scm = profile.fly_ash_kg + profile.ggbs_kg + profile.micro_silica_kg
        scm_pct = (total_scm / total_binder * 100.0) if total_binder > 0 else 0.0

        # Equivalent 100% OPC benchmark
        baseline_co2 = (total_binder * self.EMISSION_FACTORS["opc"]) + sand_co2 + coarse_co2 + admix_co2
        reduction_kg = max(0.0, baseline_co2 - total_co2)
        reduction_pct = (reduction_kg / baseline_co2 * 100.0) if baseline_co2 > 0 else 0.0

        # GRIHA / IGBC Green Rating tiers
        if scm_pct >= 35.0:
            griha_points = 4
            igbc_tier = "PLATINUM / 5-STAR GREEN CONCRETE"
        elif scm_pct >= 20.0:
            griha_points = 3
            igbc_tier = "GOLD / 4-STAR GREEN CONCRETE"
        elif scm_pct >= 10.0:
            griha_points = 2
            igbc_tier = "SILVER / 3-STAR GREEN CONCRETE"
        else:
            griha_points = 0
            igbc_tier = "BASELINE CONVENTIONAL"

        annual_offset_tonnes = (reduction_kg * monthly_volume_m3 * 12.0) / 1000.0

        return CarbonAuditResult(
            total_co2e_kg_per_m3=round(total_co2, 2),
            baseline_opc_co2e_kg_per_m3=round(baseline_co2, 2),
            co2e_reduction_kg_per_m3=round(reduction_kg, 2),
            co2e_reduction_percentage=round(reduction_pct, 1),
            scm_replacement_percentage=round(scm_pct, 1),
            griha_points_eligible=griha_points,
            igbc_rating_tier=igbc_tier,
            breakdown_by_material={
                "OPC 53 Cement": round(opc_co2, 2),
                "Fly Ash / SCMs": round(fa_co2 + ggbs_co2 + ms_co2, 2),
                "Aggregates & Sand": round(sand_co2 + coarse_co2, 2),
                "Chemical Admixture": round(admix_co2, 2),
            },
            annual_plant_carbon_offset_tonnes=round(annual_offset_tonnes, 1),
        )


carbon_engine = CarbonIntelligenceEngine()
