"""2D Urban Flood Inundation & Economic Damage Assessment Engine.
Implements depth-damage vulnerability curves for critical urban infrastructure (CPHEEO & NDMA guidelines).
"""
from typing import List, Dict, Any
from pydantic import BaseModel
from .schema import InundationZone, AssetVulnerability, DamageEstimate


class FloodRiskReport(BaseModel):
    zone_id: str
    peak_flood_depth_m: float
    total_flooded_volume_m3: float
    hazard_level: str
    total_economic_loss_cr: float
    damaged_assets: List[DamageEstimate]
    emergency_action_plan: str


class InundationRiskEngine:
    """Computes flood depth distribution and financial loss modeling."""

    def evaluate_inundation_damage(
        self,
        zone: InundationZone,
        assets: List[AssetVulnerability],
    ) -> FloodRiskReport:
        depth = zone.inundation_depth_m
        damaged_list = []
        total_loss = 0.0

        for asset in assets:
            if depth <= asset.inundation_threshold_m:
                dmg_pct = 0.0
            elif depth <= 0.60:
                dmg_pct = 0.12  # 12% minor ground floor damage
            elif depth <= 1.20:
                dmg_pct = 0.35  # 35% electrical / HVAC / inventory loss
            elif depth <= 2.00:
                dmg_pct = 0.65  # 65% major structural / electrical devastation
            else:
                dmg_pct = 0.85  # 85% near total asset write-off

            loss_cr = asset.replacement_cost_cr * dmg_pct
            total_loss += loss_cr

            damaged_list.append(DamageEstimate(
                asset_name=asset.asset_name,
                asset_type=asset.asset_type,
                flood_depth_m=round(depth, 2),
                damage_percentage=round(dmg_pct * 100.0, 1),
                estimated_financial_loss_cr=round(loss_cr, 2),
            ))

        if depth > 1.0:
            hazard = "CRITICAL_HAZARD"
            action = "Trigger Level-3 Municipal Siren; Deploy NDRF rescue boats; Cut power grid feeders in Sector 4; Activate storm sump emergency pump stations."
        elif depth > 0.4:
            hazard = "MODERATE_HAZARD"
            action = "Issue traffic diversion advisory; deploy mobile dewatering pumps (1000 GPM); open floodgates on downstream sluice."
        else:
            hazard = "LOW_HAZARD"
            action = "Normal drainage clearance; monitor telemetry sensors."

        return FloodRiskReport(
            zone_id=zone.zone_id,
            peak_flood_depth_m=round(depth, 2),
            total_flooded_volume_m3=round(zone.flood_volume_m3, 1),
            hazard_level=hazard,
            total_economic_loss_cr=round(total_loss, 2),
            damaged_assets=damaged_list,
            emergency_action_plan=action,
        )


inundation_engine = InundationRiskEngine()
