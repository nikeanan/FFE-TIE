import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from src.schema import ConcreteGrade, ExposureCondition, MixProportion, BatchTicket
from src.is_code_standards import calculate_target_mean_strength, check_is456_compliance
from src.strength_predictor import HybridStrengthPredictor
from src.qc_anomaly_engine import BatchQCAnomalyEngine
from src.carbon_intelligence import carbon_engine, CarbonProfile
from src.cure_maturity_engine import maturity_engine, MaturityReading
from src.qa_certificate_exporter import qa_exporter
from src.pilot.pilot_plants import PILOT_PLANTS
from src.pilot.pilot_evaluator import cmi_pilot_evaluator

st.set_page_config(
    page_title="CMI — Construction Material Intelligence",
    page_icon="🏗️",
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
    
    .cmi-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0369A1 100%);
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
        border-left: 4px solid #0284C7;
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
<div class="cmi-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.02em;">
                🏗️ CMI <span style="font-size: 16px; font-weight: 500; color: #38BDF8; margin-left: 10px;">Construction Material Intelligence</span>
            </h1>
            <p style="margin: 6px 0 0 0; color: #CBD5E1; font-size: 14px;">
                Physics-Informed Quality & Carbon Intelligence for Ready-Mix Concrete & EPC Contractors — IS 10262:2019 • IS 456 • IS 4926 • ASTM C1074
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(3, 105, 161, 0.3); border: 1px solid #0284C7; color: #38BDF8; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600;">
                🟢 SCADA Plant Twin Online
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Context
with st.sidebar:
    st.subheader("🏢 Batching Plant Profile")
    st.markdown("**UltraTech Ready-Mix Plant #04**")
    st.caption("Gurugram Sector 62 Hub • Twin-Shaft 2.0 m³ Mixer")
    st.markdown("**SCADA System:** BHS-Sonthofen / Schwing Stetter")
    st.markdown("**Monthly Volume:** `8,500 m³/month`")
    st.markdown("**Connected EPC Clients:** L&T, Tata Projects, DLF")
    
    st.divider()
    st.subheader("⚡ Quick Control Actions")
    if st.button("🔄 Sync Plant Telemetry", use_container_width=True):
        st.rerun()

    st.caption("CMI v3.0 • Civil Engineering & Materials Platform")

# Seven Core Tabs
tabs = st.tabs([
    "🧪 Mix Design & IS Standards",
    "⚠️ Real-Time Batch QC & Anomaly",
    "📈 Strength Prediction & Maturity",
    "🌱 Embodied Carbon & SCMs",
    "💰 Plant Economics & Savings",
    "📜 Digital QA Certificate & NCR",
    "🚀 5-Plant Live Pilot Sandbox",
])

