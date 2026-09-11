import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime
from src.schema import ConcreteGrade, ExposureCondition, MixProportion, BatchTicket
from src.is_code_standards import calculate_target_mean_strength, check_is456_compliance
from src.strength_predictor import HybridStrengthPredictor
from src.qc_anomaly_engine import BatchQCAnomalyEngine

st.set_page_config(
    page_title="Construction Material Intelligence (CMI)",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Construction Material Intelligence (CMI)")
st.caption("Physics-Informed Decision-Support System for Concrete Quality & Material Optimization (v3.0 Defensible Standard)")

tabs = st.tabs(["🧪 Mix Design & IS Standards", "⚠️ Real-Time Batch QC & Anomaly Engine", "📈 Strength Prediction & Uncertainty (90% PI)", "💰 Material Optimization Sensitivity"])

# -----------------------------------------------------------------------------
# TAB 1: MIX DESIGN & IS STANDARDS
# -----------------------------------------------------------------------------
with tabs[0]:
    st.header("1. Concrete Mix Design & Durability Checks (IS 10262:2019 & IS 456:2000)")

    col1, col2 = st.columns(2)
    with col1:
        grade_choice = st.selectbox("Design Concrete Grade:", ["M20", "M25", "M30", "M35", "M40", "M50"], index=2)
        grade_enum = ConcreteGrade(grade_choice)
        exposure_choice = st.selectbox("Environmental Exposure Condition (IS 456 Table 5):", ["MILD", "MODERATE", "SEVERE", "VERY_SEVERE", "EXTREME"], index=2)
        exposure_enum = ExposureCondition(exposure_choice)

        target_fck = calculate_target_mean_strength(grade_enum)
        st.metric("Target Mean Compressive Strength (f'ck)", f"{target_fck:.2f} MPa", f"IS 10262:2019")

    with col2:
        st.subheader("Mix Proportions per m³")
        cement_val = st.slider("Cement (OPC 53) (kg/m³):", 280.0, 480.0, 350.0, step=5.0)
        fly_ash_val = st.slider("Fly Ash (Class F) (kg/m³):", 0.0, 140.0, 70.0, step=5.0)
        water_val = st.slider("Design Water (Liters/m³):", 130.0, 200.0, 168.0, step=1.0)
        sand_val = st.slider("Fine Aggregate / M-Sand (kg/m³):", 600.0, 900.0, 720.0, step=10.0)
        coarse_10_val = st.slider("Coarse Aggregate 10mm (kg/m³):", 350.0, 650.0, 480.0, step=10.0)
        coarse_20_val = st.slider("Coarse Aggregate 20mm (kg/m³):", 500.0, 850.0, 680.0, step=10.0)
        admix_val = st.slider("Chemical Admixture (PCE) (kg/m³):", 1.0, 6.0, 3.5, step=0.1)

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
    mcol1.metric("Total Cementitious Binder", f"{total_binder:.1f} kg/m³")
    mcol2.metric("Water-Binder (W/B) Ratio", f"{wb_ratio:.3f}")
    mcol3.metric("IS 456 Status", "PASSED" if not violations else "NON-COMPLIANT", delta_color="normal" if not violations else "inverse")

    if violations:
        for v in violations:
            st.error(f"❌ {v}")
    else:
        st.success(f"✅ Mix strictly complies with IS 456 durability limits for {exposure_choice} exposure.")

# -----------------------------------------------------------------------------
# TAB 2: REAL-TIME BATCH QC & ANOMALY ENGINE
# -----------------------------------------------------------------------------
with tabs[1]:
    st.header("2. Real-Time Batch QC & Sensor Anomaly Engine (IS 4926)")
    st.markdown("Identifies unusual production behavior (scale drift, unmetered moisture) and alerts the plant quality engineer.")

    bcol1, bcol2 = st.columns(2)
    with bcol1:
        st.subheader("Batching Sensor & Moisture Readings")
        actual_cement = st.number_input("Batched Cement Weight (kg):", value=cement_val - 6.0, step=1.0)
        actual_water = st.number_input("Metered Water Added (L):", value=water_val - 3.0, step=1.0)
        measured_sand_moist = st.slider("Measured Aggregate Moisture (%):", 0.0, 8.0, 4.8, 0.1)
        sand_absorption = st.slider("Aggregate Absorption (%):", 0.0, 4.0, 1.2, 0.1)

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
        recipe_code=f"{grade_choice}_PUMPABLE",
        target_proportions=mix_prop,
        actual_cement_kg=actual_cement,
        actual_fly_ash_kg=fly_ash_val,
        actual_water_liters=actual_water,
        actual_sand_kg=sand_val + 10.0,
        actual_coarse_10mm_kg=coarse_10_val - 2.0,
        actual_coarse_20mm_kg=coarse_20_val + 2.0,
        actual_admixture_kg=admix_val,
        sand_moisture_percent=measured_sand_moist,
        sand_absorption_percent=sand_absorption,
    )

    qc_engine = BatchQCAnomalyEngine()
    alerts = qc_engine.inspect_batch(ticket)

    with bcol2:
        st.subheader("QC Diagnostics & Human-in-the-Loop Actions")
        free_water_val = ticket.free_water_from_sand_liters
        total_effective_w = ticket.actual_water_liters + free_water_val
        effective_wc_val = total_effective_w / (ticket.actual_cement_kg + ticket.actual_fly_ash_kg)

        st.metric("Effective Water (Metered + Free Moisture)", f"{total_effective_w:.1f} L", f"+{free_water_val:.1f} L from aggregate")
        st.metric("Effective W/C Ratio", f"{effective_wc_val:.3f}")

        if alerts:
            for a in alerts:
                if a.severity == "CRITICAL":
                    st.error(f"🚨 **[{a.severity}] {a.parameter}:** Actual={a.actual_value} vs Target={a.target_value} ({a.deviation_percent:+0.1f}%)\n\n**Diagnosis:** {a.explanation}\n\n👉 **Recommended Engineer Action:** `{a.recommended_engineer_action}`")
                else:
                    st.warning(f"⚠️ **[{a.severity}] {a.parameter}:** Actual={a.actual_value} vs Target={a.target_value} ({a.deviation_percent:+0.1f}%)\n\n**Diagnosis:** {a.explanation}\n\n👉 **Recommended Engineer Action:** `{a.recommended_engineer_action}`")
        else:
            st.success("✅ All batching scales and moisture values are within IS 4926 allowable tolerances.")

