"""Production-Grade Mega-Project Contractor Personas for CECI Proof-of-Value Audits."""
from typing import Dict, List
from datetime import date
from pydantic import BaseModel
from ..schema import ArtifactType, ContractClause, DelayCategory, DelayEvent, EscalationComponent


class PilotClaimScenario(BaseModel):
    project_name: str
    client_authority: str
    contract_type: str
    tender_contract_value_cr: float
    
    # BOQ Variation Data
    boq_item_no: str
    boq_description: str
    unit: str
    tender_qty: float
    executed_qty: float
    tender_rate_inr: float
    
    # Delay / EoT Scenario
    delay_title: str
    delay_category: DelayCategory
    delay_days: int
    daily_site_overhead_inr: float
    daily_ld_risk_inr: float
    
    # Escalation Scenario
    escalation_component: EscalationComponent
    base_material_rate_inr: float
    material_quantity_consumed: float
    base_wpi_index: float
    current_wpi_index: float
    
    # Root Cause & Remediation
    dispute_root_cause: str
    ceci_algorithmic_remediation: str


class PilotContractorProfile(BaseModel):
    contractor_id: str
    contractor_name: str
    headquarters: str
    project_division: str
    lead_contract_specialist: str
    scenario: PilotClaimScenario


PILOT_CONTRACTORS: Dict[str, PilotContractorProfile] = {
    "CONTRACTOR_LNT_METRO": PilotContractorProfile(
        contractor_id="CONTRACTOR_LNT_METRO",
        contractor_name="Larsen & Toubro Ltd (Heavy Civil Infra IC)",
        headquarters="Mumbai / NCR Operations Hub",
        project_division="Urban Transit & Metro Rail",
        lead_contract_specialist="Er. Rajeshwer Rao, Chief Contracts Manager",
        scenario=PilotClaimScenario(
            project_name="Delhi-Meerut Regional Rapid Transit System (RRTS) Viaduct Package 03",
            client_authority="National Capital Region Transport Corporation (NCRTC)",
            contract_type="FIDIC Conditions of Contract for Construction (Red Book 1999)",
            tender_contract_value_cr=1240.0,
            boq_item_no="04.12",
            boq_description="Bored Cast-in-Situ RC Piles 1200mm Dia in Extremely Hard Quartzite Rock (>80 MPa)",
            unit="RMT",
            tender_qty=2400.0,
            executed_qty=3360.0,
            tender_rate_inr=18500.0,
            delay_title="Delay in Shifting Unmapped 220kV Underground Gas Insulated Lines and Metro Corridor Handover",
            delay_category=DelayCategory.EMPLOYER_RISK,
            delay_days=68,
            daily_site_overhead_inr=145000.0,
            daily_ld_risk_inr=220000.0,
            escalation_component=EscalationComponent.STEEL_TMT,
            base_material_rate_inr=54000.0,  # INR per MT
            material_quantity_consumed=420.0,  # MT
            base_wpi_index=128.4,
            current_wpi_index=146.2,
            dispute_root_cause="Client Engineer refused to certify 960 RMT excess pile depth variation and threatened liquidated damages for 68-day viaduct delay caused by unmapped utility line shifting.",
            ceci_algorithmic_remediation="Auto-synthesized CPWD Cl 12 / FIDIC 13 variation dossier linking borehole core test logs and certified MB entries. Computed ₹1.77 Cr variation + ₹98.6 Lakh prolongation recovery while completely shielding contractor from ₹1.49 Cr LD liability.",
        ),
    ),
    "CONTRACTOR_TATA_COASTAL": PilotContractorProfile(
        contractor_id="CONTRACTOR_TATA_COASTAL",
        contractor_name="Tata Projects Ltd (Marine Infra SBU)",
        headquarters="Mumbai, Maharashtra",
        project_division="Bridges & Coastal Structures",
        lead_contract_specialist="Vikramaditya Kulkarni, Head of Claims & Arbitration",
        scenario=PilotClaimScenario(
            project_name="Mumbai Coastal Road Sea-Link Interchange & Pier Package",
            client_authority="Brihanmumbai Municipal Corporation (BMC)",
            contract_type="EPC Contract Agreement / FIDIC Yellow Book",
            tender_contract_value_cr=1850.0,
            boq_item_no="07.03",
            boq_description="High-Performance M60 Grade Marine Concrete with Silica Fume & Polycarboxylate Admixtures",
            unit="CUM",
            tender_qty=18000.0,
            executed_qty=23400.0,
            tender_rate_inr=9200.0,
            delay_title="Severe Marine Cyclone Tauktae & Extended High-Tide Work Restriction Orders",
            delay_category=DelayCategory.FORCE_MAJEURE,
            delay_days=45,
            daily_site_overhead_inr=180000.0,
            daily_ld_risk_inr=250000.0,
            escalation_component=EscalationComponent.CEMENT,
            base_material_rate_inr=6800.0,  # INR per Tonne
            material_quantity_consumed=3100.0,  # Tonnes
            base_wpi_index=131.0,
            current_wpi_index=149.3,
            dispute_root_cause="Client withheld payment for 5,400 m³ additional concrete executed in tidal wave protection bunds and disputed cyclone force majeure notice validity under Clause 19.",
            ceci_algorithmic_remediation="Generated tamper-evident Multi-Modal Evidence Dossier linking IMD weather cyclone radar maps, Port Authority marine safety alerts, and drone batch pour footage, securing 45-day non-penal Extension of Time and ₹4.96 Cr variation clearance.",
        ),
    ),
    "CONTRACTOR_DILIP_NHAI": PilotContractorProfile(
        contractor_id="CONTRACTOR_DILIP_NHAI",
        contractor_name="Dilip Buildcon Ltd (Highways IC)",
        headquarters="Bhopal, Madhya Pradesh",
        project_division="Expressway & Highway Pavements",
        lead_contract_specialist="Sanjay Agrawal, Chief Commercial Officer",
        scenario=PilotClaimScenario(
            project_name="Delhi-Mumbai Expressway Package 14 (6-Lane Access Controlled Green Field Corridor)",
            client_authority="National Highways Authority of India (NHAI)",
            contract_type="HAM (Hybrid Annuity Model) / EPC Standard Model",
            tender_contract_value_cr=1420.0,
            boq_item_no="02.08",
            boq_description="Embankment Construction with Fly Ash & Granular Soil Borrow Pit Stabilization",
            unit="CUM",
            tender_qty=850000.0,
            executed_qty=1080000.0,
            tender_rate_inr=320.0,
            delay_title="Non-Availability of ROW (Right of Way) Kilometer 142 to 158 Due to Land Acquisition Injunction",
            delay_category=DelayCategory.EMPLOYER_RISK,
            delay_days=82,
            daily_site_overhead_inr=125000.0,
            daily_ld_risk_inr=190000.0,
            escalation_component=EscalationComponent.BITUMEN,
            base_material_rate_inr=42000.0,  # INR per MT (VG-30/40)
            material_quantity_consumed=1850.0,  # MT
            base_wpi_index=119.5,
            current_wpi_index=142.8,
            dispute_root_cause="NHAI regional office denied bitumen price escalation (Clause 10CA) and penalized contractor for slow progress on encumbered stretch.",
            ceci_algorithmic_remediation="Computed statutory NHAI Schedule J variation (+27.0% earthwork deviation = ₹7.36 Cr) and compiled ₹91.2 Lakh Bitumen escalation claim backed by refinery invoice audits and GIS land parcel hindrance timelines.",
        ),
    ),
    "CONTRACTOR_AFCONS_JETTY": PilotContractorProfile(
        contractor_id="CONTRACTOR_AFCONS_JETTY",
        contractor_name="Afcons Infrastructure Ltd (Marine & Offshore)",
        headquarters="Mumbai / Vizag Project Office",
        project_division="Ports, Marine Terminals & Dredging",
        lead_contract_specialist="Capt. R. Nambiar, Vice President Marine Projects",
        scenario=PilotClaimScenario(
            project_name="Visakhapatnam Deepwater Container Berth Expansion Package",
            client_authority="Visakhapatnam Port Authority (VPA)",
            contract_type="FIDIC Red Book / Port Trust Standard EPC",
            tender_contract_value_cr=980.0,
            boq_item_no="01.15",
            boq_description="Capital Dredging in Hard Compact Rock & Basalt Seabed Strata (-18m CD)",
            unit="CUM",
            tender_qty=120000.0,
            executed_qty=168000.0,
            tender_rate_inr=2200.0,
            delay_title="Berthing Naval Vessel Traffic Interruption and Delayed Seabed Demarcation Clearance",
            delay_category=DelayCategory.EMPLOYER_RISK,
            delay_days=54,
            daily_site_overhead_inr=210000.0,  # Heavy marine dredger vessel day rate
            daily_ld_risk_inr=280000.0,
            escalation_component=EscalationComponent.POL_FUEL,
            base_material_rate_inr=88.0,  # High Speed Diesel INR/Liter
            material_quantity_consumed=480000.0,  # Liters
            base_wpi_index=112.0,
            current_wpi_index=133.2,
            dispute_root_cause="Port Engineer disputed seabed geological profile anomaly requiring heavy cutter-suction dredging and disallowed dredging vessel idling compensation.",
            ceci_algorithmic_remediation="Generated comprehensive seabed bathymetric difference model and cutterhead torque sensor logs, proving physical obstruction under FIDIC Clause 4.12 (Unforeseeable Physical Conditions), releasing ₹10.56 Cr variation and ₹1.13 Cr prolongation recovery.",
        ),
    ),
    "CONTRACTOR_MEGHA_TUNNEL": PilotContractorProfile(
        contractor_id="CONTRACTOR_MEGHA_TUNNEL",
        contractor_name="Megha Engineering & Infrastructures Ltd (MEIL)",
        headquarters="Hyderabad, Telangana",
        project_division="Hydroelectric & Underground Tunneling",
        lead_contract_specialist="K. Sudhakar Reddy, Executive Director Projects",
        scenario=PilotClaimScenario(
            project_name="Himalayan Hydroelectric Project Head Race Tunnel (HRT Package 2)",
            client_authority="NHPC Limited / SJVN Limited",
            contract_type="CPWD / Central Public Sector Undertaking EPC Standard",
            tender_contract_value_cr=2100.0,
            boq_item_no="08.05",
            boq_description="Underground Rock Bolting, Steel Rib Supports & Shotcrete Lining in Shear Zone (Class V Rock)",
            unit="MT",
            tender_qty=3200.0,
            executed_qty=4480.0,
            tender_rate_inr=84000.0,
            delay_title="Unforeseen Major Fault Zone Shear Ingress and Water Gushing Geological Anomaly",
            delay_category=DelayCategory.EMPLOYER_RISK,
            delay_days=95,
            daily_site_overhead_inr=160000.0,
            daily_ld_risk_inr=310000.0,
            escalation_component=EscalationComponent.STEEL_TMT,
            base_material_rate_inr=56000.0,  # INR per MT
            material_quantity_consumed=1280.0,  # MT
            base_wpi_index=125.0,
            current_wpi_index=147.5,
            dispute_root_cause="CPSU Engineer withheld certification for extra rock support ribs, arguing contractor should have anticipated Himalayan thrust fault geology during tender bidding.",
            ceci_algorithmic_remediation="Synthesized 3D geological encounter logs against initial tender DPR borings, proving latent site anomaly. Secured ₹10.75 Cr steel support variation, ₹1.52 Cr prolongation cost claim, and total exemption from ₹2.94 Cr liquidated damages.",
        ),
    ),
}
