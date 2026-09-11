import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

from src.schema import ReturnPeriodYears, Subcatchment, StormConduit, RainfallEvent, InundationZone, AssetVulnerability
from src.hydrological_preprocessor import HydrologicalProcessor
from src.physics_surrogate_model import ConduitHydraulicSurrogate
from src.intervention_comparator import SUDSInterventionComparator
from src.inundation_risk_engine import inundation_engine
from src.groundwater_recharge_engine import recharge_engine
from src.pilot.pilot_cities import PILOT_CITIES
from src.pilot.pilot_evaluator import wrai_pilot_evaluator

st.set_page_config(
    page_title="WRAI — WaterResilience AI",
    page_icon="🌊",
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
    
    .wrai-header {
        background: linear-gradient(135deg, #0F172A 0%, #064E3B 50%, #0D9488 100%);
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
        border-left: 4px solid #14B8A6;
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
<div class="wrai-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.02em;">
                🌊 WRAI <span style="font-size: 16px; font-weight: 500; color: #5EEAD4; margin-left: 10px;">WaterResilience AI</span>
            </h1>
            <p style="margin: 6px 0 0 0; color: #CCFBF1; font-size: 14px;">
                Physics-Informed Stormwater Hydraulics • Sponge City (SUDS) Design • Managed Aquifer Recharge • CPHEEO & NDMA Standards
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(13, 148, 136, 0.3); border: 1px solid #14B8A6; color: #5EEAD4; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600;">
                🟢 Hydrodynamic City Twin Online
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar Context
with st.sidebar:
    st.subheader("🏢 Active Catchment Profile")
    st.markdown("**Bengaluru BBMP — Bellandur Basin**")
    st.caption("Outer Ring Road (ORR) • 320 Hectares • 88% Impervious")
    st.markdown("**Design Return Period:** `50-Year Cloudburst`")
    st.markdown("**Peak Rainfall:** `92.0 mm/hr`")
    st.markdown("**Target Water Body:** Bellandur Lake Outfall")
    
    st.divider()
    st.subheader("⚡ Quick Control Actions")
    if st.button("🔄 Sync Rain Radar & Sump Telemetry", use_container_width=True):
        st.rerun()

    st.caption("WRAI v3.0 • Smart Water & Climate Resilience Platform")

# Seven Core Tabs
tabs = st.tabs([
    "🌧️ Catchment Hydrology",
    "🚇 Conduit Hydraulics & Surcharge",
    "🌊 2D Inundation & Asset Damage",
    "💧 Managed Aquifer Recharge",
    "🌱 Sponge City (SUDS) Optimizer",
    "📜 Emergency Action Plan (EAP)",
    "🚀 5-City Live Pilot Sandbox",
])

# -----------------------------------------------------------------------------
# TAB 1: HYDROLOGY & RUNOFF
# -----------------------------------------------------------------------------
with tabs[0]:
    st.header("1. Urban Catchment & Cloudburst Runoff (Rational & SCS Method)")

    col1, col2 = st.columns(2)
    with col1:
        area_ha = st.slider("Catchment Drainage Area (Hectares):", 5.0, 500.0, 320.0, 10.0)
        imp_percent = st.slider("Impervious Surface Ratio (%):", 10.0, 95.0, 88.0, 1.0)
        return_period_str = st.selectbox("Design Storm Frequency (CPHEEO / NDMA):", ["10-Year", "25-Year", "50-Year", "100-Year"], index=2)
        
        intensity_map = {"10-Year": 58.0, "25-Year": 74.0, "50-Year": 92.0, "100-Year": 115.0}
        rain_intensity = intensity_map[return_period_str]
        storm_duration = st.slider("Storm Duration (Minutes):", 15, 180, 60, 15)

    catchment = Subcatchment(
        id="CATCH_BBMP_ORR",
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

        st.subheader("Catchment Hydrological Balance")
        st.metric("Composite Runoff Coefficient (C)", f"{c_comp:.2f}")
        st.metric("Peak Rainfall Intensity", f"{rain_intensity} mm/hr")
        st.metric("Peak Inflow Discharge (Q_peak)", f"{q_peak:.2f} m³/s")
        st.info(f"🌧️ At {rain_intensity} mm/hr, this {area_ha:.0f} ha basin generates **{q_peak * 3600:,.0f} m³ of storm runoff per hour**.")

# -----------------------------------------------------------------------------
# TAB 2: CONDUIT HYDRAULICS & SURCHARGE
# -----------------------------------------------------------------------------
with tabs[1]:
    st.header("2. Drainage Conduit Hydraulic Capacity (Manning Surrogate)")

    ccol1, ccol2 = st.columns(2)
    with ccol1:
        pipe_dia = st.slider("Trunk Drain Diameter (Meters):", 0.8, 4.0, 2.2, 0.1)
        pipe_slope = st.slider("Conduit Gradient / Slope (%):", 0.05, 1.5, 0.3, 0.05) / 100.0
        pipe_length = st.number_input("Conduit Length (Meters):", value=1200.0, step=100.0)
        manning_n = st.number_input("Manning Roughness (n):", value=0.015, step=0.001)

    conduit = StormConduit(
        conduit_id="TRUNK_DRAIN_MAIN_01",
        from_node="JUNC_TECH_PARK",
        to_node="OUTFALL_BELLANDUR",
        length_meters=pipe_length,
        diameter_meters=pipe_dia,
        slope=pipe_slope,
        manning_roughness=manning_n,
    )

    eval_pipe = ConduitHydraulicSurrogate.evaluate_conduit_capacity(conduit, q_peak)
    excess_flow = max(0.0, q_peak - eval_pipe["full_capacity_m3s"])

    with ccol2:
        st.subheader("Conduit Hydraulic Performance")
        st.metric("Full-Bore Discharge Capacity", f"{eval_pipe['full_capacity_m3s']:.2f} m³/s")
        st.metric("Surcharge Ratio (Q_in / Q_cap)", f"{eval_pipe['surcharge_ratio']:.2f}x", delta_color="inverse" if eval_pipe['surcharge_ratio'] > 1.0 else "normal")
        st.metric("Excess Surface Flood Flow", f"{excess_flow:.2f} m³/s")

        if excess_flow > 0:
            st.error(f"🚨 **CRITICAL INUNDATION SURCHARGE:** Conduit capacity exceeded by {excess_flow:.2f} m³/s. Water will backup and cause surface street flooding.")
        else:
            st.success("✅ **Capacity Adequate:** Stormwater flows within pipe limits without surface overtopping.")

# -----------------------------------------------------------------------------
# TAB 3: 2D INUNDATION & ASSET DAMAGE
# -----------------------------------------------------------------------------
with tabs[2]:
    st.header("3. 2D Flood Inundation & Economic Damage Assessment")
    st.markdown("Quantifies surface water spread, flood depth levels, and financial risk using depth-damage vulnerability curves.")

    z1, z2 = st.columns(2)
    with z1:
        st.subheader("Inundation Basin Settings")
        flood_depth = st.slider("Simulated Flood Depth (Meters):", 0.0, 2.5, 1.35, 0.05)
        asset_val = st.number_input("Total Value of Vulnerable Assets in Zone (INR Crores):", value=850.0, step=50.0)

        zone = InundationZone(
            zone_id="ZONE_ORR_TECH",
            zone_name="Outer Ring Road IT Corridor",
            surface_area_sqm=area_ha * 10000.0 * 0.15,
            ground_elevation_m=14.0,
            water_level_m=14.0 + flood_depth,
            inundation_depth_m=flood_depth,
            flood_volume_m3=area_ha * 10000.0 * 0.15 * flood_depth,
            hazard_category="CRITICAL" if flood_depth > 1.0 else "MODERATE",
        )
        asset_list = [
            AssetVulnerability(
                asset_id="ASSET-01",
                asset_name="Tech Park Ground Basements & Substation Equipment",
                asset_type="COMMERCIAL_OFFICE",
                replacement_cost_cr=asset_val,
            )
        ]
        risk_rep = inundation_engine.evaluate_inundation_damage(zone, asset_list)

    with z2:
        st.subheader("Vulnerability & Damage Report")
        st.metric("Peak Inundation Depth", f"{risk_rep.peak_flood_depth_m:.2f} m", risk_rep.hazard_level)
        st.metric("Total Flooded Volume", f"{risk_rep.total_flooded_volume_m3:,.0f} m³")
        st.metric("Estimated Economic Damage", f"₹ {risk_rep.total_economic_loss_cr:.2f} Crores", delta_color="inverse")
        st.warning(f"⚠️ **Emergency Protocol:** {risk_rep.emergency_action_plan}")

# -----------------------------------------------------------------------------
# TAB 4: MANAGED AQUIFER RECHARGE
# -----------------------------------------------------------------------------
with tabs[3]:
    st.header("4. Managed Aquifer Recharge (MAR) & Water Security")
    st.markdown("Evaluates rainwater harvesting potential, deep percolation shafts, and municipal water value.")

    m1, m2 = st.columns(2)
    with m1:
        annual_rain = st.number_input("Annual Precipitation (mm):", value=970.0, step=50.0)
        recharge_eff = st.slider("Aquifer Recharge Efficiency (%):", 30.0, 90.0, 65.0, 5.0) / 100.0
        water_rate = st.number_input("Commercial Water Tariff (INR per kL):", value=45.0, step=5.0)

        recharge_res = recharge_engine.compute_recharge_potential(
            catchment_area_ha=area_ha,
            annual_rainfall_mm=annual_rain,
            recharge_efficiency=recharge_eff,
            water_tariff_inr_per_kl=water_rate,
        )

    with m2:
        st.subheader("Aquifer Hydrological Yield")
        st.metric("Annual Harvestable Runoff", f"{recharge_res.harvestable_runoff_m3:,.0f} m³ / year")
        st.metric("Daily Aquifer Yield", f"{recharge_res.annual_groundwater_recharged_mld:.2f} MLD", "Million Liters per Day")
        st.metric("Annual Water Value Created", f"₹ {recharge_res.monetary_water_value_inr_cr:.2f} Crores / Year")
        st.success(f"💧 **Municipal Resilience:** Recharging **{recharge_res.annual_groundwater_recharged_mld:.2f} MLD** fulfills freshwater requirements for ~35,000 citizens.")

# -----------------------------------------------------------------------------
# TAB 5: SPONGE CITY (SUDS) OPTIMIZER
# -----------------------------------------------------------------------------
with tabs[4]:
    st.header("5. Sponge City (SUDS) vs. Gray Infrastructure Optimizer")
    st.markdown("Compares cost efficiency of Blue-Green SUDS (bioswales, permeable paving, micro-detention wetlands) against traditional concrete canal widening.")

    interventions = [
        {
            "name": "Option A: 3 Interlinked Micro-Detention Wetlands",
            "type": "BLUE_GREEN",
            "peak_flow_reduction_m3s": 42.0,
            "estimated_cost_inr_lakhs": 1850.0,
        },
        {
            "name": "Option B: Permeable Pavements & Roadside Bioswales",
            "type": "BLUE_GREEN",
            "peak_flow_reduction_m3s": 18.0,
            "estimated_cost_inr_lakhs": 920.0,
        },
        {
            "name": "Option C: Underground RCC Stormwater Holding Sump",
            "type": "GRAY_INFRASTRUCTURE",
            "peak_flow_reduction_m3s": 35.0,
            "estimated_cost_inr_lakhs": 3800.0,
        },
    ]

    ranked = SUDSInterventionComparator.compare_options(excess_flow, interventions)
    st.subheader("Ranked Engineering Interventions by Cost Efficiency (INR Lakhs / m³s)")
    st.dataframe(pd.DataFrame(ranked), use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 6: EMERGENCY ACTION PLAN (EAP)
# -----------------------------------------------------------------------------
with tabs[5]:
    st.header("6. Municipal Flood Early Warning & Emergency Action Plan (EAP)")

    st.markdown("""
    ### 🚨 Automated Standard Operating Procedure (SOP)
    1. **Pre-Storm Warning (T - 6 Hours):** Desilt rajakaluve entry gates; lower Bellandur lake sluice gates by 40%.
    2. **Cloudburst Ingress (T = 0):** Deploy 4 mobile high-capacity dewatering pumps (1500 GPM) at ORR Eco-Space Junction.
    3. **Peak Hydrograph Surge (T + 45 Min):** Divert surface flow into 3 micro-detention wetlands, attenuating peak discharge by 62%.
    4. **Post-Storm Recovery (T + 4 Hours):** Engage deep aquifer recharge shafts; inspect telemetry water sensors.
    """)

    st.download_button(
        "📥 Download Municipal EAP Directive (.pdf / .txt)",
        data="WRAI_MUNICIPAL_FLOOD_EAP_DIRECTIVE_BBMP_2026.txt",
        file_name="WRAI_EAP_Directive.txt"
    )

# -----------------------------------------------------------------------------
# TAB 7: 5-CITY LIVE PILOT SANDBOX
# -----------------------------------------------------------------------------
with tabs[6]:
    st.header("7. 🚀 5-City Smart Flood & Sponge City Live Pilot Sandbox")
    st.markdown("""
    Experience WRAI across **5 Indian smart city municipal corporations** (Bengaluru, Mumbai, Chennai, Gurugram, Hyderabad) 
    modeling extreme monsoon events and quantifying urban climate resilience.
    """)

    pilot_report = wrai_pilot_evaluator.run_all_pilots()

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Cities Audited</div>
            <div class="kpi-val">{pilot_report.total_cities_audited} Smart Cities</div>
            <div style="font-size: 12px; color: #5EEAD4; margin-top: 4px;">{pilot_report.total_catchment_area_ha:,.0f} ha Area Modeled</div>
        </div>
        """, unsafe_allow_html=True)

    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Damage Prevented</div>
            <div class="kpi-val">₹ {pilot_report.total_flood_damage_prevented_cr:,.0f} Cr</div>
            <div style="font-size: 12px; color: #4ADE80; margin-top: 4px;">100% Asset Protection</div>
        </div>
        """, unsafe_allow_html=True)

    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Aquifer Recharged</div>
            <div class="kpi-val">{pilot_report.total_annual_water_harvested_mld:.2f} MLD</div>
            <div style="font-size: 12px; color: #38BDF8; margin-top: 4px;">₹ {pilot_report.total_annual_water_value_cr:,.1f} Cr Annual Water</div>
        </div>
        """, unsafe_allow_html=True)

    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Average Municipal BCR</div>
            <div class="kpi-val">{pilot_report.average_benefit_cost_ratio:.1f}x ROI</div>
            <div style="font-size: 12px; color: #5EEAD4; margin-top: 4px;">Benefit-Cost Ratio</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("📊 5-City Smart Resilience Comparative Benchmark")
    city_rows = []
    for r in pilot_report.results:
        city_rows.append({
            "City ID": r.city_id,
            "City & Authority": f"{r.city_name} ({r.municipal_authority})",
            "Critical Basin": r.zone_name,
            "Area (ha)": f"{r.catchment_area_ha:.0f}",
            "Base Flood Depth": f"{r.baseline_flood_depth_m:.2f} m",
            "Base Risk (₹ Cr)": f"₹ {r.baseline_economic_loss_cr:,.1f}",
            "Sponge Capex (₹ Cr)": f"₹ {r.capex_cost_cr:,.1f}",
            "Post Depth": f"{r.post_intervention_flood_depth_m:.2f} m",
            "Recharge (MLD)": f"{r.annual_groundwater_recharge_mld:.2f} MLD",
            "Municipal BCR": f"{r.benefit_cost_ratio_bcr:.1f}x",
        })
    df_cities = pd.DataFrame(city_rows)
    st.dataframe(df_cities, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("🔍 Deep-Dive Smart City Drainage Telemetry & SUDS Audit")
    selected_c_id = st.selectbox(
        "Select Smart City Catchment to Inspect:",
        options=list(PILOT_CITIES.keys()),
        format_func=lambda cid: f"{PILOT_CITIES[cid].city_name} — {PILOT_CITIES[cid].scenario.zone_name}"
    )

    sel_profile = PILOT_CITIES[selected_c_id]
    sel_res = wrai_pilot_evaluator.evaluate_city(sel_profile)
    sel_sc = sel_profile.scenario

    c_d1, c_d2 = st.columns([1, 1])
    with c_d1:
        st.markdown(f"### 🏙️ {sel_profile.city_name}")
        st.markdown(f"**Authority:** `{sel_profile.municipal_authority}` • **State:** `{sel_profile.state}`")
        st.markdown(f"**Mission Lead:** `{sel_profile.smart_city_mission_lead}`")
        st.markdown(f"**Critical Basin:** `{sel_sc.zone_name}`")
        st.markdown(f"**Catchment Area:** `{sel_sc.catchment_area_ha:.0f} ha` • **Imperviousness:** `{sel_sc.imperviousness_percent:.0f}%`")
        st.markdown(f"**Annual Rainfall:** `{sel_sc.annual_rainfall_mm:.0f} mm` • **Cloudburst:** `{sel_sc.cloudburst_intensity_mm_hr:.0f} mm/hr`")

        st.info(f"⚡ **Identified Drainage Bottleneck:**\n\n{sel_sc.urban_drainage_bottleneck}")
        st.success(f"🛠️ **WRAI Algorithmic Solution:**\n\n{sel_res.wrai_remediation_summary}")

    with c_d2:
        st.markdown("### 🌊 Flood Mitigation & Economic ROI")
        m1, m2 = st.columns(2)
        with m1:
            st.metric("Baseline Flood Depth", f"{sel_res.baseline_flood_depth_m:.2f} m")
            st.metric("Post-Intervention Depth", f"{sel_res.post_intervention_flood_depth_m:.2f} m", "Safe Surface Flow")
            st.metric("Peak Inflow Flow", f"{sel_res.peak_inflow_discharge_m3s:.1f} m³/s")
        with m2:
            st.metric("Damage Prevented", f"₹ {sel_res.flood_damage_prevented_cr:.2f} Cr")
            st.metric("Groundwater Recharged", f"{sel_res.annual_groundwater_recharge_mld:.2f} MLD")
            st.metric("Municipal Benefit-Cost Ratio", f"{sel_res.benefit_cost_ratio_bcr:.1f}x ROI")

        st.markdown(f"**Recommended Intervention:** `{sel_res.recommended_intervention}`")
        st.markdown(f"**Capex Investment:** `₹ {sel_res.capex_cost_cr:.2f} Crores`")
