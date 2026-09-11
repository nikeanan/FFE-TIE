from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel


class ReturnPeriodYears(int, Enum):
    TWO_YEAR = 2
    FIVE_YEAR = 5
    TEN_YEAR = 10
    TWENTY_FIVE_YEAR = 25
    FIFTY_YEAR = 50
    HUNDRED_YEAR = 100


class InterventionType(str, Enum):
    BLUE_GREEN_SUDS = "BLUE_GREEN_SUDS"
    GRAY_INFRASTRUCTURE = "GRAY_INFRASTRUCTURE"
    MANAGED_AQUIFER_RECHARGE = "MANAGED_AQUIFER_RECHARGE"
    LAKE_CASCADE_RESTORATION = "LAKE_CASCADE_RESTORATION"


class Subcatchment(BaseModel):
    id: str
    area_hectares: float
    imperviousness_percent: float  # e.g., 75% for dense urban
    slope_percent: float
    soil_curve_number: float = 85.0  # SCS Runoff Curve Number


class StormConduit(BaseModel):
    conduit_id: str
    from_node: str
    to_node: str
    length_meters: float
    diameter_meters: float
    slope: float
    manning_roughness: float = 0.015


class RainfallEvent(BaseModel):
    return_period: ReturnPeriodYears
    duration_minutes: int
    intensity_mm_per_hr: float


class InundationZone(BaseModel):
    zone_id: str
    zone_name: str
    surface_area_sqm: float
    ground_elevation_m: float
    water_level_m: float
    inundation_depth_m: float
    flood_volume_m3: float
    hazard_category: str  # LOW, MODERATE, CRITICAL


class AssetVulnerability(BaseModel):
    asset_id: str
    asset_name: str
    asset_type: str  # RESIDENTIAL, COMMERCIAL_OFFICE, TRANSPORT_METRO, SUBSTATION
    replacement_cost_cr: float
    inundation_threshold_m: float = 0.30


class DamageEstimate(BaseModel):
    asset_name: str
    asset_type: str
    flood_depth_m: float
    damage_percentage: float
    estimated_financial_loss_cr: float


class GroundwaterRechargeResult(BaseModel):
    annual_rainfall_mm: float
    catchment_area_ha: float
    harvestable_runoff_m3: float
    recharge_efficiency_percent: float
    annual_groundwater_recharged_mld: float  # Million Liters per Day equivalent
    monetary_water_value_inr_cr: float

