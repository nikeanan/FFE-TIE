from .schema import ConcreteGrade, ExposureCondition


# IS 456:2000 Table 5: Minimum Cementitious Content & Max W/C Ratio for RCC
IS456_LIMITS = {
    ExposureCondition.MILD: {"min_cement": 300, "max_wc": 0.55, "min_grade": ConcreteGrade.M20},
    ExposureCondition.MODERATE: {"min_cement": 300, "max_wc": 0.50, "min_grade": ConcreteGrade.M25},
    ExposureCondition.SEVERE: {"min_cement": 320, "max_wc": 0.45, "min_grade": ConcreteGrade.M30},
    ExposureCondition.VERY_SEVERE: {"min_cement": 340, "max_wc": 0.45, "min_grade": ConcreteGrade.M35},
    ExposureCondition.EXTREME: {"min_cement": 360, "max_wc": 0.40, "min_grade": ConcreteGrade.M40},
}

# IS 10262:2019 Standard Deviation (s) values for target mean strength
IS10262_STD_DEV = {
    ConcreteGrade.M20: 4.0,
    ConcreteGrade.M25: 4.0,
    ConcreteGrade.M30: 5.0,
    ConcreteGrade.M35: 5.0,
    ConcreteGrade.M40: 5.0,
    ConcreteGrade.M50: 5.0,
}


def calculate_target_mean_strength(grade: ConcreteGrade, custom_s: float = None) -> float:
    """Calculates Target Mean Compressive Strength f'ck = fck + 1.65 * s (IS 10262:2019 Clause 4.2)"""
    grade_val = float(grade.value.replace("M", ""))
    s = custom_s if custom_s is not None else IS10262_STD_DEV.get(grade, 5.0)
    target_fck = grade_val + 1.65 * s
    return round(target_fck, 2)


def check_is456_compliance(
    total_cementitious_kg: float,
    water_cement_ratio: float,
    grade: ConcreteGrade,
    exposure: ExposureCondition = ExposureCondition.MODERATE,
) -> list[str]:
    """Validates mix design against IS 456 durability limits."""
    violations = []
    limits = IS456_LIMITS[exposure]

    if total_cementitious_kg < limits["min_cement"]:
        violations.append(
            f"Binder content {total_cementitious_kg} kg/m3 below IS 456 min requirement ({limits['min_cement']} kg/m3) for {exposure.value} exposure."
        )

    if water_cement_ratio > limits["max_wc"]:
        violations.append(
            f"W/C ratio {water_cement_ratio:.2f} exceeds IS 456 maximum limit ({limits['max_wc']}) for {exposure.value} exposure."
        )

    return violations
