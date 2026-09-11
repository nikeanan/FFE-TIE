from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class ReturnPeriodYears(int, Enum):
    TWO_YEAR = 2
    FIVE_YEAR = 5
    TEN_YEAR = 10
    TWENTY_FIVE_YEAR = 25
    FIFTY_YEAR = 50
    HUNDRED_YEAR = 100


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
