from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class ConcreteGrade(str, Enum):
    M20 = "M20"
    M25 = "M25"
    M30 = "M30"
    M35 = "M35"
    M40 = "M40"
    M50 = "M50"


class ExposureCondition(str, Enum):
    MILD = "MILD"
    MODERATE = "MODERATE"
    SEVERE = "SEVERE"
    VERY_SEVERE = "VERY_SEVERE"
    EXTREME = "EXTREME"


class MixProportion(BaseModel):
    """Mix proportions per cubic meter (kg/m3)"""
    grade: ConcreteGrade
    target_fck_28d: float
    cement_opc_kg: float
    fly_ash_kg: float = 0.0
    ggbs_kg: float = 0.0
    water_liters: float
    fine_aggregate_sand_kg: float
    coarse_aggregate_10mm_kg: float
    coarse_aggregate_20mm_kg: float
    chemical_admixture_kg: float = 0.0

    @property
    def total_binder_kg(self) -> float:
        return self.cement_opc_kg + self.fly_ash_kg + self.ggbs_kg

    @property
    def water_binder_ratio(self) -> float:
        return self.water_liters / self.total_binder_kg if self.total_binder_kg > 0 else 0.0


class BatchTicket(BaseModel):
    """Actual batch plant sensor readings per batch"""
    ticket_id: str
    plant_id: str
    timestamp: datetime
    recipe_code: str
    target_proportions: MixProportion
    actual_cement_kg: float
    actual_fly_ash_kg: float = 0.0
    actual_water_liters: float
    actual_sand_kg: float
    actual_coarse_10mm_kg: float
    actual_coarse_20mm_kg: float
    actual_admixture_kg: float = 0.0
    sand_moisture_percent: float = 0.0
    sand_absorption_percent: float = 0.0
    slump_measured_mm: Optional[float] = None
    cube_strength_7d_actual: Optional[float] = None
    cube_strength_28d_actual: Optional[float] = None

    @property
    def free_water_from_sand_liters(self) -> float:
        """Returns surface water after accounting for aggregate absorption."""
        net_surface_moisture = max(
            0.0, self.sand_moisture_percent - self.sand_absorption_percent
        )
        return self.actual_sand_kg * net_surface_moisture / 100.0