# -----------------------------------------------------------------------------
# TAB 1: MIX DESIGN & IS STANDARDS
# -----------------------------------------------------------------------------
with tabs[0]:
    st.header("1. Concrete Mix Design & Code Compliance (IS 10262:2019 & IS 456:2000)")

    col1, col2 = st.columns(2)
    with col1:
        grade_choice = st.selectbox("Design Concrete Grade:", ["M20", "M25", "M30", "M35", "M40", "M50"], index=2)
        grade_enum = ConcreteGrade(grade_choice)
        exposure_choice = st.selectbox("Environmental Exposure Condition (IS 456 Table 5):", ["MILD", "MODERATE", "SEVERE", "VERY_SEVERE", "EXTREME"], index=2)
        exposure_enum = ExposureCondition(exposure_choice)

        target_fck = calculate_target_mean_strength(grade_enum)
        st.metric("Target Mean Compressive Strength (f'ck)", f"{target_fck:.2f} MPa", f"IS 10262:2019 (f'ck = fck + 1.65×s)")

    with col2:
        st.subheader("Mix Proportions per m³")
        cement_val = st.slider("Cement (OPC 53) (kg/m³):", 250.0, 480.0, 330.0, step=5.0)
        fly_ash_val = st.slider("Fly Ash (Class F) (kg/m³):", 0.0, 140.0, 80.0, step=5.0)
        water_val = st.slider("Design Water (Liters/m³):", 130.0, 200.0, 160.0, step=1.0)
        sand_val = st.slider("Fine Aggregate / M-Sand (kg/m³):", 600.0, 900.0, 740.0, step=10.0)
        coarse_10_val = st.slider("Coarse Aggregate 10mm (kg/m³):", 350.0, 650.0, 480.0, step=10.0)
        coarse_20_val = st.slider("Coarse Aggregate 20mm (kg/m³):", 500.0, 850.0, 680.0, step=10.0)
        admix_val = st.slider("Chemical Admixture (PCE Polycarboxylate) (kg/m³):", 1.0, 6.0, 3.2, step=0.1)

    total_binder = cement_val + fly_ash_val
    wb_ratio = water_val / total_binder if total_binder > 0 else 0.55

    st.subheader("Durability & Code Compliance Verification")
    violations = check_is456_compliance(
        total_cementitious_kg=total_binder,
        water_cement_ratio=wb_ratio,
        grade=grade_enum,
        exposure=exposure_enum,
    )

    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.metric("Total Cementitious Binder", f"{total_binder:.1f} kg/m³")
    with mcol2:
        st.metric("Water-Binder (W/B) Ratio", f"{wb_ratio:.3f}")
    with mcol3:
        st.metric("IS 456 Status", "PASSED" if not violations else "NON-COMPLIANT", delta_color="normal" if not violations else "inverse")

    if violations:
        for v in violations:
            st.error(f"❌ {v}")
    else:
        st.success(f"✅ Mix strictly complies with IS 456:2000 durability limits for {exposure_choice} exposure.")

# -----------------------------------------------------------------------------
# TAB 2: REAL-TIME BATCH QC & ANOMALY ENGINE
# -----------------------------------------------------------------------------
with tabs[1]:
    st.header("2. Real-Time Batch QC & Sensor Anomaly Engine (IS 4926)")
    st.markdown("Automated SCADA scale drift detector and aggregate surface moisture compensation engine.")

    bcol1, bcol2 = st.columns(2)
    with bcol1:
        st.subheader("Batching Plant Sensor Readings (Live Batch)")
        actual_cement = st.number_input("Batched Cement Weight (kg):", value=cement_val - 4.0, step=1.0)
        actual_water = st.number_input("Metered Water Added (L):", value=water_val - 5.0, step=1.0)
        measured_sand_moist = st.slider("Measured Sand Moisture (%):", 0.0, 8.0, 4.5, 0.1)
        sand_absorption = st.slider("Sand Absorption (%):", 0.0, 4.0, 1.2, 0.1)

    mix_prop = MixProportion(
        grade=grade_enum,
        target_fck_28d=target_fck,
        cement_opc_kg=cement_val,
        fly_ash_kg=fly_ash_val,
        water_liters=water_val,
        fine_aggregate_sand_kg=sand_val,
        coarse_aggregate_10mm_kg=coarse_10_val,
        coarse_aggregate_20mm_kg=coarse_20_val,
        chemical_admixture_kg=admix_val,
    )

    ticket = BatchTicket(
        ticket_id="TICKET-NCR-2026-9081",
        plant_id="PLANT_GURUGRAM_01",
        timestamp=datetime.now(),
        recipe_code=f"{grade_choice}_PUMP_SCM",
        target_proportions=mix_prop,
        actual_cement_kg=actual_cement,
        actual_fly_ash_kg=fly_ash_val,
        actual_water_liters=actual_water,
        actual_sand_kg=sand_val + 8.0,
        actual_coarse_10mm_kg=coarse_10_val - 2.0,
        actual_coarse_20mm_kg=coarse_20_val + 2.0,
        actual_admixture_kg=admix_val,
        sand_moisture_percent=measured_sand_moist,
        sand_absorption_percent=sand_absorption,
    )

    qc_engine = BatchQCAnomalyEngine()
    alerts = qc_engine.inspect_batch(ticket)

    with bcol2:
        st.subheader("Moisture Diagnostics & Effective Water-Cement Ratio")
        free_water_val = ticket.free_water_from_sand_liters
        total_effective_w = ticket.actual_water_liters + free_water_val
        effective_wc_val = total_effective_w / (ticket.actual_cement_kg + ticket.actual_fly_ash_kg)

        st.metric("Effective Water (Metered + Moisture)", f"{total_effective_w:.1f} L", f"+{free_water_val:.1f} L from aggregate moisture")
        st.metric("Effective W/C Ratio", f"{effective_wc_val:.3f}")

        if alerts:
            for a in alerts:
                if a.severity == "CRITICAL":
                    st.error(f"🚨 **[{a.severity}] {a.parameter}:** Actual={a.actual_value} vs Target={a.target_value} ({a.deviation_percent:+0.1f}%)\n\n**Diagnosis:** {a.explanation}\n\n👉 **Recommended Engineer Action:** `{a.recommended_engineer_action}`")
                else:
                    st.warning(f"⚠️ **[{a.severity}] {a.parameter}:** Actual={a.actual_value} vs Target={a.target_value} ({a.deviation_percent:+0.1f}%)\n\n**Diagnosis:** {a.explanation}\n\n👉 **Recommended Engineer Action:** `{a.recommended_engineer_action}`")
        else:
            st.success("✅ All batching scales and moisture values are strictly within IS 4926 allowable tolerances (±2% cement, ±3% aggregates).")

