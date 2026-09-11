import streamlit as st
import numpy as np
import pandas as pd
from datetime import date, datetime
from decimal import Decimal

st.set_page_config(
    page_title="AI B2B Opportunities - Executive Demo",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏗️ AI-Enabled B2B Portfolio — Interactive Executive Hub")
st.caption("Four Shortlisted B2B Ventures | Live Simulation & Quality Intelligence Engines")

# Sidebar navigation
st.sidebar.title("📌 Select Opportunity")
app_mode = st.sidebar.radio(
    "Choose Project:",
    [
        "01. CPSE–MSME Receivables Agent",
        "02. Construction Material Intelligence (Recommended)",
        "03. Civil Evidence & Claims Intelligence",
        "04. WaterResilience AI",
    ],
)

# -----------------------------------------------------------------------------
# 1. CPSE-MSME RECEIVABLES INTELLIGENCE
# -----------------------------------------------------------------------------
if app_mode == "01. CPSE–MSME Receivables Agent":
    st.header("🏢 CPSE–MSME Receivables Intelligence Agent")
    st.markdown("Automated pre-submission audit, MSMED Section 15/16 interest calculation, and TReDS discount optimization.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Invoice & Contract Parameters")
        cpse_buyer = st.selectbox("CPSE Buyer:", ["NTPC Limited", "BHEL", "ONGC", "NHPC", "Indian Railways (IREPS)"])
        supplier_name = st.text_input("MSME Supplier:", "Precision Engineering MSME Ltd")
        udyam_reg = st.text_input("Udyam Registration No:", "UDYAM-HR-01-0012345")
        invoice_amount = st.number_input("Invoice Value (INR):", min_value=10000.0, max_value=100000000.0, value=531000.0, step=50000.0)
        days_overdue = st.slider("Days Overdue Beyond 45-Day Statutory Limit:", min_value=0, max_value=365, value=142)
        rbi_bank_rate = st.slider("RBI Bank Rate (%):", min_value=4.0, max_value=10.0, value=6.5, step=0.25) / 100.0

    with col2:
        st.subheader("2. Statutory MSMED & Tax Calculations")
        statutory_rate = rbi_bank_rate * 3.0  # 3x RBI rate under MSMED Sec 16
        monthly_rate = statutory_rate / 12.0
        months = days_overdue / 30.416
        compounded_total = invoice_amount * ((1.0 + monthly_rate) ** months)
        statutory_interest = compounded_total - invoice_amount

        mcol1, mcol2 = st.columns(2)
        mcol1.metric("Statutory Annual Rate (3x RBI)", f"{statutory_rate*100:.1f}%")
        mcol2.metric("MSMED Sec 16 Interest", f"INR {statutory_interest:,.2f}")
        
        mcol3, mcol4 = st.columns(2)
        mcol3.metric("Total Claimable Dues", f"INR {compounded_total:,.2f}")
        mcol4.metric("Sec 43B(h) Disallowance", "EXPOSED" if days_overdue > 0 else "COMPLIANT", delta_color="inverse")

        st.subheader("3. TReDS vs. Bank OD Optimization")
        treds_bid_rate = st.number_input("TReDS Annual Discount Bid (%):", value=8.2, step=0.1) / 100.0
        bank_od_rate = st.number_input("Bank Cash Credit / OD Rate (%):", value=12.5, step=0.1) / 100.0
        
        days_maturity = 45
        treds_cost = invoice_amount * treds_bid_rate * (days_maturity / 365.0)
        od_cost = invoice_amount * bank_od_rate * (days_maturity / 365.0)
        net_savings = od_cost - treds_cost

        st.info(f"💡 **TReDS Recommendation:** {'ACCEPT BID' if net_savings > 0 else 'HOLD'} | Net Interest Saved: **INR {net_savings:,.2f}**")

    st.divider()
    st.subheader("4. Auto-Generated Statutory MSMED Notice")
    notice_text = f"""FORMAL DEMAND NOTICE: SETTLEMENT OF OVERDUE RECEIVABLES UNDER MSMED ACT, 2006

To: General Manager (Finance & Accounts), {cpse_buyer}
From: {supplier_name} (Udyam Reg: {udyam_reg})
Subject: Urgent settlement of outstanding dues for Invoice Amount INR {invoice_amount:,.2f}

1. STATUTORY TIMELINE BREACH:
As per Section 15 of the MSMED Act 2006, payment was due within 45 days. The invoice is currently overdue by {days_overdue} days.

2. ACCRUED STATUTORY COMPOUND INTEREST (SECTION 16):
Pursuant to Section 16, interest at 3 times RBI bank rate ({statutory_rate*100:.1f}% p.a.) has accrued:
- Principal Outstanding: INR {invoice_amount:,.2f}
- Accumulated Interest: INR {statutory_interest:,.2f}
- Total Claimable: INR {compounded_total:,.2f}

3. SECTION 43B(h) NOTICE:
Failure to clear dues will attract tax deduction disallowance under Section 43B(h) of the Income Tax Act."""
    
    st.text_area("Legal Demand Draft (Copy/Export):", notice_text, height=220)

# -----------------------------------------------------------------------------
# 2. CONSTRUCTION MATERIAL INTELLIGENCE (RECOMMENDED)
# -----------------------------------------------------------------------------
elif app_mode == "02. Construction Material Intelligence (Recommended)":
    st.header("🏗️ Construction Material Intelligence (CMI)")
    st.markdown("Physics-informed quality intelligence, real-time moisture compensation, and IS 10262:2019 mix optimization.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Concrete Mix Design (IS 10262:2019)")
        grade = st.selectbox("Design Grade:", ["M20", "M25", "M30", "M35", "M40", "M50"], index=2)
        fck_val = float(grade.replace("M", ""))
        std_dev = 5.0 if fck_val >= 30 else 4.0
        target_fck = fck_val + 1.65 * std_dev

        st.metric("Target Mean Strength (f'ck)", f"{target_fck:.2f} MPa", f"IS 10262 (s={std_dev})")

        cement_opc = st.slider("Cement (OPC 53) (kg/m3):", 280.0, 480.0, 350.0, step=5.0)
        fly_ash = st.slider("Fly Ash (Class F) (kg/m3):", 0.0, 120.0, 70.0, step=5.0)
        sand_kg = st.slider("Fine Aggregate / Sand (kg/m3):", 600.0, 900.0, 720.0, step=10.0)
        batch_water = st.slider("Batching Water Added (Liters):", 130.0, 200.0, 168.0, step=1.0)
        sand_moisture = st.slider("Measured Sand Moisture (%):", 0.0, 8.0, 4.8, step=0.1)

    with col2:
        st.subheader("2. Real-Time Physical Chemistry & Prediction")
        total_binder = cement_opc + fly_ash
        free_water = sand_kg * (sand_moisture / 100.0)
        effective_water = batch_water + free_water
        effective_wc = effective_water / total_binder

        # Abram's Law Base Prior: fc = A / (B^(1.5 * wc))
        A_param, B_param = 98.0, 2.4
        pred_28d = A_param / (B_param ** (1.5 * effective_wc))
        fly_ash_ratio = fly_ash / total_binder
        early_factor = 0.67 - (0.12 * fly_ash_ratio)
        pred_7d = pred_28d * early_factor
        margin = pred_28d - target_fck

        pcol1, pcol2 = st.columns(2)
        pcol1.metric("Effective W/C Ratio", f"{effective_wc:.3f}", f"+{free_water:.1f}L Free Moisture" if free_water > 0 else "Dry")
        pcol2.metric("Predicted 7-Day Strength", f"{pred_7d:.2f} MPa")

        pcol3, pcol4 = st.columns(2)
        pcol3.metric("Predicted 28-Day Strength", f"{pred_28d:.2f} MPa")
        pcol4.metric("Safety Margin vs Target", f"{margin:+0.2f} MPa", delta_color="normal" if margin >= 0 else "inverse")

        # Anomaly Check
        st.subheader("3. Real-Time Batch QC Diagnostic")
        if sand_moisture > 3.0:
            st.error(f"🚨 **CRITICAL MOISTURE ALERT:** Sand moisture at {sand_moisture:.1f}% elevated effective water by {free_water:.1f}L. Adjust batch water down to {max(130.0, batch_water - free_water):.1f}L!")
        else:
            st.success("✅ **Batch QC Passed:** Moisture and weight tolerances within IS 4926 limits.")

        # Cement Optimization potential
        if margin > 5.0:
            potential_cement_save = (margin / 50.0) * 20.0
            monthly_save = potential_cement_save * 7500 * (360.0 / 50.0)
            st.info(f"💰 **Mix Optimization Opportunity:** Safe cement buffer reduction of **{potential_cement_save:.1f} kg/m³** = **INR {monthly_save:,.0f}/month saved** on 7,500 m³ volume.")

# -----------------------------------------------------------------------------
# 3. CIVIL EVIDENCE & CLAIMS INTELLIGENCE
# -----------------------------------------------------------------------------
elif app_mode == "03. Civil Evidence & Claims Intelligence":
    st.header("📊 Civil Engineering Evidence & Claims Intelligence")
    st.markdown("Multi-modal engineering evidence graph, BOQ quantity deviation monitoring, and audit-ready claim dossiers.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. BOQ Item & Execution Tracking")
        boq_item_id = st.text_input("BOQ Item No:", "04.1")
        item_desc = st.text_input("Description:", "Bored Cast-in-Situ RC Piles 1200mm Dia in Hard Rock")
        unit = st.selectbox("Unit:", ["RMT", "CUM", "SQM", "MT", "NOS"])
        tender_qty = st.number_input("Tender Agreed Quantity:", value=1200.0, step=100.0)
        executed_qty = st.number_input("Executed Site Quantity:", value=1620.0, step=50.0)
        tender_rate = st.number_input("Tender Unit Rate (INR):", value=14500.0, step=500.0)

    with col2:
        st.subheader("2. Contractual Variation Audit (CPWD Clause 12 / FIDIC)")
        deviation_qty = executed_qty - tender_qty
        deviation_pct = (deviation_qty / tender_qty) * 100.0 if tender_qty > 0 else 0.0
        claim_value = max(0.0, deviation_qty * tender_rate)

        vcol1, vcol2 = st.columns(2)
        vcol1.metric("Quantity Deviation", f"{deviation_pct:+0.1f}%", f"{deviation_qty:+0.1f} {unit}")
        vcol2.metric("Extra Variation Value", f"INR {claim_value:,.2f}")

        if deviation_pct > 25.0:
            st.error(f"🚨 **CRITICAL VARIATION EXCEEDED (>25% Limit):** Deviation of {deviation_pct:.1f}% mandates formal Clause 12 Substituted Rate Analysis before next RA bill.")
        elif deviation_pct > 10.0:
            st.warning(f"⚠️ **VARIATION WARNING (>10%):** Issue advance deviation notice to Engineer-in-Charge.")
        else:
            st.success("✅ **Within Standard Limits (<10%):** Routine RA bill certification permitted.")

    st.divider()
    st.subheader("3. Linked Engineering Evidence Trail")
    evidence_data = [
        {"Artifact": "Drawing Revision", "ID": "DWG-STR-P04-R2", "Title": "Substructure Pier P4 Pile Layout Rev-2 (Rock Level Adjusted)", "Status": "APPROVED"},
        {"Artifact": "Measurement Book", "ID": "MB-42-P18", "Title": "MB #42 Page 18-24 (Pile Depth Boring Logs)", "Status": "CERTIFIED"},
        {"Artifact": "Site Photo / Core", "ID": "PHOTO-PIER4-CORE", "Title": "Geo-tagged Rock Core Samples Pier 4 Deep Socketing", "Status": "VERIFIED"},
    ]
    st.table(pd.DataFrame(evidence_data))

# -----------------------------------------------------------------------------
# 4. WATERRESILIENCE AI
# -----------------------------------------------------------------------------
elif app_mode == "04. WaterResilience AI":
    st.header("🌊 WaterResilience AI — Urban Flood & Drainage Simulator")
    st.markdown("Physics-informed ML surrogate for rapid 1D/2D hydraulic simulation & Sponge City (SUDS) ROI optimization.")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("1. Urban Catchment & Cloudburst Storm")
        area_ha = st.slider("Catchment Area (Hectares):", 10.0, 200.0, 45.0, step=5.0)
        impervious_pct = st.slider("Impervious Surface Fraction (%):", 20.0, 95.0, 82.0, step=1.0)
        return_period = st.selectbox("Design Storm Return Period:", ["10-Year", "25-Year", "50-Year", "100-Year"], index=2)
        
        intensity_map = {"10-Year": 48.0, "25-Year": 62.0, "50-Year": 78.5, "100-Year": 96.0}
        rain_intensity = intensity_map[return_period]

        st.metric("Rainfall Intensity", f"{rain_intensity} mm/hr", return_period)

        # Rational Runoff: Q = C * I * A / 360
        c_composite = (impervious_pct / 100.0 * 0.90) + ((1.0 - impervious_pct / 100.0) * 0.30)
        peak_runoff = (c_composite * rain_intensity * area_ha) / 360.0

        st.metric("Peak Inflow Runoff", f"{peak_runoff:.3f} m³/s")

    with col2:
        st.subheader("2. Drainage Network Hydraulic Surcharge")
        pipe_dia = st.slider("Trunk Conduit Diameter (m):", 0.8, 3.0, 1.6, step=0.1)
        pipe_slope = st.slider("Drain Gradient / Slope (%):", 0.1, 1.0, 0.3, step=0.05) / 100.0
        
        # Manning full-pipe capacity
        radius = pipe_dia / 2.0
        area_pipe = np.pi * (radius ** 2)
        hyd_radius = pipe_dia / 4.0
        manning_n = 0.015
        q_full = (1.0 / manning_n) * area_pipe * (hyd_radius ** (2.0 / 3.0)) * np.sqrt(pipe_slope)

        surcharge_ratio = peak_runoff / q_full if q_full > 0 else 999.0
        excess_flood = max(0.0, peak_runoff - q_full)

        hcol1, hcol2 = st.columns(2)
        hcol1.metric("Conduit Capacity", f"{q_full:.3f} m³/s")
        hcol2.metric("Surcharge Ratio", f"{surcharge_ratio:.2f}x", delta_color="inverse" if surcharge_ratio > 1.0 else "normal")

        if excess_flood > 0:
            st.error(f"🚨 **DRAINAGE SURCHARGE:** Overtopping flow of **{excess_flood:.2f} m³/s** causing surface street inundation!")
        else:
            st.success("✅ **Conduit Adequate:** Drainage capacity handles peak storm without surcharge.")

    st.divider()
    st.subheader("3. AI Sponge City & SUDS Intervention Comparison")
    interventions = [
        {"Option": "Option A: Micro-Detention Basin (Public Parks)", "Type": "Blue-Green", "Flow Reduction (m3/s)": 2.4, "Cost (INR Lakhs)": 65.0, "Efficiency (INR L / m3/s)": 27.08},
        {"Option": "Option B: Permeable Pavements & Bioswales", "Type": "Blue-Green", "Flow Reduction (m3/s)": 1.1, "Cost (INR Lakhs)": 42.0, "Efficiency (INR L / m3/s)": 38.18},
        {"Option": "Option C: Twin 2.2m RCC Box Culvert Upsizing", "Type": "Gray Infra", "Flow Reduction (m3/s)": 3.2, "Cost (INR Lakhs)": 220.0, "Efficiency (INR L / m3/s)": 68.75},
    ]
    st.table(pd.DataFrame(interventions))
