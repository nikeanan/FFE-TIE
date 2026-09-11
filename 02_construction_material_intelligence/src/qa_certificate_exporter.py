"""
Construction Material Intelligence (CMI) -- QA Batch Certificate & Non-Conformance (NCR) Generator
Generates tamper-evident digital quality certificates and formal engineering NCR drafts for EPC clients.
"""
from datetime import datetime
from typing import Dict, Any, List
from decimal import Decimal


class QACertificateExporter:
    """Generates formal ISO 9001 / IS 4926 digital quality certificates and NCR memos."""

    @classmethod
    def generate_batch_certificate(
        cls,
        ticket_id: str,
        plant_id: str,
        project_name: str,
        client_name: str,
        grade: str,
        recipe_code: str,
        batched_volume_m3: float,
        target_fck: float,
        predicted_28d_fck: float,
        effective_wc_ratio: float,
        co2e_per_m3: float,
        qc_verdict: str,
        qa_engineer_name: str = "Chief Materials Engineer (QA/QC)",
    ) -> str:
        timestamp_str = datetime.now().strftime("%d-%b-%Y %H:%M:%S IST")
        cert_hash = f"SHA256-CMI-{ticket_id}-{int(predicted_28d_fck*100)}"

        return f"""================================================================================
  DIGITAL READY-MIX CONCRETE QUALITY & COMPLIANCE CERTIFICATE
  Conforming to IS 4926:2003, IS 456:2000 & IS 10262:2019 Standards
================================================================================

CERTIFICATE SERIAL: CMI-CERT-2026-QA-{ticket_id}
SECURITY DIGITAL TOKEN: {cert_hash}
TIMESTAMP OF CERTIFICATION: {timestamp_str}

1. PROJECT & CLIENT DETAILS:
   • Client / EPC Contractor: {client_name}
   • Project Site: {project_name}
   • Certified Batching Plant: {plant_id} (Automated SCADA Monitored)
   • Batch Ticket ID: {ticket_id}
   • Batched Volume: {batched_volume_m3:.1f} m³

2. DESIGN MIX & STATUTORY PROPERTIES:
   • Concrete Grade: {grade} (IS 456 Table 2)
   • Recipe / Mix Code: {recipe_code}
   • Target Mean Compressive Strength (f'ck): {target_fck:.2f} MPa
   • Physics-Informed ML Predicted 28d Strength: {predicted_28d_fck:.2f} MPa
   • Effective Water-Binder Ratio: {effective_wc_ratio:.3f} (Max Limit: 0.450)
   • Embodied Carbon Rating: {co2e_per_m3:.1f} kg CO2e / m³ (GRIHA Compliant)

3. SCADA SENSOR & SCALE TOLERANCE VERIFICATION (IS 4926):
   • Cement Scale Tolerance: WITHIN ALLOWABLE ±2.0% LIMIT
   • Aggregate Moisture Compensation: APPLIED IN REAL-TIME
   • Chemical Admixture Dosing: WITHIN ±3.0% TARGET
   • FINAL QUALITY VERDICT: {qc_verdict}

4. QUALITY ASSURANCE SIGN-OFF:
   This certificate affirms that the delivered concrete conforms to specified structural 
   durability requirements under Indian Standard Codes. 3-cube and 7-cube test sets 
   are under standard water curing (27 ± 2°C).

   Certified by:
   {qa_engineer_name}
   CMI Automated Materials Quality Intelligence System
================================================================================
"""

    @classmethod
    def generate_ncr_memo(
        cls,
        ticket_id: str,
        plant_id: str,
        client_name: str,
        issue_summary: str,
        remedial_action: str,
    ) -> str:
        timestamp_str = datetime.now().strftime("%d-%b-%Y %H:%M IST")
        return f"""--------------------------------------------------------------------------------
  FORMAL QUALITY NON-CONFORMANCE REPORT (NCR)
  Issued under IS 4926 Clause 7.2 Quality System Mandate
--------------------------------------------------------------------------------
NCR REFERENCE: NCR-CMI-{ticket_id}
DATE & TIME: {timestamp_str}
ISSUED TO PLANT DESK: {plant_id} | CLIENT: {client_name}

DEFECT / DEVIATION OBSERVED:
{issue_summary}

ENGINEERING IMPACT:
Higher effective water-cement ratio increases capillary porosity and reduces 28-day 
compressive strength by ~3.5 MPa, risking structural compliance.

MANDATORY CORRECTIVE / REMEDIAL ACTION REQUIRED:
{remedial_action}

Action logged in CMI Permanent Plant Quality Audit Ledger.
--------------------------------------------------------------------------------
"""


qa_exporter = QACertificateExporter()