# -----------------------------------------------------------------------------
# TAB 3: STRENGTH PREDICTION & MATURITY
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("3. Strength Prediction (90% PI) & Concrete Maturity Log")
    st.markdown("Physics-Informed ML predictor coupled with Nurse-Saul temperature-maturity index (ASTM C1074) for early formwork de-shuttering.")

    predictor = HybridStrengthPredictor()
    pred_res = predictor.predict_strength(ticket)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Predicted 28-Day Strength", f"{pred_res['predicted_28d_strength_mpa']} MPa", f"PI: {pred_res['prediction_interval_28d_90'][0]} – {pred_res['prediction_interval_28d_90'][1]} MPa")
    p2.metric("Predicted 7-Day Strength", f"{pred_res['predicted_7d_strength_mpa']} MPa", f"PI: {pred_res['prediction_interval_7d_90'][0]} – {pred_res['prediction_interval_7d_90'][1]} MPa")
    p3.metric("Target f'ck (IS 10262)", f"{pred_res['target_mean_strength_mpa']} MPa")
    p4.metric("Safety Margin", f"{pred_res['safety_margin_mpa']:+0.2f} MPa", delta_color="normal" if pred_res['safety_margin_mpa'] >= 0 else "inverse")

    st.divider()
    st.subheader("🌡️ In-Situ Curing Maturity & Early De-Shuttering Engine (ASTM C1074)")
    st.caption("Thermocouple temperature sensor stream tracking hydration heat inside the cast structure:")

    m1, m2 = st.columns([1, 1])
    with m1:
        curing_hours = st.slider("Hours Elapsed Since Pouring:", 12.0, 96.0, 48.0, step=6.0)
        avg_ambient_temp = st.slider("Average Curing Temperature (°C):", 15.0, 42.0, 30.0, step=1.0)
        
        sim_history = [
            MaturityReading(hours_elapsed=curing_hours * 0.25, curing_temp_celsius=avg_ambient_temp + 3.0),
            MaturityReading(hours_elapsed=curing_hours * 0.50, curing_temp_celsius=avg_ambient_temp + 5.0),
            MaturityReading(hours_elapsed=curing_hours * 0.75, curing_temp_celsius=avg_ambient_temp + 2.0),
            MaturityReading(hours_elapsed=curing_hours, curing_temp_celsius=avg_ambient_temp),
        ]
        maturity_est = maturity_engine.estimate_early_strength(sim_history, target_28d_strength=target_fck)

    with m2:
        st.metric("Nurse-Saul Maturity Index", f"{maturity_est.maturity_index_degree_hours:,.0f} °C-hrs")
        st.metric("Estimated In-Situ Strength", f"{maturity_est.estimated_insitu_strength_mpa:.2f} MPa", f"{maturity_est.percent_target_achieved:.1f}% of 28d Target")
        if maturity_est.deshuttering_status == "SAFE_TO_DESHUTTER":
            st.success(maturity_est.safety_verdict)
        else:
            st.warning(maturity_est.safety_verdict)

