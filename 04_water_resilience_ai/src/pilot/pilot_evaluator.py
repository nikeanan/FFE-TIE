"""WRAI Pilot Evaluator & Proof-of-Value (PoV) Municipal Flood Audit Engine."""
from typing import Dict, List, Any
from pydantic import BaseModel
from .pilot_cities import PILOT_CITIES, PilotCityProfile, PilotCityScenario
from ..schema import Subcatchment, RainfallEvent, StormConduit, ReturnPeriodYears, InundationZone, AssetVulnerability
from ..hydrological_preprocessor import HydrologicalProcessor
from ..physics_surrogate_model import ConduitHydraulicSurrogate
from ..inundation_risk_engine import inundation_engine
from ..groundwater_recharge_engine import recharge_engine


class CitySimulationResult(BaseModel):
    city_id: str
    city_name: str
    municipal_authority: str
    zone_name: str
    catchment_area_ha: float
    
    # Baseline Hydraulic Metrics
    peak_inflow_discharge_m3s: float
    conduit_capacity_m3s: float
    baseline_flood_depth_m: float
    baseline_flood_volume_m3: float
    baseline_economic_loss_cr: float
    
    # Post-Intervention Impact
    recommended_intervention: str
    capex_cost_cr: float
    attenuated_peak_flow_m3s: float
    post_intervention_flood_depth_m: float
    flood_damage_prevented_cr: float
    annual_groundwater_recharge_mld: float
    annual_water_value_cr: float
    net_municipal_benefit_cr: float
    benefit_cost_ratio_bcr: float
    wrai_remediation_summary: str


class WRAIPilotReport(BaseModel):
    total_cities_audited: int
    total_catchment_area_ha: float
    total_baseline_damage_risk_cr: float
    total_intervention_capex_cr: float
    total_flood_damage_prevented_cr: float
    total_annual_water_harvested_mld: float
    total_annual_water_value_cr: float
    average_benefit_cost_ratio: float
    results: List[CitySimulationResult]


