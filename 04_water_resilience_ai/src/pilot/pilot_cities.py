"""Production-Grade Smart City & Municipal Corporation Personas for WaterResilience AI Pilot Audits."""
from typing import Dict, List
from pydantic import BaseModel
from ..schema import ReturnPeriodYears, InterventionType


class PilotCityScenario(BaseModel):
    zone_name: str
    catchment_area_ha: float
    imperviousness_percent: float
    annual_rainfall_mm: float
    cloudburst_intensity_mm_hr: float
    trunk_drain_dia_m: float
    baseline_flood_depth_m: float
    baseline_flood_volume_m3: float
    vulnerable_assets_value_cr: float
    
    # Intervention Strategy
    recommended_intervention: str
    intervention_type: InterventionType
    capex_cost_inr_cr: float
    flood_peak_attenuation_percent: float
    post_intervention_flood_depth_m: float
    annual_groundwater_recharge_mld: float
    
    # Root Cause & Remediation
    urban_drainage_bottleneck: str
    wrai_algorithmic_solution: str


class PilotCityProfile(BaseModel):
    city_id: str
    city_name: str
    municipal_authority: str
    smart_city_mission_lead: str
    state: str
    scenario: PilotCityScenario


PILOT_CITIES: Dict[str, PilotCityProfile] = {
    "CITY_BENGALURU_BBMP": PilotCityProfile(
        city_id="CITY_BENGALURU_BBMP",
        city_name="Bengaluru (Bangalore)",
        municipal_authority="Bruhat Bengaluru Mahanagara Palike (BBMP) / BWSSB",
        smart_city_mission_lead="Chief Engineer (Stormwater Drains & Lakes), BBMP",
        state="Karnataka",
        scenario=PilotCityScenario(
            zone_name="Bellandur-Varthur Lake Basin & Outer Ring Road (ORR) Eco-Space Tech Corridor",
            catchment_area_ha=320.0,
            imperviousness_percent=88.0,
            annual_rainfall_mm=970.0,
            cloudburst_intensity_mm_hr=92.0,
            trunk_drain_dia_m=2.2,
            baseline_flood_depth_m=1.35,
            baseline_flood_volume_m3=148000.0,
            vulnerable_assets_value_cr=850.0,
            recommended_intervention="Sponge City Cascade: 3 Interlinked Micro-Detention Wetlands + Permeable Tech-Park Corridors",
            intervention_type=InterventionType.BLUE_GREEN_SUDS,
            capex_cost_inr_cr=18.5,
            flood_peak_attenuation_percent=62.0,
            post_intervention_flood_depth_m=0.18,  # Below damage threshold
            annual_groundwater_recharge_mld=4.85,
            urban_drainage_bottleneck="Encroachment of rajakaluves (natural storm canals) and 88% asphalt imperviousness causing repeated ORR tech-park shutdowns during 50-year storm events.",
            wrai_algorithmic_solution="Optimized hybrid 1D/2D hydrodynamic surrogate identified 3 natural depression zones for micro-wetlands, reducing peak runoff from 72 m³/s to 27 m³/s while recharging 4.85 MLD into deep aquifer wells.",
        ),
    ),
    "CITY_MUMBAI_BMC": PilotCityProfile(
        city_id="CITY_MUMBAI_BMC",
        city_name="Mumbai",
        municipal_authority="Brihanmumbai Municipal Corporation (BMC) / SWD Dept",
        smart_city_mission_lead="Deputy Municipal Commissioner (Storm Water Drains), BMC",
        state="Maharashtra",
        scenario=PilotCityScenario(
            zone_name="Mithi River Basin & Hindmata - Gandhi Market Low-Lying Inundation Bowl",
            catchment_area_ha=480.0,
            imperviousness_percent=92.0,
            annual_rainfall_mm=2450.0,
            cloudburst_intensity_mm_hr=120.0,
            trunk_drain_dia_m=2.8,
            baseline_flood_depth_m=1.65,
            baseline_flood_volume_m3=295000.0,
            vulnerable_assets_value_cr=1450.0,
            recommended_intervention="Dual Underground Storm Holding Tanks (Pramod Mahajan Park) + High-Discharge Archimedes Pumps",
            intervention_type=InterventionType.GRAY_INFRASTRUCTURE,
            capex_cost_inr_cr=45.0,
            flood_peak_attenuation_percent=74.0,
            post_intervention_flood_depth_m=0.22,
            annual_groundwater_recharge_mld=6.20,
            urban_drainage_bottleneck="Tidal backwater lock during high tide (>4.5m) coincides with intense monsoon cloudbursts, paralyzing suburban railway and Central Mumbai traffic.",
            wrai_algorithmic_solution="Dynamic tidal gate scheduling coupled with physics-surrogate retention basin routing buffers 180,000 m³ of storm peak during high-tide locks, completely preventing road inundation.",
        ),
    ),
    "CITY_CHENNAI_GCC": PilotCityProfile(
        city_id="CITY_CHENNAI_GCC",
        city_name="Chennai",
        municipal_authority="Greater Chennai Corporation (GCC) / Water Resources Dept",
        smart_city_mission_lead="Superintending Engineer (Special Projects & Smart City), GCC",
        state="Tamil Nadu",
        scenario=PilotCityScenario(
            zone_name="Velachery Lake & Old Mahabalipuram Road (OMR) IT Corridor Basin",
            catchment_area_ha=390.0,
            imperviousness_percent=84.0,
            annual_rainfall_mm=1400.0,
            cloudburst_intensity_mm_hr=105.0,
            trunk_drain_dia_m=2.4,
            baseline_flood_depth_m=1.45,
            baseline_flood_volume_m3=210000.0,
            vulnerable_assets_value_cr=980.0,
            recommended_intervention="Velachery Surplus Canal Widening + 12 Deep Recharge Wells in Pallikaranai Marshland Buffer",
            intervention_type=InterventionType.LAKE_CASCADE_RESTORATION,
            capex_cost_inr_cr=26.0,
            flood_peak_attenuation_percent=68.0,
            post_intervention_flood_depth_m=0.15,
            annual_groundwater_recharge_mld=5.40,
            urban_drainage_bottleneck="Cyclone Michaung type extreme precipitation overwhelmed Velachery surplus canal, flooding 45 residential colonies and commercial IT parks.",
            wrai_algorithmic_solution="Calibrated multi-catchment hydrographs restored hydraulic flow capacity from 28 m³/s to 64 m³/s, safeguarding ₹980 Cr asset base and harvesting 5.4 MLD freshwater.",
        ),
    ),
    "CITY_GURUGRAM_GMDA": PilotCityProfile(
        city_id="CITY_GURUGRAM_GMDA",
        city_name="Gurugram (NCR)",
        municipal_authority="Gurugram Metropolitan Development Authority (GMDA) / MCG",
        smart_city_mission_lead="Chief Engineer (Infrastructure), GMDA",
        state="Haryana",
        scenario=PilotCityScenario(
            zone_name="Subhash Chowk, Golf Course Ext Road & Badshahpur Outfall Catchment",
            catchment_area_ha=260.0,
            imperviousness_percent=86.0,
            annual_rainfall_mm=720.0,
            cloudburst_intensity_mm_hr=85.0,
            trunk_drain_dia_m=1.8,
            baseline_flood_depth_m=1.10,
            baseline_flood_volume_m3=115000.0,
            vulnerable_assets_value_cr=620.0,
            recommended_intervention="Aravalli Ridge Check Dams + Bioswales & Urban Recharge Shafts along NH-48",
            intervention_type=InterventionType.MANAGED_AQUIFER_RECHARGE,
            capex_cost_inr_cr=12.8,
            flood_peak_attenuation_percent=58.0,
            post_intervention_flood_depth_m=0.12,
            annual_groundwater_recharge_mld=3.80,
            urban_drainage_bottleneck="Rapid urban expansion blocked natural drainage channels from Aravalli foothills into Badshahpur drain, triggering multi-kilometer gridlocks on Hero Honda Chowk and Subhash Chowk.",
            wrai_algorithmic_solution="Decentralized upstream retention in Aravalli foothills combined with roadside bioswales captures 65,000 m³ storm runoff at source, elevating falling groundwater table by 2.4 meters.",
        ),
    ),
    "CITY_HYDERABAD_GHMC": PilotCityProfile(
        city_id="CITY_HYDERABAD_GHMC",
        city_name="Hyderabad",
        municipal_authority="Greater Hyderabad Municipal Corporation (GHMC) / SNDP",
        smart_city_mission_lead="Strategic Nala Development Programme (SNDP) Director, GHMC",
        state="Telangana",
        scenario=PilotCityScenario(
            zone_name="Begumpet Nala, Balkapur Channel & Hussain Sagar Inflow Basin",
            catchment_area_ha=350.0,
            imperviousness_percent=82.0,
            annual_rainfall_mm=820.0,
            cloudburst_intensity_mm_hr=90.0,
            trunk_drain_dia_m=2.0,
            baseline_flood_depth_m=1.25,
            baseline_flood_volume_m3=160000.0,
            vulnerable_assets_value_cr=740.0,
            recommended_intervention="Strategic Nala Retaining Walls + 4 Micro-Sponge Parks in Municipal Playgrounds",
            intervention_type=InterventionType.BLUE_GREEN_SUDS,
            capex_cost_inr_cr=19.2,
            flood_peak_attenuation_percent=65.0,
            post_intervention_flood_depth_m=0.14,
            annual_groundwater_recharge_mld=4.20,
            urban_drainage_bottleneck="Hussain Sagar surplus weir backflow and constricted Begumpet nala cross-sections causing severe flooding in residential colonies and Begumpet airport road.",
            wrai_algorithmic_solution="Coupled Saint-Venant 1D/2D surrogate modeled optimal weir discharge gates and converted 4 public parks into dual-use dry detention ponds, eliminating flash flooding.",
        ),
    ),
}
