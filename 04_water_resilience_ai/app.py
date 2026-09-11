import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import numpy as np
import pandas as pd
from src.schema import ReturnPeriodYears, Subcatchment, StormConduit, RainfallEvent
from src.hydrological_preprocessor import HydrologicalProcessor
from src.physics_surrogate_model import ConduitHydraulicSurrogate
from src.intervention_comparator import SUDSInterventionComparator

st.set_page_config(
    page_title="WaterResilience AI",
    page_icon="🌊",
    layout="wide",
)

st.title("🌊 WaterResilience AI — Urban Flood & Drainage Simulator")
st.caption("Physics-Informed ML Surrogate for Rapid 1D/2D Stormwater Hydraulics & Sponge City (SUDS) Optimization")

tabs = st.tabs(["🌧️ Hydrology & Catchment Runoff", "🚇 Conduit Hydraulic Surcharge", "🌱 Sponge City (SUDS) ROI Optimizer"])

# -----------------------------------------------------------------------------
# TAB 1: HYDROLOGY & RUNOFF
# -----------------------------------------------------------------------------
with tabs[0]:
    st.header("1. Urban Catchment & Cloudburst Runoff (Rational Method)")

    col1, col2 = st.columns(2)
    with col1:
        area_ha = st.slider("Catchment Drainage Area (Hectares):", 5.0, 250.0, 45.0, 5.0)
        imp_percent = st.slider("Impervious Surface Ratio (%):", 10.0, 95.0, 82.0, 1.0)
        return_period_str = st.selectbox("Design Storm Frequency:", ["10-Year", "25-Year", "50-Year", "100-Year"], index=2)
        
        intensity_map = {"10-Year": 48.0, "25-Year": 62.0, "50-Year": 78.5, "100-Year": 96.0}
        rain_intensity = intensity_map[return_period_str]
        storm_duration = st.slider("Storm Duration (Minutes):", 15, 180, 60, 15)

    catchment = Subcatchment(
        id="CATCH_DEMO_01",
        area_hectares=area_ha,
        imperviousness_percent=imp_percent,
        slope_percent=1.2,
    )

    storm = RainfallEvent(
        return_period=ReturnPeriodYears.FIFTY_YEAR,
        duration_minutes=storm_duration,
        intensity_mm_per_hr=rain_intensity,
    )

    q_peak = HydrologicalProcessor.calculate_rational_peak_discharge(catchment, storm)

    with col2:
        c_impervious = 0.90
        c_pervious = 0.30
        c_comp = ((imp_percent / 100.0) * c_impervious) + ((1.0 - (imp_percent / 100.0)) * c_pervious)

        st.subheader("Hydrological Output")
        st.metric("Composite Runoff Coefficient (C)", f"{c_comp:.2f}")
        st.metric("Peak Rainfall Intensity", f"{rain_intensity} mm/hr")
        st.metric("Peak Inflow Discharge (Q_peak)", f"{q_peak:.3f} m³/s")

# -----------------------------------------------------------------------------
# TAB 2: CONDUIT SURCHARGE
# -----------------------------------------------------------------------------
with tabs[1]:
    st.header("2. Drainage Conduit Hydraulic Capacity (Manning Surrogate)")

    ccol1, ccol2 = st.columns(2)
    with ccol1:
        pipe_dia = st.slider("Trunk Pipe Diameter (Meters):", 0.6, 3.5, 1.6, 0.1)
        pipe_slope = st.slider("Conduit Gradient / Slope (%):", 0.05, 1.5, 0.3, 0.05) / 100.0
        pipe_length = st.number_input("Conduit Length (Meters):", value=850.0, step=50.0)
        manning_n = st.number_input("Manning Roughness (n):", value=0.015, step=0.001)

    conduit = StormConduit(
        conduit_id="TRUNK_DRAIN_MAIN_01",
        from_node="JUNC_A",
        to_node="OUTFALL_RIVER",
        length_meters=pipe_length,
        diameter_meters=pipe_dia,
        slope=pipe_slope,
        manning_roughness=manning_n,
    )

    eval_pipe = ConduitHydraulicSurrogate.evaluate_conduit_capacity(conduit, q_peak)
    excess_flow = max(0.0, q_peak - eval_pipe["full_capacity_m3s"])

    with ccol2:
        st.subheader("Conduit Hydraulic Performance")
        st.metric("Full-Bore Capacity", f"{eval_pipe['full_capacity_m3s']:.3f} m³/s")
        st.metric("Surcharge Ratio (Q_in / Q_cap)", f"{eval_pipe['surcharge_ratio']:.2f}x", delta_color="inverse" if eval_pipe['surcharge_ratio'] > 1.0 else "normal")
        st.metric("Excess Surface Flood Flow", f"{excess_flow:.3f} m³/s")

        if excess_flow > 0:
            st.error(f"🚨 **CRITICAL INUNDATION SURCHARGE:** Pipe capacity exceeded by {excess_flow:.2f} m³/s. Water will backup and cause surface street flooding.")
        else:
            st.success("✅ **Capacity Adequate:** Stormwater flows within pipe limits without surface overtopping.")

# -----------------------------------------------------------------------------
# TAB 3: SPONGE CITY ROI OPTIMIZER
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("3. Sponge City (SUDS) vs. Gray Infrastructure Optimizer")

    interventions = [
        {
            "name": "Option A: Micro-Detention Basin (Parks & Playgrounds)",
            "type": "BLUE_GREEN",
            "peak_flow_reduction_m3s": 2.4,
            "estimated_cost_inr_lakhs": 65.0,
        },
        {
            "name": "Option B: Permeable Pavements & Roadside Bioswales",
            "type": "BLUE_GREEN",
            "peak_flow_reduction_m3s": 1.1,
            "estimated_cost_inr_lakhs": 42.0,
        },
        {
            "name": "Option C: Twin 2.2m RCC Box Culvert Upsizing",
            "type": "GRAY_INFRASTRUCTURE",
            "peak_flow_reduction_m3s": 3.2,
            "estimated_cost_inr_lakhs": 220.0,
        },
    ]

    ranked = SUDSInterventionComparator.compare_options(excess_flow, interventions)

    st.subheader("Ranked Engineering Interventions by Cost Efficiency")
    df_interventions = pd.DataFrame(ranked)
    st.dataframe(df_interventions, use_container_width=True)

    st.info("💡 **Key Finding:** Blue-Green infrastructure (Option A) delivers the highest flood mitigation per rupee invested (INR 27.08 L per m³/s mitigated vs. INR 68.75 L for traditional concrete culvert widening).")