# -----------------------------------------------------------------------------
# TAB 3: STRENGTH PREDICTION & UNCERTAINTY QUANTIFICATION (90% PI)
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("3. Strength Prediction with Uncertainty Quantification (90% PI)")
    st.markdown("Outputs predicted compressive strength, 90% prediction intervals, and operational confidence scores.")

    predictor = HybridStrengthPredictor()
    pred_res = predictor.predict_strength(ticket)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Predicted 28-Day Strength", f"{pred_res['predicted_28d_strength_mpa']} MPa")
    p1.caption(f"90% Prediction Interval: **{pred_res['prediction_interval_28d_90'][0]} – {pred_res['prediction_interval_28d_90'][1]} MPa**")

    p2.metric("Predicted 7-Day Strength", f"{pred_res['predicted_7d_strength_mpa']} MPa")
    p2.caption(f"90% Prediction Interval: **{pred_res['prediction_interval_7d_90'][0]} – {pred_res['prediction_interval_7d_90'][1]} MPa**")

    p3.metric("Target f'ck (IS 10262)", f"{pred_res['target_mean_strength_mpa']} MPa")
    p4.metric("Safety Margin", f"{pred_res['safety_margin_mpa']:+0.2f} MPa", delta_color="normal" if pred_res['safety_margin_mpa'] >= 0 else "inverse")

    st.info(f"📊 **Model Calibration Status:** `{pred_res['confidence_level']}` | Operational Flag: `{pred_res['operational_flag']}`\n\n*Note: {pred_res['governance_note']}*")

    # Abrams Curve with 90% Prediction Envelope
    wc_range = np.linspace(0.32, 0.65, 40)
    base_curve = 98.0 / (2.4 ** (1.5 * wc_range))
    lower_env = np.maximum(0, base_curve - (1.645 * 1.8))
    upper_env = base_curve + (1.645 * 1.8)

    df_chart = pd.DataFrame({
        "W/C Ratio": wc_range,
        "Expected Strength (MPa)": base_curve,
        "Lower 90% Bound (MPa)": lower_env,
        "Upper 90% Bound (MPa)": upper_env,
    })
    st.line_chart(df_chart.set_index("W/C Ratio"))

# -----------------------------------------------------------------------------
# TAB 4: MATERIAL OPTIMIZATION SENSITIVITY
# -----------------------------------------------------------------------------
with tabs[3]:
    st.header("4. Material Optimization Sensitivity Scenario")
    st.markdown("Evaluates potential economic and material savings under validated pilot hypotheses (without making unverified guarantee claims).")

    r1, r2 = st.columns(2)
    with r1:
        plant_monthly_volume = st.number_input("Monthly Plant Production Volume (m³):", value=7500.0, step=500.0)
        cement_cost_bag = st.number_input("Cement Price per 50kg Bag (INR):", value=360.0, step=10.0)
        cement_reduction = st.slider("Hypothesized Cement Reduction (kg/m³):", 4.0, 20.0, 12.0, step=1.0)
        saas_fee_monthly = st.number_input("Hypothesized CMI Software Fee (INR/month/plant):", value=20000.0, step=5000.0)

    with r2:
        monthly_cement_saved_kg = plant_monthly_volume * cement_reduction
        monthly_bags_saved = monthly_cement_saved_kg / 50.0
        monthly_inr_saved = monthly_bags_saved * cement_cost_bag
        net_monthly_profit = monthly_inr_saved - saas_fee_monthly
        roi_multiple = monthly_inr_saved / saas_fee_monthly if saas_fee_monthly > 0 else 0.0

        st.subheader("Sensitivity Scenario Outcomes")
        st.metric("Monthly Cement Saved (Hypothesis)", f"{monthly_bags_saved:,.0f} Bags ({monthly_cement_saved_kg/1000:,.1f} Tonnes)")
        st.metric("Gross Material Cost Reduction", f"INR {monthly_inr_saved:,.2f}")
        st.metric("Net Operational Delta (after SaaS fee)", f"INR {net_monthly_profit:,.2f}")
        st.metric("Illustrative ROI Multiple", f"{roi_multiple:.1f}x (Subject to Pilot Verification)")

        st.caption("⚠️ **Governance Disclaimer:** The above figures represent sensitivity projections for engineering evaluation and require formal verification during Phase 3 & 4 pilot trials.")