class WRAIPilotEvaluatorEngine:
    """Runs automated multi-city flood resilience & sponge city audits for WRAI pilot demonstrations."""

    def evaluate_city(self, profile: PilotCityProfile) -> CitySimulationResult:
        sc = profile.scenario

        # 1. Hydrology calculation
        catchment = Subcatchment(
            id=f"CATCH_{profile.city_id}",
            area_hectares=sc.catchment_area_ha,
            imperviousness_percent=sc.imperviousness_percent,
            slope_percent=1.2,
        )
        storm = RainfallEvent(
            return_period=ReturnPeriodYears.FIFTY_YEAR,
            duration_minutes=60,
            intensity_mm_per_hr=sc.cloudburst_intensity_mm_hr,
        )
        q_peak = HydrologicalProcessor.calculate_rational_peak_discharge(catchment, storm)

        # 2. Conduit capacity
        conduit = StormConduit(
            conduit_id=f"CONDUIT_{profile.city_id}",
            from_node="INLET_HUB",
            to_node="OUTFALL_RIVER",
            length_meters=1200.0,
            diameter_meters=sc.trunk_drain_dia_m,
            slope=0.003,
            manning_roughness=0.015,
        )
        eval_conduit = ConduitHydraulicSurrogate.evaluate_conduit_capacity(conduit, q_peak)

        # 3. Inundation Damage Baseline
        zone_baseline = InundationZone(
            zone_id=f"ZONE_{profile.city_id}",
            zone_name=sc.zone_name,
            surface_area_sqm=sc.catchment_area_ha * 10000.0 * 0.15,
            ground_elevation_m=12.0,
            water_level_m=12.0 + sc.baseline_flood_depth_m,
            inundation_depth_m=sc.baseline_flood_depth_m,
            flood_volume_m3=sc.baseline_flood_volume_m3,
            hazard_category="CRITICAL",
        )
        asset_sample = [
            AssetVulnerability(
                asset_id="ASSET-01",
                asset_name=f"{profile.city_name} Urban Transport, Commercial & Residential Hub",
                asset_type="COMMERCIAL_OFFICE",
                replacement_cost_cr=sc.vulnerable_assets_value_cr,
            )
        ]
        base_risk_rep = inundation_engine.evaluate_inundation_damage(zone_baseline, asset_sample)
        base_loss_cr = base_risk_rep.total_economic_loss_cr

        # 4. Post-Intervention Simulation
        attenuated_q = q_peak * (1.0 - (sc.flood_peak_attenuation_percent / 100.0))
        zone_post = InundationZone(
            zone_id=f"ZONE_POST_{profile.city_id}",
            zone_name=sc.zone_name,
            surface_area_sqm=sc.catchment_area_ha * 10000.0 * 0.15,
            ground_elevation_m=12.0,
            water_level_m=12.0 + sc.post_intervention_flood_depth_m,
            inundation_depth_m=sc.post_intervention_flood_depth_m,
            flood_volume_m3=sc.baseline_flood_volume_m3 * (1.0 - (sc.flood_peak_attenuation_percent / 100.0)),
            hazard_category="LOW",
        )
        post_risk_rep = inundation_engine.evaluate_inundation_damage(zone_post, asset_sample)
        post_loss_cr = post_risk_rep.total_economic_loss_cr

        damage_prevented_cr = max(0.0, base_loss_cr - post_loss_cr)

        # 5. Groundwater recharge valuation
        recharge_res = recharge_engine.compute_recharge_potential(
            catchment_area_ha=sc.catchment_area_ha,
            annual_rainfall_mm=sc.annual_rainfall_mm,
            recharge_efficiency=0.65,
        )

        net_benefit_cr = damage_prevented_cr + (recharge_res.monetary_water_value_inr_cr * 5.0)  # 5-year water benefit
        bcr = net_benefit_cr / sc.capex_cost_inr_cr if sc.capex_cost_inr_cr > 0 else 0.0

        return CitySimulationResult(
            city_id=profile.city_id,
            city_name=profile.city_name,
            municipal_authority=profile.municipal_authority,
            zone_name=sc.zone_name,
            catchment_area_ha=sc.catchment_area_ha,
            peak_inflow_discharge_m3s=round(q_peak, 2),
            conduit_capacity_m3s=round(eval_conduit["full_capacity_m3s"], 2),
            baseline_flood_depth_m=round(sc.baseline_flood_depth_m, 2),
            baseline_flood_volume_m3=round(sc.baseline_flood_volume_m3, 0),
            baseline_economic_loss_cr=round(base_loss_cr, 2),
            recommended_intervention=sc.recommended_intervention,
            capex_cost_cr=round(sc.capex_cost_inr_cr, 2),
            attenuated_peak_flow_m3s=round(attenuated_q, 2),
            post_intervention_flood_depth_m=round(sc.post_intervention_flood_depth_m, 2),
            flood_damage_prevented_cr=round(damage_prevented_cr, 2),
            annual_groundwater_recharge_mld=round(sc.annual_groundwater_recharge_mld, 2),
            annual_water_value_cr=round(recharge_res.monetary_water_value_inr_cr, 2),
            net_municipal_benefit_cr=round(net_benefit_cr, 2),
            benefit_cost_ratio_bcr=round(bcr, 2),
            wrai_remediation_summary=sc.wrai_algorithmic_solution,
        )

    def run_all_pilots(self) -> WRAIPilotReport:
        all_results = []
        tot_area = 0.0
        tot_base_loss = 0.0
        tot_capex = 0.0
        tot_saved = 0.0
        tot_water_mld = 0.0
        tot_water_val = 0.0
        tot_bcr = 0.0

        for cid, profile in PILOT_CITIES.items():
            res = self.evaluate_city(profile)
            all_results.append(res)
            tot_area += res.catchment_area_ha
            tot_base_loss += res.baseline_economic_loss_cr
            tot_capex += res.capex_cost_cr
            tot_saved += res.flood_damage_prevented_cr
            tot_water_mld += res.annual_groundwater_recharge_mld
            tot_water_val += res.annual_water_value_cr
            tot_bcr += res.benefit_cost_ratio_bcr

        count = len(all_results)
        return WRAIPilotReport(
            total_cities_audited=count,
            total_catchment_area_ha=round(tot_area, 1),
            total_baseline_damage_risk_cr=round(tot_base_loss, 2),
            total_intervention_capex_cr=round(tot_capex, 2),
            total_flood_damage_prevented_cr=round(tot_saved, 2),
            total_annual_water_harvested_mld=round(tot_water_mld, 2),
            total_annual_water_value_cr=round(tot_water_val, 2),
            average_benefit_cost_ratio=round(tot_bcr / count, 2) if count > 0 else 0.0,
            results=all_results,
        )


wrai_pilot_evaluator = WRAIPilotEvaluatorEngine()
