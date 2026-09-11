from typing import List, Dict


class ClaimDossierGenerator:
    """Compiles structured, audit-ready variation and delay claim dossiers."""

    @staticmethod
    def generate_variation_claim_memo(
        project_name: str,
        contractor_name: str,
        client_name: str,
        item_no: str,
        description: str,
        tender_qty: float,
        executed_qty: float,
        unit: str,
        rate: float,
        evidence_chain: List[Dict],
    ) -> str:
        excess_qty = executed_qty - tender_qty
        excess_amount = excess_qty * rate

        evidence_md = "\n".join(
            [f"  - [{e['type']}] {e['title']} ({e['relation']}) | Ref: {e['reference']}" for e in evidence_chain]
        )

        return f"""
# VARIATION & QUANTITY DEVIATION JUSTIFICATION DOSSIER

**Project:** {project_name}  
**Contractor:** {contractor_name}  
**Client / Employer:** {client_name}  
**Clause Reference:** Clause 12 (Deviations / Variations)

---

## 1. Item Details
- **BOQ Item No:** {item_no}
- **Description:** {description}
- **Tender Agreed Quantity:** {tender_qty:,.2f} {unit}
- **Executed Quantity on Site:** {executed_qty:,.2f} {unit}
- **Excess Variation Quantity:** {excess_qty:,.2f} {unit} (+{((executed_qty - tender_qty) / tender_qty * 100):.1f}%)
- **Tender Rate:** INR {rate:,.2f} / {unit}
- **Claim Financial Value:** INR {excess_amount:,.2f}

## 2. Supporting Engineering Evidence Trail
The above executed quantity is verified and backed by the following primary field records:
{evidence_md}

## 3. Contractual Basis & Request for Certification
Since the deviation exceeds contractual limits, we formally request the Engineer-in-Charge to certify the Running Account (RA) bill along with the attached rate analysis.

Submitted by:
Chief Quantity Surveyor / Claims Head
{contractor_name}
"""