# -----------------------------------------------------------------------------
# TAB 4: EMBODIED CARBON & SCMS
# -----------------------------------------------------------------------------
with tabs[3]:
    st.header("4. Embodied Carbon & SCM Replacement Intelligence")
    st.markdown("Calculates Scope 3 Embodied Carbon (kg CO₂e/m³), SCM substitution ratios, and green building credits (GRIHA, IGBC, LEED).")

    carb_profile = CarbonProfile(
        opc_kg=cement_val,
        fly_ash_kg=fly_ash_val,
        ggbs_kg=0.0,
        micro_silica_kg=0.0,
        water_liters=water_val,
        sand_kg=sand_val,
        coarse_aggregate_kg=coarse_10_val + coarse_20_val,
        admixture_kg=admix_val,
    )
    carbon_res = carbon_engine.compute_embodied_carbon(carb_profile, monthly_volume_m3=8500.0)

    ccol1, ccol2, ccol3, ccol4 = st.columns(4)
    ccol1.metric("Embodied Carbon", f"{carbon_res.total_co2e_kg_per_m3:.1f} kg CO₂e/m³")
    ccol2.metric("Carbon Reduction vs OPC", f"-{carbon_res.co2e_reduction_percentage:.1f}%", f"-{carbon_res.co2e_reduction_kg_per_m3:.1f} kg/m³")
    ccol3.metric("SCM Replacement Ratio", f"{carbon_res.scm_replacement_percentage:.1f}%")
    ccol4.metric("GRIHA / IGBC Tier", carbon_res.igbc_rating_tier)

    st.divider()
    st.subheader("📊 Material Carbon Footprint Breakdown")
    df_carbon = pd.DataFrame([
        {"Material": k, "Embodied CO₂e (kg/m³)": v}
        for k, v in carbon_res.breakdown_by_material.items()
    ])
    st.bar_chart(df_carbon.set_index("Material"))
    st.info(f"🌱 **Annual Plant Carbon Offset:** This mix reduces **{carbon_res.annual_plant_carbon_offset_tonnes:,.1f} Tonnes of CO₂e per year** at 8,500 m³/month production volume.")

# -----------------------------------------------------------------------------
# TAB 5: PLANT ECONOMICS & SAVINGS
# -----------------------------------------------------------------------------
with tabs[4]:
    st.header("5. Plant Economics & Cement Reduction ROI Matrix")
    st.markdown("Quantifies raw material cost savings achieved through precision moisture compensation and low-variance batching.")

    r1, r2 = st.columns(2)
    with r1:
        plant_monthly_volume = st.number_input("Monthly Plant Production Volume (m³):", value=8500.0, step=500.0)
        cement_cost_bag = st.number_input("Cement Price per 50kg Bag (INR):", value=360.0, step=10.0)
        cement_reduction_kg = st.slider("Achieved Cement Reduction via CMI Optimization (kg/m³):", 4.0, 25.0, 14.0, step=1.0)
        cmi_saas_fee = st.number_input("CMI Platform Fee (INR/month):", value=25000.0, step=5000.0)

    with r2:
        monthly_cement_saved_kg = plant_monthly_volume * cement_reduction_kg
        monthly_bags_saved = monthly_cement_saved_kg / 50.0
        monthly_inr_saved = monthly_bags_saved * cement_cost_bag
        net_monthly_profit = monthly_inr_saved - cmi_saas_fee
        roi_multiple = monthly_inr_saved / cmi_saas_fee if cmi_saas_fee > 0 else 0.0

        st.subheader("Monthly Economic Savings")
        st.metric("Cement Saved Monthly", f"{monthly_bags_saved:,.0f} Bags ({monthly_cement_saved_kg/1000:,.1f} Tonnes)")
        st.metric("Gross Material Cost Saved", f"₹ {monthly_inr_saved:,.2f} / month")
        st.metric("Net Plant Profit Delta", f"₹ {net_monthly_profit:,.2f} / month", f"ROI: {roi_multiple:.1f}x")

