import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from datetime import date, datetime

from src.schema import ArtifactType, BOQItem, EvidenceNode, ContractClause, DelayCategory, DelayEvent, EscalationComponent
from src.evidence_graph import CivilEvidenceGraph
from src.boq_discrepancy_detector import BOQDiscrepancyDetector
from src.claim_package_generator import ClaimDossierGenerator
from src.delay_analysis_engine import delay_engine
from src.price_escalation_engine import escalation_engine
from src.pilot.pilot_contractors import PILOT_CONTRACTORS
from src.pilot.pilot_evaluator import ceci_pilot_evaluator

st.set_page_config(
    page_title="CECI — Civil Evidence & Claims Intelligence",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-Aesthetic Theme Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .ceci-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #4338CA 100%);
        padding: 24px 32px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-card {
        background: #1E293B;
        border-radius: 12px;
        padding: 18px 20px;
        border-left: 4px solid #6366F1;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .kpi-val {
        font-size: 26px;
        font-weight: 700;
        color: #F8FAFC;
    }
    
    .kpi-lbl {
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94A3B8;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Main Banner Header
st.markdown("""
<div class="ceci-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.02em;">
                ⚖️ CECI <span style="font-size: 16px; font-weight: 500; color: #A5B4FC; margin-left: 10px;">Civil Evidence & Claims Intelligence</span>
            </h1>
            <p style="margin: 6px 0 0 0; color: #CBD5E1; font-size: 14px;">
                Multi-Modal Evidence Knowledge Graph • Time Impact Delay Analysis (TIA) • CPWD Clause 12/5/10CA/10CC • FIDIC 1999 Red/Yellow Book
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(99, 102, 241, 0.3); border: 1px solid #6366F1; color: #A5B4FC; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600;">
                🟢 Arbitral Legal Twin Online
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Context
with st.sidebar:
    st.subheader("🏢 Active Project Context")
    st.markdown("**Delhi-Meerut RRTS Viaduct PKG-03**")
    st.caption("NCRTC • EPC Contract • ₹ 1,240 Cr Contract Value")
    st.markdown("**Lead Contractor:** Larsen & Toubro Heavy Civil")
    st.markdown("**Contract Standard:** `FIDIC Red Book 1999`")
    st.markdown("**Claims Defense Status:** Active Monitoring")
    
    st.divider()
    st.subheader("⚡ Quick Control Actions")
    if st.button("🔄 Sync Site Telemetry & MB", use_container_width=True):
        st.rerun()

    st.caption("CECI v3.0 • Civil Litigation & Contract Intelligence")

# Seven Core Tabs
tabs = st.tabs([
    "📊 BOQ Variation Auditor",
    "🕸️ Multi-Modal Evidence Graph",
    "⏱️ Delay Analysis & EoT Matrix",
    "📈 Price Escalation Engine",
    "📑 Claim Dossier Compiler",
    "🛡️ Liquidated Damages Shield",
    "🚀 5-Contractor Live Pilot Sandbox",
])

# -----------------------------------------------------------------------------
# TAB 1: BOQ VARIATION AUDITOR
# -----------------------------------------------------------------------------
with tabs[0]:
    st.header("1. BOQ Quantity & Variation Deviation Auditor")
    st.markdown("Audits field quantities against CPWD Clause 12, NHAI Schedule J, and FIDIC Clause 13 deviation thresholds.")

    col1, col2 = st.columns(2)
    with col1:
        item_no = st.text_input("BOQ Item Number", "04.12")
        item_desc = st.text_input("Item Description", "Bored Cast-in-Situ Reinforced Concrete Piles 1200mm Dia in Hard Quartzite Rock")
        unit = st.selectbox("Measurement Unit", ["RMT", "CUM", "SQM", "MT", "NOS"], index=0)
        tender_qty = st.number_input("Tender Contract Quantity", value=2400.0, step=100.0)
        executed_qty = st.number_input("Cumulative Executed Quantity on Site", value=3360.0, step=50.0)
        tender_rate = st.number_input("Agreed Tender Rate (INR)", value=18500.0, step=500.0)

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
        st.metric("Total Executed Financial Value", f"₹ {executed_qty * tender_rate:,.2f}")
        st.metric("Variation / Extra Claim Value", f"₹ {excess_amount:,.2f}")

        if dev_percent > 25.0:
            st.error(f"🚨 **CRITICAL VARIATION EXCEEDED (>25% Limit):** Deviation of {dev_percent:.1f}% exceeds statutory limits. Initiate Substituted Item Rate Analysis under CPWD Clause 12 / FIDIC 13 immediately.")
        elif dev_percent > 10.0:
            st.warning(f"⚠️ **VARIATION WARNING (>10%):** Issue advance notice of deviation to the Engineer-in-Charge.")
        else:
            st.success("✅ **Within Allowable Limits (<10%):** Routine RA bill certification permitted.")

# -----------------------------------------------------------------------------
# TAB 2: EVIDENCE GRAPH
# -----------------------------------------------------------------------------
with tabs[1]:
    st.header("2. Relational Multi-Modal Engineering Evidence Graph")
    st.markdown("Visualizes primary engineering artifacts backing the item for bulletproof audit defense against client rejections.")

    graph = CivilEvidenceGraph()
    graph.add_node(EvidenceNode(
        node_id=f"BOQ-{item_no}",
        artifact_type=ArtifactType.BOQ_ITEM,
        title=f"BOQ Item {item_no} — {item_desc[:35]}...",
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
        title="Geo-tagged Rock Core Samples Pier 4 Deep Socketing (>80 MPa)",
        date_created=date(2026, 7, 21),
        reference_path="/site_media/geo_photos/IMG_20260721_1430.jpg"
    ))
    graph.add_node(EvidenceNode(
        node_id="HINDRANCE-REG-09",
        artifact_type=ArtifactType.HINDRANCE_REGISTER_ENTRY,
        title="Site Hindrance Register Item #09 (220kV Gas Line Clearance Delay)",
        date_created=date(2026, 3, 10),
        reference_path="/site_records/hindrance_reg_vol1.pdf"
    ))

    graph.link_artifacts("DWG-STR-P04-R2", f"BOQ-{item_no}", "REVISED_SPECIFICATION_FOR")
    graph.link_artifacts("MB-42-P18", f"BOQ-{item_no}", "CERTIFIES_EXECUTED_QUANTITY_OF")
    graph.link_artifacts("PHOTO-PIER4-CORE", f"BOQ-{item_no}", "VISUAL_EVIDENCE_FOR")
    graph.link_artifacts("HINDRANCE-REG-09", f"BOQ-{item_no}", "CAUSES_DELAY_TO")

    audit_trail = graph.trace_audit_trail(f"BOQ-{item_no}")

    st.subheader(f"Certified Evidence Trail for Item {item_no}")
    df_evidence = pd.DataFrame(audit_trail)
    st.table(df_evidence)

# -----------------------------------------------------------------------------
# TAB 3: DELAY ANALYSIS & EOT MATRIX (TIA)
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("3. Time Impact Analysis (TIA) & Extension of Time (EoT) Matrix")
    st.markdown("Quantifies delay events, concurrent overlaps, and critical path impacts under CPWD Clause 5 and FIDIC Sub-Clause 8.4.")

    d1, d2 = st.columns(2)
    with d1:
        st.subheader("Delay Event Parameters")
        delay_name = st.text_input("Delay Event Title", "Delay in Shifting Unmapped 220kV Underground Utilities")
        delay_cat = st.selectbox("Delay Category", [DelayCategory.EMPLOYER_RISK.value, DelayCategory.FORCE_MAJEURE.value, DelayCategory.CONTRACTOR_RISK.value, DelayCategory.CONCURRENT_DELAY.value], index=0)
        delay_days = st.slider("Delay Duration (Days)", 5, 120, 68, step=1)
        daily_overhead = st.number_input("Contractor Site Daily Overhead / Idling Cost (INR/day)", value=145000.0, step=5000.0)
        daily_ld = st.number_input("Contract Liquidated Damages Rate (INR/day)", value=220000.0, step=10000.0)

    ev = DelayEvent(
        event_id="EV-DEMO-01",
        title=delay_name,
        category=DelayCategory(delay_cat),
        start_date=date(2025, 4, 1),
        end_date=date(2025, 6, 8),
        duration_days=delay_days,
        impacted_activity="Viaduct Substructure Foundation",
        is_critical_path=True,
        daily_site_overhead_inr=daily_overhead,
        ld_liability_risk_inr_per_day=daily_ld,
    )
    delay_res = delay_engine.analyze_delays([ev], custom_daily_overhead_inr=daily_overhead, custom_daily_ld_inr=daily_ld)

    with d2:
        st.subheader("Extension of Time & Prolongation Entitlement")
        st.metric("Net Excusable EoT Days", f"{delay_res.net_excusable_eot_days} Days", "Statutory Extension Justified")
        st.metric("Compensable Prolongation Cost", f"₹ {delay_res.prolongation_claim_amount_inr:,.2f}")
        st.metric("LD Liability Shielded", f"₹ {delay_res.ld_liability_shielded_inr:,.2f}", delta_color="normal")
        st.info(f"📜 **Arbitral Assessment:** {delay_res.contractual_verdict}")

# -----------------------------------------------------------------------------
# TAB 4: PRICE ESCALATION ENGINE
# -----------------------------------------------------------------------------
with tabs[3]:
    st.header("4. Price Escalation Engine (CPWD Clause 10CA / 10CC & FIDIC 13.7)")
    st.markdown("Automated statutory escalation calculator linked with RBI Wholesale Price Index (WPI) and Labour Bureau CPI-IW.")

    e1, e2 = st.columns(2)
    with e1:
        st.subheader("Clause 10CA Material Escalation")
        esc_comp = st.selectbox("Escalation Material Component", ["STEEL_TMT", "CEMENT", "BITUMEN", "POL_FUEL"], index=0)
        base_rate = st.number_input("Base Contract Rate (INR/Unit)", value=54000.0, step=1000.0)
        qty_consumed = st.number_input("Quantity Consumed in Quarter", value=420.0, step=10.0)
        base_index = st.number_input("Base WPI Index at Tender Base Date (CI0)", value=128.4, step=0.5)
        curr_index = st.number_input("Current WPI Index at Time of Execution (CIn)", value=146.2, step=0.5)

        res_10ca = escalation_engine.calculate_clause_10ca_item(
            component=EscalationComponent(esc_comp),
            base_rate_inr=base_rate,
            quantity_consumed=qty_consumed,
            base_index_ci0=base_index,
            current_index_cin=curr_index,
        )

    with e2:
        st.subheader("Escalation Determination")
        st.metric("Index Delta (WPI Increase)", f"+{res_10ca.delta_index_percent:.2f}%")
        st.metric("Statutory Claimable Escalation", f"₹ {res_10ca.escalation_amount_inr:,.2f}")
        st.caption(f"Governing Formula: {res_10ca.clause_reference}")

        st.divider()
        st.subheader("Clause 10CC Composite Escalation (Labour + Material + POL)")
        gross_bill = st.number_input("Gross Work Done in Quarter (INR)", value=50000000.0, step=5000000.0)
        res_10cc = escalation_engine.calculate_clause_10cc_composite(gross_work_done_inr=gross_bill)
        st.write(f"• **Labour Escalation (VL):** ₹ {res_10cc['labour_escalation_vl_inr']:,.2f}")
        st.write(f"• **Material Escalation (VM):** ₹ {res_10cc['material_escalation_vm_inr']:,.2f}")
        st.write(f"• **Fuel Escalation (VF):** ₹ {res_10cc['fuel_escalation_vf_inr']:,.2f}")
        st.metric("Total Clause 10CC Escalation", f"₹ {res_10cc['total_escalation_inr']:,.2f}", f"{res_10cc['effective_escalation_percent']:.2f}% of Gross Bill")

# -----------------------------------------------------------------------------
# TAB 5: CLAIM DOSSIER COMPILER
# -----------------------------------------------------------------------------
with tabs[4]:
    st.header("5. Automated Variation & EoT Claim Dossier Compiler")

    proj_name = st.text_input("Project Name", "Delhi-Meerut Regional Rapid Transit System (RRTS) Viaduct PKG-03")
    contractor = st.text_input("Contractor Name", "Larsen & Toubro Ltd (Heavy Civil Infra IC)")
    client = st.text_input("Client / Authority", "National Capital Region Transport Corporation (NCRTC)")

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

# -----------------------------------------------------------------------------
# TAB 6: LIQUIDATED DAMAGES SHIELD
# -----------------------------------------------------------------------------
with tabs[5]:
    st.header("6. Liquidated Damages (LD) Immunity & Shield Engine")
    st.markdown("Statutory shield protecting EPC contractors from wrongful LD deductions through contemporaneous evidence trails.")

    scol1, scol2 = st.columns(2)
    with scol1:
        st.markdown("### 🛡️ Contractor Risk Shield Summary")
        st.write(f"• **Target Milestone Date:** `31-March-2026`")
        st.write(f"• **Actual/Anticipated Completion:** `07-June-2026` (68 Days Extended)")
        st.write(f"• **Contract LD Rate:** `₹ {daily_ld:,.0f} / day` (Max 10% of Contract Value = ₹ 124 Cr)")
        st.write(f"• **Potential LD Liability at Risk:** `₹ {delay_res.ld_shielded_amount_inr:,.2f}`")

    with scol2:
        st.markdown("### ⚖️ Legal & Contractual Precedents")
        st.success("✅ **Hindrance Register Duly Signed:** Employer delay recorded under Clause 5.2.")
        st.success("✅ **Notice of Claim Served:** Delivered within 28 days as mandated by FIDIC Sub-Clause 20.1.")
        st.success("✅ **No Concurrent Contractor Default:** Critical path exclusively impeded by unmapped 220kV gas insulated utility line.")
        st.metric("Protected Value", f"₹ {delay_res.ld_liability_shielded_inr:,.2f}", "100% Shielded from Deduction")

# -----------------------------------------------------------------------------
# TAB 7: 5-CONTRACTOR LIVE PILOT SANDBOX
# -----------------------------------------------------------------------------
with tabs[6]:
    st.header("7. 🚀 5-Contractor Live Pilot Sandbox & Proof-of-Value (PoV)")
    st.markdown("""
    Experience CECI across **5 mega-infrastructure contractor portfolios** (Metro Elevated Rail, Coastal Sea-Link, 6-Lane Expressway, Deepwater Port, and Himalayan Hydroelectric Tunnel).
    """)

    pilot_report = ceci_pilot_evaluator.run_all_pilots()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Projects Audited</div>
            <div class="kpi-val">{pilot_report.total_contractors_audited} Projects</div>
            <div style="font-size: 12px; color: #A5B4FC; margin-top: 4px;">₹ {pilot_report.total_contract_value_cr:,.1f} Cr Total Portfolio</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Variation Claims</div>
            <div class="kpi-val">₹ {pilot_report.total_variation_claims_inr/10000000:,.2f} Cr</div>
            <div style="font-size: 12px; color: #4ADE80; margin-top: 4px;">100% Evidence-Backed</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">LD Liability Shielded</div>
            <div class="kpi-val">₹ {pilot_report.total_ld_liability_shielded_inr/10000000:,.2f} Cr</div>
            <div style="font-size: 12px; color: #4ADE80; margin-top: 4px;">Liquidated Damages Waived</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Total Value Unlocked</div>
            <div class="kpi-val">₹ {pilot_report.total_monetary_value_unlocked_inr/10000000:,.2f} Cr</div>
            <div style="font-size: 12px; color: #38BDF8; margin-top: 4px;">Variations + EoT + Escalations</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("📊 5-Contractor Proof-of-Value Comparative Benchmark")
    contractor_rows = []
    for r in pilot_report.results:
        contractor_rows.append({
            "Contractor ID": r.contractor_id,
            "Contractor Name": r.contractor_name,
            "Project": r.project_name,
            "Contract Standard": r.contract_type,
            "Variation Claim (₹)": f"₹ {r.variation_claim_amount_inr:,.0f}",
            "EoT Days": f"{r.eot_days_approved} Days",
            "Prolongation (₹)": f"₹ {r.prolongation_cost_recovered_inr:,.0f}",
            "Escalation (₹)": f"₹ {r.escalation_claim_amount_inr:,.0f}",
            "LD Shielded (₹)": f"₹ {r.ld_liability_shielded_inr:,.0f}",
            "Total Unlocked (₹)": f"₹ {r.total_financial_impact_inr:,.0f}",
        })
    df_contr = pd.DataFrame(contractor_rows)
    st.dataframe(df_contr, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("🔍 Deep-Dive Contractor Dispute Audit")
    selected_c_id = st.selectbox(
        "Select Contractor to Inspect:",
        options=list(PILOT_CONTRACTORS.keys()),
        format_func=lambda cid: f"{PILOT_CONTRACTORS[cid].contractor_name} — {PILOT_CONTRACTORS[cid].scenario.project_name}"
    )

    sel_profile = PILOT_CONTRACTORS[selected_c_id]
    sel_res = ceci_pilot_evaluator.evaluate_contractor(sel_profile)
    sel_sc = sel_profile.scenario

    c_d1, c_d2 = st.columns([1, 1])
    with c_d1:
        st.markdown(f"### 🏗️ {sel_profile.contractor_name}")
        st.markdown(f"**Headquarters:** `{sel_profile.headquarters}` • **Division:** `{sel_profile.project_division}`")
        st.markdown(f"**Lead Specialist:** `{sel_profile.lead_contract_specialist}`")
        st.markdown(f"**Project:** `{sel_sc.project_name}`")
        st.markdown(f"**Authority:** `{sel_sc.client_authority}` • **Contract:** `{sel_sc.contract_type}`")
        st.markdown(f"**Contract Value:** `₹ {sel_sc.tender_contract_value_cr:,.1f} Crores`")

        st.info(f"⚡ **Dispute Root Cause / Impasse:**\n\n{sel_sc.dispute_root_cause}")
        st.success(f"🛠️ **CECI Algorithmic Remediation:**\n\n{sel_res.ceci_remediation_summary}")

    with c_d2:
        st.markdown("### 💰 Financial & Contractual Recovery")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Variation Claim", f"₹ {sel_res.variation_claim_amount_inr:,.0f}", f"+{sel_res.variation_percent:.1f}% Deviation")
            st.metric("EoT Approved", f"{sel_res.eot_days_approved} Days")
            st.metric("Prolongation Overheads", f"₹ {sel_res.prolongation_cost_recovered_inr:,.0f}")
        with m2:
            st.metric("Price Escalation", f"₹ {sel_res.escalation_claim_amount_inr:,.0f}")
            st.metric("LD Shielded", f"₹ {sel_res.ld_liability_shielded_inr:,.0f}")
            st.metric("Total Monetary Delta", f"₹ {sel_res.total_financial_impact_inr:,.0f}")

        st.markdown(f"**Notice Compliance:** `{sel_res.notice_compliance_status}`")
