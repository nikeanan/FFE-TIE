import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from datetime import date
from src.schema import ArtifactType, BOQItem, EvidenceNode
from src.evidence_graph import CivilEvidenceGraph
from src.boq_discrepancy_detector import BOQDiscrepancyDetector
from src.claim_package_generator import ClaimDossierGenerator

st.set_page_config(
    page_title="Civil Engineering Evidence & Claims Intelligence",
    page_icon="⚖️",
    layout="wide",
)

st.title("⚖️ Civil Engineering Evidence & Claims Intelligence")
st.caption("Multi-Modal Evidence Knowledge Graph & Proactive Variation/Dispute Dossier Compiler")

tabs = st.tabs(["📊 BOQ Variation Auditor", "🕸️ Engineering Evidence Graph", "📑 Claim Dossier Compiler"])

# -----------------------------------------------------------------------------
# TAB 1: BOQ VARIATION AUDITOR
# -----------------------------------------------------------------------------
with tabs[0]:
    st.header("1. BOQ Quantity & Variation Deviation Auditor")
    st.markdown("Audits field quantities against CPWD Clause 12 and FIDIC Red Book Clause 13 deviation thresholds.")

    col1, col2 = st.columns(2)
    with col1:
        item_no = st.text_input("BOQ Item Number", "04.1")
        item_desc = st.text_input("Item Description", "Bored Cast-in-Situ Reinforced Concrete Piles 1200mm Dia in Hard Rock")
        unit = st.selectbox("Measurement Unit", ["RMT", "CUM", "SQM", "MT", "NOS"])
        tender_qty = st.number_input("Tender Contract Quantity", value=1200.0, step=100.0)
        executed_qty = st.number_input("Cumulative Executed Quantity on Site", value=1620.0, step=50.0)
        tender_rate = st.number_input("Agreed Tender Rate (INR)", value=14500.0, step=500.0)

    boq_item = BOQItem(
        item_id=f"BOQ-{item_no}",
        item_no=item_no,
        description=item_desc,
        unit=unit,
        tender_quantity=tender_qty,
        tender_rate=tender_rate,
        executed_quantity=executed_qty,
    )

    detector = BOQDiscrepancyDetector()
    findings = detector.analyze_quantities([boq_item])

    with col2:
        excess_qty = executed_qty - tender_qty
        excess_amount = max(0.0, excess_qty * tender_rate)
        dev_percent = (excess_qty / tender_qty) * 100.0 if tender_qty > 0 else 0.0

        st.subheader("Contractual Compliance Analysis")
        st.metric("Quantity Deviation", f"{dev_percent:+0.1f}%", f"{excess_qty:+0.1f} {unit}")
        st.metric("Total Executed Financial Value", f"INR {executed_qty * tender_rate:,.2f}")
        st.metric("Variation / Extra Claim Value", f"INR {excess_amount:,.2f}")

        if dev_percent > 25.0:
            st.error(f"🚨 **CRITICAL VARIATION EXCEEDED (>25% Limit):** Deviation of {dev_percent:.1f}% exceeds statutory limits. Initiate Substituted Item Rate Analysis under Clause 12 immediately.")
        elif dev_percent > 10.0:
            st.warning(f"⚠️ **VARIATION WARNING (>10%):** Issue advance notice of deviation to the Engineer-in-Charge.")
        else:
            st.success("✅ **Within Allowable Limits (<10%):** Routine RA bill certification permitted.")

# -----------------------------------------------------------------------------
# TAB 2: EVIDENCE GRAPH
# -----------------------------------------------------------------------------
with tabs[1]:
    st.header("2. Relational Engineering Evidence Graph")
    st.markdown("Visualizes primary engineering artifacts backing the item for bulletproof audit defense.")

    graph = CivilEvidenceGraph()
    graph.add_node(EvidenceNode(
        node_id=f"BOQ-{item_no}",
        artifact_type=ArtifactType.BOQ_ITEM,
        title=f"BOQ Item {item_no}",
        date_created=date(2025, 6, 1),
        reference_path="/contracts/tender_boq_vol2.pdf#p44"
    ))
    graph.add_node(EvidenceNode(
        node_id="DWG-STR-P04-R2",
        artifact_type=ArtifactType.DRAWING_REVISION,
        title="Substructure Pier P4 Pile Layout Rev-2 (Rock Level Adjusted)",
        date_created=date(2026, 2, 14),
        reference_path="/drawings/structural/DWG-STR-P04-R2.dwg"
    ))
    graph.add_node(EvidenceNode(
        node_id="MB-42-P18",
        artifact_type=ArtifactType.MEASUREMENT_BOOK_ENTRY,
        title="Measurement Book #42 Page 18-24 (Pile Depth Boring Logs)",
        date_created=date(2026, 7, 20),
        reference_path="/measurements/MB_42_certified.pdf"
    ))
    graph.add_node(EvidenceNode(
        node_id="PHOTO-PIER4-CORE",
        artifact_type=ArtifactType.SITE_PHOTO,
        title="Geo-tagged Rock Core Samples Pier 4 Deep Socketing",
        date_created=date(2026, 7, 21),
        reference_path="/site_media/geo_photos/IMG_20260721_1430.jpg"
    ))

    graph.link_artifacts("DWG-STR-P04-R2", f"BOQ-{item_no}", "REVISED_SPECIFICATION_FOR")
    graph.link_artifacts("MB-42-P18", f"BOQ-{item_no}", "CERTIFIES_EXECUTED_QUANTITY_OF")
    graph.link_artifacts("PHOTO-PIER4-CORE", f"BOQ-{item_no}", "VISUAL_EVIDENCE_FOR")

    audit_trail = graph.trace_audit_trail(f"BOQ-{item_no}")

    st.subheader(f"Evidence Trail for Item {item_no}")
    df_evidence = pd.DataFrame(audit_trail)
    st.table(df_evidence)

# -----------------------------------------------------------------------------
# TAB 3: CLAIM DOSSIER COMPILER
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("3. Automated Variation Claim Dossier")

    proj_name = st.text_input("Project Name", "Metro Elevated Viaduct Package EV-03")
    contractor = st.text_input("Contractor Name", "Apex Mega-Infra JV")
    client = st.text_input("Client / Authority", "State Metro Rail Corporation")

    dossier_text = ClaimDossierGenerator.generate_variation_claim_memo(
        project_name=proj_name,
        contractor_name=contractor,
        client_name=client,
        item_no=item_no,
        description=item_desc,
        tender_qty=tender_qty,
        executed_qty=executed_qty,
        unit=unit,
        rate=tender_rate,
        evidence_chain=audit_trail,
    )

    st.text_area("Audit-Ready Variation Dossier Draft:", dossier_text, height=320)
    st.download_button("📥 Download Dossier (.md)", dossier_text, file_name=f"Variation_Claim_Dossier_Item_{item_no}.md")
