from src.schema import ReturnPeriodYears, Subcatchment, StormConduit, RainfallEvent
from src.hydrological_preprocessor import HydrologicalProcessor
from src.physics_surrogate_model import ConduitHydraulicSurrogate
from src.intervention_comparator import SUDSInterventionComparator


def main():
    print("=" * 70)
    print("04. WaterResilience AI - Urban Drainage & Flood Simulation")
    print("=" * 70)

    # 1. Define Urban Catchment & 50-year Extreme Cloudburst Event
    catchment = Subcatchment(
        id="CATCH_IND_SECTOR_62",
        area_hectares=45.0,
        imperviousness_percent=82.0,
        slope_percent=1.2,
    )

    storm_50yr = RainfallEvent(
        return_period=ReturnPeriodYears.FIFTY_YEAR,
        duration_minutes=60,
        intensity_mm_per_hr=78.5,
    )

    # 2. Runoff Inflow Calculation
    q_peak = HydrologicalProcessor.calculate_rational_peak_discharge(catchment, storm_50yr)
    print(f"\n[1] Hydrological Inflow (Rational Runoff Engine):")
    print(f"    Catchment Area: {catchment.area_hectares} ha | Imperviousness: {catchment.imperviousness_percent}%")
    print(f"    Design Storm: 50-Year (Intensity: {storm_50yr.intensity_mm_per_hr} mm/hr)")
    print(f"    Peak Storm Discharge: {q_peak} m3/sec")

    # 3. Existing Drainage Network Capacity Check
    existing_drain = StormConduit(
        conduit_id="TRUNK_DRAIN_MAIN_01",
        from_node="JUNC_SEC62_A",
        to_node="OUTFALL_RIVER_01",
        length_meters=850.0,
        diameter_meters=1.6,
        slope=0.003,
    )

    hydraulic_eval = ConduitHydraulicSurrogate.evaluate_conduit_capacity(existing_drain, q_peak)
    print(f"\n[2] Drainage Network Hydraulic Surcharge Evaluation:")
    print(f"    Conduit ID: {hydraulic_eval['conduit_id']} (Dia: {existing_drain.diameter_meters}m)")
    print(f"    Conduit Full-Bore Capacity: {hydraulic_eval['full_capacity_m3s']} m3/s")
    print(f"    Peak Surcharge Ratio: {hydraulic_eval['surcharge_ratio']}x -> Risk: [{hydraulic_eval['inundation_risk']}]")

    excess_flood_m3s = max(0.0, q_peak - hydraulic_eval["full_capacity_m3s"])
    print(f"    Excess Surcharged Flood Flow: {excess_flood_m3s:0.2f} m3/s")

    # 4. Compare Sponge City / Engineering Interventions
    interventions = [
        {
            "name": "Option A: Micro-Detention Basin (Parks & Playgrounds)",
            "type": "BLUE_GREEN",
            "peak_flow_reduction_m3s": 2.4,
            "estimated_cost_inr_lakhs": 65.0,
        },
        {
            "name": "Option B: Permeable Pavements & Roadside Bioswales",
            "type": "BLUE_GREEN",
            "peak_flow_reduction_m3s": 1.1,
            "estimated_cost_inr_lakhs": 42.0,
        },
        {
            "name": "Option C: Twin 2.2m RCC Box Culvert Upsizing",
            "type": "GRAY_INFRASTRUCTURE",
            "peak_flow_reduction_m3s": 3.2,
            "estimated_cost_inr_lakhs": 220.0,
        },
    ]

    ranked_options = SUDSInterventionComparator.compare_options(excess_flood_m3s, interventions)
    print(f"\n[3] AI Intervention Comparison & Optimization:")
    for rank, opt in enumerate(ranked_options, 1):
        status = "SOLVES FLOOD" if opt["completely_resolves_flood"] else f"Residual Overflow: {opt['residual_surcharge_m3s']} m3/s"
        print(f"    Rank #{rank}: {opt['intervention_name']} ({opt['type']})")
        print(f"      -> Cost: INR {opt['estimated_cost_inr_lakhs']} L | Efficiency: INR {opt['cost_efficiency_lakhs_per_m3s']} L/(m3/s) | Result: {status}")
    print("=" * 70)


if __name__ == "__main__":
    main()
