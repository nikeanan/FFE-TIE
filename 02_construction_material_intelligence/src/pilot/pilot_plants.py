"""Real-World RMC & EPC Contractor Plant Personas for Live Pilot Demonstration."""
from typing import Dict, List, Optional
from pydantic import BaseModel


class PilotBatchScenario(BaseModel):
    batch_id: str
    project_name: str
    epc_client: str
    target_grade: str
    structure_element: str
    monthly_volume_m3: float
    target_fck_28d: float
    design_cement_kg: float
    design_flyash_kg: float
    design_ggbs_kg: float
    design_water_liters: float
    measured_sand_moisture_pct: float
    scale_drift_cement_kg: float
    curing_ambient_temp_c: float
    typical_plant_issue: str
    cmi_remediation: str
    optimized_cement_kg: float


class PilotPlantProfile(BaseModel):
    plant_id: str
    plant_name: str
    operator_name: str
    location: str
    scada_brand: str
    monthly_production_m3: float
    cement_price_per_bag_inr: float
    scenario: PilotBatchScenario


PILOT_PLANTS: Dict[str, PilotPlantProfile] = {
    "plant_lt_metro": PilotPlantProfile(
        plant_id="plant_lt_metro",
        plant_name="L&T Heavy Civil Casting Yard #02",
        operator_name="Larsen & Toubro Ltd",
        location="Delhi-Meerut RRTS Package 3",
        scada_brand="BHS-Sonthofen 2.5 m³ Twin-Shaft",
        monthly_production_m3=9500.0,
        cement_price_per_bag_inr=365.0,
        scenario=PilotBatchScenario(
            batch_id="TICKET-RRTS-M45-104",
            project_name="Delhi-Meerut Regional Rapid Transit System",
            epc_client="National Capital Region Transport Corp (NCRTC)",
            target_grade="M45",
            structure_element="Pre-cast Segmental Box Girder",
            monthly_volume_m3=9500.0,
            target_fck_28d=53.25,
            design_cement_kg=420.0,
            design_flyash_kg=60.0,
            design_ggbs_kg=0.0,
            design_water_liters=155.0,
            measured_sand_moisture_pct=5.2,
            scale_drift_cement_kg=12.0,  # Over-dosing by 12 kg/m3 as safety buffer
            curing_ambient_temp_c=34.0,
            typical_plant_issue="Plant over-dosing 14 kg cement/m³ due to fear of low 7-day strength; unmetered aggregate moisture causing 0.44 W/C drift.",
            cmi_remediation="Physics-informed moisture compensation + Nurse-Saul maturity tracking allows cutting 15 kg/m³ cement while guaranteeing early de-shuttering.",
            optimized_cement_kg=405.0,
        ),
    ),
    "plant_tata_highrise": PilotPlantProfile(
        plant_id="plant_tata_highrise",
        plant_name="Tata Projects Urban RMC Hub",
        operator_name="Tata Projects Ltd",
        location="Bandra-Kurla Complex (BKC), Mumbai",
        scada_brand="Schwing Stetter CP30",
        monthly_production_m3=12000.0,
        cement_price_per_bag_inr=380.0,
        scenario=PilotBatchScenario(
            batch_id="TICKET-BKC-M50-Core",
            project_name="Commercial Tower 60-Story Core Wall",
            epc_client="Brookfield Properties",
            target_grade="M50",
            structure_element="Pumpable Shear Wall (180m Pumping Height)",
            monthly_volume_m3=12000.0,
            target_fck_28d=58.25,
            design_cement_kg=450.0,
            design_flyash_kg=80.0,
            design_ggbs_kg=40.0,
            design_water_liters=150.0,
            measured_sand_moisture_pct=4.8,
            scale_drift_cement_kg=-6.0,  # Scale under-weighing by 6 kg
            curing_ambient_temp_c=31.0,
            typical_plant_issue="Cement silo load cell drifting -1.3%, risking strength failure on critical shear wall cubes.",
            cmi_remediation="IS 4926 scale tolerance alarm triggers immediate auto-tare calibration; SCM ratio optimized to achieve 61.4 MPa 28d strength.",
            optimized_cement_kg=432.0,
        ),
    ),
    "plant_afcons_marine": PilotPlantProfile(
        plant_id="plant_afcons_marine",
        plant_name="Afcons Marine Concrete Batching Unit",
        operator_name="Afcons Infrastructure Ltd",
        location="Okha-Bet Dwarka Signature Bridge, Gujarat",
        scada_brand="Liebherr Betomix 2.25 m³",
        monthly_production_m3=7000.0,
        cement_price_per_bag_inr=370.0,
        scenario=PilotBatchScenario(
            batch_id="TICKET-DWK-M40-Pier",
            project_name="Marine Viaduct & Cable-Stayed Pier Pylons",
            epc_client="National Highways Authority of India (NHAI)",
            target_grade="M40",
            structure_element="Submerged Marine Pier Cap (Extreme Exposure)",
            monthly_volume_m3=7000.0,
            target_fck_28d=48.25,
            design_cement_kg=380.0,
            design_flyash_kg=0.0,
            design_ggbs_kg=120.0,
            design_water_liters=145.0,
            measured_sand_moisture_pct=6.1,
            scale_drift_cement_kg=8.0,
            curing_ambient_temp_c=29.0,
            typical_plant_issue="Severe chloride attack environment requires strict W/B < 0.40; high sand moisture (6.1%) was driving effective W/C to 0.435.",
            cmi_remediation="Live moisture deduction reduces metered water by 42 L/batch, restoring W/B to 0.380 and ensuring 100% IS 456 Table 5 compliance.",
            optimized_cement_kg=365.0,
        ),
    ),
    "plant_dilip_expressway": PilotPlantProfile(
        plant_id="plant_dilip_expressway",
        plant_name="Dilip Buildcon High-Volume PQC Plant",
        operator_name="Dilip Buildcon Ltd",
        location="Delhi-Mumbai Expressway Package 14",
        scada_brand="Apollo Infratech 120 m³/hr",
        monthly_production_m3=18500.0,
        cement_price_per_bag_inr=350.0,
        scenario=PilotBatchScenario(
            batch_id="TICKET-DME-M35-PQC",
            project_name="8-Lane Greenfield Expressway Mainline",
            epc_client="NHAI Highway Division",
            target_grade="M35",
            structure_element="Pavement Quality Concrete (PQC Slab 300mm)",
            monthly_volume_m3=18500.0,
            target_fck_28d=43.25,
            design_cement_kg=360.0,
            design_flyash_kg=50.0,
            design_ggbs_kg=0.0,
            design_water_liters=140.0,
            measured_sand_moisture_pct=3.9,
            scale_drift_cement_kg=16.0,  # Major cement buffer over-batching
            curing_ambient_temp_c=38.0,
            typical_plant_issue="Heavy over-cementing (16 kg/m³) to guard against flexural strength penalties on highway slipform paving.",
            cmi_remediation="Precision aggregate gradation & PCE admixture tuning saves 18 kg/m³ cement while meeting 4.5 MPa flexural strength standard.",
            optimized_cement_kg=342.0,
        ),
    ),
    "plant_nhpc_hydel": PilotPlantProfile(
        plant_id="plant_nhpc_hydel",
        plant_name="NHPC Hydro Mass Concrete Plant",
        operator_name="NHPC Limited / Patel Engineering",
        location="Parbati Hydroelectric Project Stage-II, Himachal",
        scada_brand="Simem MMX 5000",
        monthly_production_m3=6500.0,
        cement_price_per_bag_inr=390.0,
        scenario=PilotBatchScenario(
            batch_id="TICKET-NHPC-M25-Dam",
            project_name="Concrete Gravity Dam & Surge Shaft",
            epc_client="Ministry of Power, Govt of India",
            target_grade="M25",
            structure_element="Mass Concrete Dam Body Block",
            monthly_volume_m3=6500.0,
            target_fck_28d=31.60,
            design_cement_kg=270.0,
            design_flyash_kg=90.0,
            design_ggbs_kg=0.0,
            design_water_liters=145.0,
            measured_sand_moisture_pct=4.2,
            scale_drift_cement_kg=5.0,
            curing_ambient_temp_c=16.0,  # Cold weather mountain curing
            typical_plant_issue="Cold ambient mountain temperatures (16°C) cause slow strength gain; thermal gradient risks micro-cracking.",
            cmi_remediation="Nurse-Saul maturity engine predicts exact maturity index (degree-hours) ensuring formwork is not stripped prematurely in winter.",
            optimized_cement_kg=258.0,
        ),
    ),
}