# -----------------------------------------------------------------------------
# TAB 6: DIGITAL QA CERTIFICATE & NCR
# -----------------------------------------------------------------------------
with tabs[5]:
    st.header("6. Digital Ready-Mix QA Certificate & Non-Conformance Report (NCR)")
    st.markdown("Generates tamper-evident, cryptographic digital batch compliance certificates for EPC contractors and project consultants.")

    qcol1, qcol2 = st.columns([1, 1])
    with qcol1:
        project_name = st.text_input("Project Name:", "Delhi-Meerut RRTS Corridor Package 3")
        client_name = st.text_input("EPC Client / Contractor:", "Larsen & Toubro Ltd (Heavy Civil Infra)")
        ticket_no = st.text_input("Batch Ticket Ref:", "TICKET-NCR-2026-9081")

        cert_text = qa_exporter.generate_batch_certificate(
            ticket_id=ticket_no,
            plant_id="PLANT_GURUGRAM_01",
            project_name=project_name,
            client_name=client_name,
            grade=grade_choice,
            recipe_code=f"{grade_choice}_PUMP_SCM",
            batched_volume_m3=6.0,
            target_fck=target_fck,
            predicted_28d_fck=pred_res["predicted_28d_strength_mpa"],
            effective_wc_ratio=effective_wc_val,
            co2e_per_m3=carbon_res.total_co2e_kg_per_m3,
            qc_verdict="PASSED_AND_CERTIFIED" if not alerts else "CONDITIONAL_APPROVAL",
        )

        st.download_button(
            label="📥 Download Digital QA Certificate (.txt)",
            data=cert_text,
            file_name=f"CMI_QA_CERT_{ticket_no}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with qcol2:
        st.subheader("Live Certificate Preview")
        st.text_area("Certificate Content:", cert_text, height=420)

# -----------------------------------------------------------------------------
# TAB 7: 5-PLANT LIVE PILOT SANDBOX & PROOF-OF-VALUE
# -----------------------------------------------------------------------------
with tabs[6]:
    st.header("7. 🚀 5-Plant Live Pilot Sandbox & Zero-Rejection Proof-of-Value (PoV)")
    st.markdown("""
    Experience CMI across **5 production-grade Ready-Mix & EPC batching plants** simulating challenging real-world Indian infrastructure projects 
    (Metro Rail, Coastal Expressways, Bullet Train Terminals, Highway Pavements, and Hydroelectric Dams).
    """)

    pilot_report = cmi_pilot_evaluator.run_all_pilots()

    # Executive Overview KPIs
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Plants Audited</div>
            <div class="kpi-val">{pilot_report.total_plants_audited} Plants</div>
            <div style="font-size: 12px; color: #38BDF8; margin-top: 4px;">100% IS 456 & 4926 Verified</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Total Monthly Volume</div>
            <div class="kpi-val">{pilot_report.total_monthly_volume_m3:,.0f} m³</div>
            <div style="font-size: 12px; color: #38BDF8; margin-top: 4px;">Across 5 Mega-Projects</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Monthly Material Savings</div>
            <div class="kpi-val">₹ {pilot_report.total_monthly_savings_inr:,.0f}</div>
            <div style="font-size: 12px; color: #4ADE80; margin-top: 4px;">₹ {pilot_report.total_annual_savings_inr/10000000:,.2f} Cr / Year</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Annual Carbon Offset</div>
            <div class="kpi-val">{pilot_report.total_annual_co2_tonnes_offset:,.1f} T</div>
            <div style="font-size: 12px; color: #4ADE80; margin-top: 4px;">Scope 3 CO₂e Reduced</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 5-Plant Comparison Table
    st.subheader("📊 5-Plant Proof-of-Value Comparative Benchmark")
    plant_rows = []
    for r in pilot_report.results:
        plant_rows.append({
            "Plant ID": r.plant_id,
            "Plant & Operator": f"{r.plant_name} ({r.operator_name})",
            "Project": r.project_name,
            "Grade": r.target_grade,
            "Monthly Vol (m³)": f"{r.monthly_volume_m3:,.0f}",
            "Cement Saved (kg/m³)": f"-{r.cement_saved_kg_m3:.1f} kg",
            "28d Safety Margin": f"+{r.safety_margin_mpa:.2f} MPa",
            "Monthly Savings (₹)": f"₹ {r.monthly_gross_savings_inr:,.0f}",
            "Annual CO₂ Offset (T)": f"{r.annual_co2e_tonnes_offset:,.1f} T",
            "Green Tier": r.green_rating_tier,
        })
    df_plants = pd.DataFrame(plant_rows)
    st.dataframe(df_plants, use_container_width=True, hide_index=True)

    st.divider()

    # Detailed Plant Drill-Down
    st.subheader("🔍 Deep-Dive Plant Telemetry & Remediation Audit")
    selected_p_id = st.selectbox(
        "Select Pilot Plant to Inspect:",
        options=list(PILOT_PLANTS.keys()),
        format_func=lambda pid: f"{PILOT_PLANTS[pid].plant_name} — {PILOT_PLANTS[pid].scenario.project_name} ({PILOT_PLANTS[pid].scenario.target_grade})"
    )

    sel_profile = PILOT_PLANTS[selected_p_id]
    sel_res = cmi_pilot_evaluator.evaluate_plant(sel_profile)
    sel_sc = sel_profile.scenario

    dcol1, dcol2 = st.columns([1, 1])
    with dcol1:
        st.markdown(f"### 🏭 {sel_profile.plant_name}")
        st.markdown(f"**Operator:** `{sel_profile.operator_name}` • **Location:** `{sel_profile.location}`")
        st.markdown(f"**Mixer Hardware:** `{sel_profile.mixer_hardware}` • **SCADA:** `{sel_profile.scada_system}`")
        st.markdown(f"**Target Application:** `{sel_sc.project_name}`")
        st.markdown(f"**Design Grade:** `{sel_sc.target_grade}` ({sel_sc.exposure_condition} Exposure)")

        st.info(f"⚡ **Identified Bottleneck / Root Cause:**\n\n{sel_sc.root_cause_defect}")
        st.success(f"🛠️ **CMI Algorithmic Remediation:**\n\n{sel_res.cmi_remediation_summary}")

    with dcol2:
        st.markdown("### 📈 Quality & Economic Impact")
        
        m_c1, m_c2 = st.columns(2)
        with m_c1:
            st.metric("Baseline Cement", f"{sel_res.baseline_cement_kg_m3:.0f} kg/m³")
            st.metric("CMI Optimized Cement", f"{sel_res.optimized_cement_kg_m3:.0f} kg/m³", f"-{sel_res.cement_saved_kg_m3:.1f} kg/m³")
            st.metric("Target f'ck", f"{sel_res.target_28d_strength_mpa:.1f} MPa")
        with m_c2:
            st.metric("Monthly Bags Saved", f"{sel_res.monthly_cement_bags_saved:,.0f} Bags")
            st.metric("Monthly Savings", f"₹ {sel_res.monthly_gross_savings_inr:,.0f}")
            st.metric("Predicted 28d Strength", f"{sel_res.predicted_28d_strength_mpa:.2f} MPa", f"+{sel_res.safety_margin_mpa:.2f} MPa Margin")

        st.markdown(f"**Green Rating Tier:** `{sel_res.green_rating_tier}` • **Annual CO₂ Offset:** `{sel_res.annual_co2e_tonnes_offset:,.1f} Tonnes`")

