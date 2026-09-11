import numpy as np
from .schema import Subcatchment, RainfallEvent


class HydrologicalProcessor:
    """Calculates peak runoff using the Rational Formula (Q = C * I * A / 360) and SCS-CN methods."""

    @staticmethod
    def calculate_rational_peak_discharge(catchment: Subcatchment, rain: RainfallEvent) -> float:
        """
        Q = C * I * A / 360
        Q in m3/s
        C: composite runoff coefficient (weighted by imperviousness)
        I: rainfall intensity in mm/hr
        A: area in hectares
        """
        c_impervious = 0.90
        c_pervious = 0.30
        imp_frac = catchment.imperviousness_percent / 100.0
        c_composite = (imp_frac * c_impervious) + ((1.0 - imp_frac) * c_pervious)

        peak_q_m3s = (c_composite * rain.intensity_mm_per_hr * catchment.area_hectares) / 360.0
        return round(peak_q_m3s, 3)
