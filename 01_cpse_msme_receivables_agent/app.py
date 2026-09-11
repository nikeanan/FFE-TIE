import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
from decimal import Decimal

from src.database.db_session import db
from src.database.models import InvoiceLifecycleStatus
from src.database.seed_data import seed_database
from src.agents.validator_agent import validator_agent
from src.agents.tracker_agent import tracker_agent, InboundEmailParser
from src.agents.escalator_agent import escalator_agent
from src.agents.financier_agent import financier_agent
from src.agents.forecaster_agent import forecaster_agent
from src.agents.advisor_agent import advisor_agent
from src.agents.orchestrator import orchestrator
from src.integrations.whatsapp_adapter import whatsapp
from src.integrations.samadhaan_adapter import samadhaan

# Ensure database is seeded
if not db.invoices:
    seed_database()

st.set_page_config(
    page_title="RECEIVX — CPSE–MSME Receivables Intelligence Platform",
    page_icon="⚡",
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
    
    .receivx-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0F766E 100%);
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
        border-left: 4px solid #0D9488;
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
    
    .nba-card {
        background: #1E293B;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 4px solid #F59E0B;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .whatsapp-chat-bubble-out {
        background: #005C4B;
        color: #E9EDEF;
        padding: 12px 16px;
        border-radius: 12px 12px 0 12px;
        margin: 8px 0;
        max-width: 85%;
        margin-left: auto;
        font-size: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .whatsapp-chat-bubble-in {
        background: #202C33;
        color: #E9EDEF;
        padding: 12px 16px;
        border-radius: 12px 12px 12px 0;
        margin: 8px 0;
        max-width: 85%;
        font-size: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .tag-blocker {
        background: #EF4444;
        color: white;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .tag-warn {
        background: #F59E0B;
        color: black;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .tag-info {
        background: #3B82F6;
        color: white;
        padding: 2px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Main Banner Header
st.markdown("""
<div class="receivx-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-size: 28px; font-weight: 800; letter-spacing: -0.02em;">
                ⚡ RECEIVX <span style="font-size: 16px; font-weight: 500; color: #5EEAD4; margin-left: 10px;">CPSE–MSME Receivables Intelligence</span>
            </h1>
            <p style="margin: 6px 0 0 0; color: #CBD5E1; font-size: 14px;">
                Autonomous AI Layer from <strong>Created to Cash in Bank</strong> — Pre-Submission Gatekeeper • TReDS Multi-Exchange • MSMED Compliance
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(13, 148, 136, 0.3); border: 1px solid #0D9488; color: #5EEAD4; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600;">
                🟢 6 Autonomous Agents Active
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar: Supplier & Environment Context
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/null/financial-growth-analysis.png", width=64)
    st.subheader("MSME Supplier Profile")
    msme = db.get_msme("msme_precision_01")
    if msme:
        st.markdown(f"**{msme.legal_name}**")
        st.caption(f"Udyam: `{msme.udyam_number}` | Category: `{msme.category.value}`")
        st.markdown(f"**Bank OD/CC Facility:** `{float(msme.cash_credit_apr*100):.1f}% APR`")
        st.markdown(f"**Connected Rails:** RXIL, M1x, Invoicemart")
        st.markdown(f"**WhatsApp:** `{msme.whatsapp_number}`")
    
    st.divider()
    st.subheader("⚡ Quick Agent Actions")
    if st.button("🔄 Refresh Multi-Agent State", use_container_width=True):
        st.rerun()
    if st.button("🌱 Reset Sample Data", use_container_width=True):
        seed_database()
        st.success("Database restored to baseline seed.")
        st.rerun()

    st.caption("RECEIVX v2.0 • Microservices & AI Layer")

# Seven Core Navigation Tabs
tabs = st.tabs([
    "🌟 Command Center & Advisor",
    "🔍 Pre-Submission Gatekeeper",
    "⏱️ SLA & Acceptance Tracker",
    "⚖️ Statutory Escalator Desk",
    "💰 TReDS Financing Optimizer",
    "📈 Buyer Behaviour Graph",
    "💬 WhatsApp Bot Simulator"
])

# -----------------------------------------------------------------------------
# TAB 1: COMMAND CENTER & ADVISOR (AGENT 6)
# -----------------------------------------------------------------------------
with tabs[0]:
    advisor_summary = advisor_agent.generate_daily_actions("msme_precision_01")
    
    # 4 Top KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #38BDF8;">
            <div class="kpi-lbl">Active Receivables Book</div>
            <div class="kpi-val">₹{advisor_summary.total_active_receivables:,.0f}</div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">4 invoices across 3 CPSEs</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #EF4444;">
            <div class="kpi-lbl">MSMED Overdue (>45d)</div>
            <div class="kpi-val" style="color: #F87171;">₹{advisor_summary.total_overdue_msmed:,.0f}</div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Non-compliance with Sec 15</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #F59E0B;">
            <div class="kpi-lbl">Claimable Section 16 Interest</div>
            <div class="kpi-val" style="color: #FBBF24;">₹{advisor_summary.total_claimable_interest:,.0f}</div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">3x RBI Bank Rate (19.5% p.a.)</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #10B981;">
            <div class="kpi-lbl">Instant TReDS Liquidity</div>
            <div class="kpi-val" style="color: #34D399;">₹{advisor_summary.available_treds_liquidity:,.0f}</div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 4px;">Factoring ready for T+1 cash</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("🎯 Daily Next-Best-Action (NBA) Agenda")
    st.caption("Autonomous synthesis across all invoices: Ranked by urgency to maximize cash recovery and protect relationships.")

    for action in advisor_summary.actions:
        urgency_color = "#EF4444" if action.urgency.value == "IMMEDIATE_ACTION" else "#10B981" if action.urgency.value == "FINANCING_OPPORTUNITY" else "#3B82F6"
        with st.container():
            acol1, acol2 = st.columns([4, 1])
            with acol1:
                st.markdown(f"""
                <div style="background: #1E293B; border-left: 4px solid {urgency_color}; padding: 14px 18px; border-radius: 8px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; font-size: 15px; color: #F8FAFC;">{action.title}</span>
                        <span style="font-size: 11px; background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 4px; color: #E2E8F0;">{action.buyer_name}</span>
                    </div>
                    <div style="color: #CBD5E1; font-size: 13px; margin-top: 6px;">{action.rationale}</div>
                    <div style="color: #5EEAD4; font-size: 12px; margin-top: 4px;">⚡ Impact: {action.estimated_impact}</div>
                </div>
                """, unsafe_allow_html=True)
            with acol2:
                if action.action_type == "FIX_INVOICE":
                    if st.button("🛠️ Auto-Fix Now", key=action.action_id, use_container_width=True):
                        res = orchestrator.auto_remediate_invoice(action.invoice_id)
                        st.success(res["message"])
                        st.rerun()
                elif action.action_type == "ACCEPT_TREDS_BID":
                    if st.button("💰 Accept TReDS Bid", key=action.action_id, use_container_width=True):
                        fin = financier_agent.evaluate_financing(action.invoice_id)
                        if fin.best_offer:
                            treds_res = financier_agent.execute_bid_acceptance(fin.best_offer.id)
                            st.success(treds_res["message"])
                            st.rerun()
                elif action.action_type == "AUTHORIZE_ESCALATION":
                    if st.button("⚖️ Review Notice", key=action.action_id, use_container_width=True):
                        st.info("Navigating to Escalator Desk. Review draft and authorize below.")
                elif action.action_type == "SEND_NUDGE":
                    if st.button("📨 Dispatch Nudge", key=action.action_id, use_container_width=True):
                        tracker_agent.evaluate_invoice(action.invoice_id)
                        st.success(f"Follow-up dispatched to {action.buyer_name} Accounts.")

    st.divider()
    st.subheader("📊 12-Week Working Capital Cash-Flow Simulator (Agent 5)")
    st.caption("Comparing Direct CPSE Collections (P50 Payment Date) vs. RECEIVX TReDS Factoring Acceleration.")
    
    cf = forecaster_agent.simulate_cash_flow("msme_precision_01", starting_balance=500000.0)
    df_cf = pd.DataFrame([
        {
            "Week": w.week_start_date,
            "Direct Collection (₹)": w.direct_cumulative_cash,
            "TReDS Accelerated (₹)": w.treds_cumulative_cash,
            "Liquidity Buffer Saved (₹)": w.liquidity_gap_saved,
        }
        for w in cf.weeks
    ])
    st.line_chart(df_cf.set_index("Week")[["Direct Collection (₹)", "TReDS Accelerated (₹)"]], height=260)
    st.dataframe(df_cf, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 2: PRE-SUBMISSION GATEKEEPER (AGENT 1: VALIDATOR)
# -----------------------------------------------------------------------------
with tabs[1]:
    st.subheader("🔍 Agent 1: VALIDATOR — Pre-Submission 4-Way Gatekeeper")
    st.markdown("**Job:** Guarantee first-pass acceptance. Catch every rate, quantity, GST, and buyer-specific quirk *before* upload to eliminate the 15–30 day rejection loop.")

    invoices = db.list_invoices()
    inv_options = {f"{i.invoice_number} — {db.get_buyer(i.buyer_id).name if db.get_buyer(i.buyer_id) else i.buyer_id} (Status: {i.status.value})": i.id for i in invoices}
    
    selected_label = st.selectbox("Select Invoice for Pre-Submission Gatekeeper Audit:", list(inv_options.keys()), index=0)
    selected_inv_id = inv_options[selected_label]
    
    vcol1, vcol2 = st.columns([3, 2])
    with vcol1:
        # Run live Validator
        val_state = validator_agent.run_sync(selected_inv_id)
        
        # 5-Node Graph Visualizer
        st.markdown("""
        <div style="background: #1E293B; padding: 14px 20px; border-radius: 10px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.08);">
            <div style="font-size: 12px; color: #94A3B8; text-transform: uppercase; margin-bottom: 6px;">LangGraph Execution Pipeline</div>
            <div style="display: flex; gap: 8px; align-items: center; font-size: 13px;">
                <span style="background: #0D9488; color: white; padding: 4px 10px; border-radius: 6px;">1. Extract Docs</span> ➔
                <span style="background: #0D9488; color: white; padding: 4px 10px; border-radius: 6px;">2. 3-Way Match</span> ➔
                <span style="background: #0D9488; color: white; padding: 4px 10px; border-radius: 6px;">3. GST / IRN</span> ➔
                <span style="background: #0D9488; color: white; padding: 4px 10px; border-radius: 6px;">4. Buyer Rules (Moat)</span> ➔
                <span style="background: #0D9488; color: white; padding: 4px 10px; border-radius: 6px;">5. Verdict</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"### Verdict: **{val_state.verdict}**")
        st.progress(val_state.score, text=f"First-Pass Acceptance Probability: {int(val_state.score*100)}%")

        st.write("#### Detected Discrepancies & Learned Buyer Checks")
        if not val_state.flags:
            st.success("✅ Clean Invoice: 0 flags detected. Ready for CPSE portal upload.")
        else:
            for f in val_state.flags:
                tag_class = "tag-blocker" if f["severity"] == "BLOCKER" else "tag-warn" if f["severity"] == "WARN" else "tag-info"
                st.markdown(f"""
                <div style="background: #0F172A; padding: 10px 14px; border-radius: 8px; margin-bottom: 8px; border: 1px solid rgba(255,255,255,0.05);">
                    <span class="{tag_class}">{f['severity']}</span>
                    <strong style="margin-left: 8px; color: #F8FAFC;">{f['code']}</strong>
                    <div style="font-size: 13px; color: #CBD5E1; margin-top: 4px;">{f['detail']}</div>
                </div>
                """, unsafe_allow_html=True)
                
        if val_state.verdict != "READY":
            st.write("")
            if st.button("⚡ Apply Auto-Remediation (Fix Quantity to GRN & Stamp Udyam)", type="primary", use_container_width=True):
                rem_res = orchestrator.auto_remediate_invoice(selected_inv_id)
                st.success(rem_res["message"])
                st.rerun()

    with vcol2:
        st.subheader("📱 Proactive WhatsApp Alert to MSME")
        st.caption("The exact message delivered to the business owner before submission:")
        if val_state.whatsapp_message:
            st.markdown(f"""
            <div style="background: #111B21; border-radius: 12px; padding: 18px; border: 1px solid #2A3942; max-width: 400px; margin: auto;">
                <div style="font-size: 12px; color: #00A884; font-weight: 600; margin-bottom: 8px;">RECEIVX WhatsApp Bot • Outbound</div>
                <div class="whatsapp-chat-bubble-out" style="white-space: pre-wrap; font-family: monospace;">{val_state.whatsapp_message}</div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: SLA & ACCEPTANCE TRACKER (AGENT 2)
# -----------------------------------------------------------------------------
with tabs[2]:
    st.subheader("⏱️ Agent 2: TRACKER — Acceptance Velocity Engine")
    st.markdown("**Job:** Compress the buyer's acceptance window — the #1 hidden delay. Implements adaptive cadences and learns from buyer email replies.")

    tcol1, tcol2 = st.columns([3, 2])
    with tcol1:
        st.markdown("#### Monitored Receivables & Adaptive Follow-Up Policy")
        invoices = db.list_invoices()
        tracker_rows = []
        for inv in invoices:
            buyer = db.get_buyer(inv.buyer_id)
            stats = db.get_buyer_stats(inv.buyer_id)
            act = tracker_agent.evaluate_invoice(inv.id)
            tracker_rows.append({
                "Invoice No": inv.invoice_number,
                "Buyer": buyer.name.split("—")[0].strip() if buyer else inv.buyer_id,
                "Status": inv.status.value,
                "Days Pending": act.days_pending,
                "Buyer Median Acc.": f"{stats.avg_acceptance_days:.0f}d" if stats else "14d",
                "Next Policy Action": act.type.value,
            })
        st.dataframe(pd.DataFrame(tracker_rows), use_container_width=True, hide_index=True)

        st.divider()
        st.markdown("#### Manual Trigger: Execute Follow-Up Cadence")
        inv_to_track = st.selectbox("Select Invoice to inspect cadence:", [i.invoice_number for i in invoices], key="track_sel")
        matched_inv = [i for i in invoices if i.invoice_number == inv_to_track][0]
        act_res = tracker_agent.evaluate_invoice(matched_inv.id)
        
        st.info(f"**Policy Action:** `{act_res.type.value}` (Pending: {act_res.days_pending} days | T1: {act_res.t1_threshold}d, T2: {act_res.t2_threshold}d, T3: {act_res.t3_threshold}d)")
        if act_res.message_content:
            st.text_area("Generated Follow-up Communication:", act_res.message_content, height=180)
            if st.button("📤 Send Automated Dispatch via " + act_res.channel):
                st.success(f"Dispatched to {matched_inv.buyer_id} via {act_res.channel}.")

    with tcol2:
        st.markdown("#### 📥 Inbound Buyer Reply / IMAP Parser")
        st.caption("Simulate reading a CPSE accounts officer's email reply. Watch how the system extracts reasons and teaches Agent 1:")

        from_email = st.text_input("Buyer Email Sender", "stores.accounts@bhel.in")
        subject = st.text_input("Email Subject", "Re: Status of Tax Invoice INV/2026/088")
        email_body = st.text_area("Email Content", "Dear Vendor,\nInvoice INV/2026/088 is returned. Rejection reason: Vendor code was missing in billing subject header. Please rectify and resubmit.")
        
        if st.button("🤖 Parse Buyer Reply & Update Moat", use_container_width=True):
            parse_res = InboundEmailParser.process_buyer_email(from_email=from_email, subject=subject, body=email_body)
            st.success(f"Status extracted: **{parse_res['detected_status']}** | Reason: **{parse_res['extracted_reason']}**")
            if parse_res["learned_pattern_injected"]:
                st.info("🧠 **Feedback Loop Triggered:** New learned rejection pattern injected into Buyer Behaviour Graph! Agent 1 will now block this for all future invoices to this CPSE.")

# -----------------------------------------------------------------------------
# TAB 4: STATUTORY ESCALATOR DESK (AGENT 3)
# -----------------------------------------------------------------------------
with tabs[3]:
    st.subheader("⚖️ Agent 3: ESCALATOR — Rights-Enforcement Engine")
    st.markdown("**Job:** Convert legal rights MSMEs never exercise into automated leverage — with strict human-in-the-loop approval for relationship safety.")

    # Overdue Invoices
    overdue_invoices = [i for i in db.list_invoices() if i.status in [InvoiceLifecycleStatus.OVERDUE, InvoiceLifecycleStatus.DISPUTED]]
    if not overdue_invoices:
        overdue_invoices = db.list_invoices()

    sel_esc_inv_no = st.selectbox("Select Overdue Invoice for Legal Escalation:", [i.invoice_number for i in overdue_invoices], key="esc_sel")
    esc_inv = [i for i in overdue_invoices if i.invoice_number == sel_esc_inv_no][0]
    
    rec = escalator_agent.recommend_escalation(esc_inv.id)

    ecol1, ecol2 = st.columns([1, 2])
    with ecol1:
        st.markdown("### Accrued Statutory Dues")
        st.metric("Principal Outstanding", f"₹{rec.principal_amount:,.2f}")
        st.metric("Accrued Section 16 Interest", f"₹{rec.accrued_interest:,.2f}", f"{rec.days_overdue} days overdue")
        st.metric("Total Claimable Recoverable", f"₹{rec.total_claimable:,.2f}")

        st.markdown("---")
        st.markdown(f"**Recommended Step:** `Step {rec.recommended_step.step_number}`")
        st.markdown(f"**Action:** `{rec.recommended_step.action_name}`")
        st.markdown(f"**Relationship Risk:** `{rec.recommended_step.relationship_risk}`")
        st.markdown(f"**Historical Effectiveness:** `{int(rec.recommended_step.typical_effectiveness*100)}%`")
        st.markdown(f"**Human Approval Required:** `{'YES 🔒' if rec.recommended_step.requires_human_approval else 'NO'}`")

        if rec.recommended_step.requires_human_approval:
            st.warning("⚠️ **Human-in-the-Loop Gate:** Escalation steps > 2 require explicit authorization to safeguard buyer relationships.")
            if st.button("✅ Authorize Digital Execution & Dispatch", type="primary", use_container_width=True):
                exec_res = escalator_agent.execute_escalation_step(esc_inv.id, rec.recommended_step.step_number)
                st.success(exec_res["message"])
                st.rerun()

    with ecol2:
        st.markdown("### Generated Legal Document Draft")
        st.text_area("Legal Instrument Draft:", rec.escalation_content, height=420)
        st.download_button(
            label=f"📥 Download {rec.recommended_step.action_name} (.txt)",
            data=rec.escalation_content,
            file_name=f"RECEIVX_{rec.recommended_step.action_code}_{esc_inv.invoice_number.replace('/', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

# -----------------------------------------------------------------------------
# TAB 5: TREDS FINANCING OPTIMIZER (AGENT 4)
# -----------------------------------------------------------------------------
with tabs[4]:
    st.subheader("💰 Agent 4: FINANCIER — TReDS Multi-Exchange Auction & OD Optimizer")
    st.markdown("**Job:** Turn receivables into immediate cash on optimal terms across RXIL, M1xchange, Invoicemart, and C2FO.")

    f_invoices = [i for i in db.list_invoices() if i.treds_ready or i.status == InvoiceLifecycleStatus.TREDS_LISTED]
    if not f_invoices:
        f_invoices = db.list_invoices()

    fin_inv_no = st.selectbox("Select Invoice to Optimize Financing:", [i.invoice_number for i in f_invoices], key="fin_sel")
    fin_target_inv = [i for i in f_invoices if i.invoice_number == fin_inv_no][0]

    fin_analysis = financier_agent.evaluate_financing(fin_target_inv.id)

    fcol1, fcol2 = st.columns([1, 1])
    with fcol1:
        st.markdown("### Financial Comparison: TReDS vs. Bank OD")
        st.metric("Invoice Face Value", f"₹{fin_analysis.invoice_amount:,.2f}")
        st.metric("TReDS Financing Cost (Best Bid)", f"₹{fin_analysis.treds_discount_cost:,.2f}", f"APR: {float(fin_analysis.best_offer.discount_rate_apr*100 if fin_analysis.best_offer else 8.2):.1f}%")
        st.metric("Supplier Bank OD/CC Cost", f"₹{fin_analysis.bank_od_cost:,.2f}", f"APR: {float(fin_analysis.msme_cc_od_apr*100):.1f}%")
        st.metric("Net Working Capital Savings", f"₹{fin_analysis.net_working_capital_savings:,.2f}", f"Spread: +{fin_analysis.effective_apr_spread:.1f}%")

        if fin_analysis.recommended_action == "ACCEPT_TREDS_BID":
            st.success(f"✅ **Recommended Action: ACCEPT TREDS BID** (Saves ₹{fin_analysis.net_working_capital_savings:,.2f} vs Bank OD)")
        else:
            st.warning("⚠️ **Action: HOLD / SELF-FINANCE**")

    with fcol2:
        st.markdown("### Multi-Exchange Live Auction Stream")
        if not fin_analysis.all_offers:
            st.info("No live bids currently open. Buyer must be registered on TReDS.")
        else:
            for off in fin_analysis.all_offers:
                is_best = fin_analysis.best_offer and off.id == fin_analysis.best_offer.id
                border_style = "border: 2px solid #10B981;" if is_best else "border: 1px solid rgba(255,255,255,0.08);"
                st.markdown(f"""
                <div style="background: #1E293B; {border_style} padding: 12px 16px; border-radius: 8px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #F8FAFC;">{off.platform} — {off.financier}</span>
                        <span style="background: #0D9488; color: white; padding: 2px 8px; border-radius: 4px; font-weight: 700; font-size: 13px;">{float(off.discount_rate_apr*100):.2f}% APR</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #94A3B8; margin-top: 6px;">
                        <span>Net Payout: ₹{off.net_amount:,.2f}</span>
                        <span>Status: {off.status}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if off.status == "OPEN":
                    if st.button(f"⚡ Accept {off.platform} Bid (Lock Payout)", key=f"acc_{off.id}", use_container_width=True):
                        res = financier_agent.execute_bid_acceptance(off.id)
                        st.success(res["message"])
                        st.rerun()

# -----------------------------------------------------------------------------
# TAB 6: BUYER BEHAVIOUR GRAPH (AGENT 5 & THE MOAT)
# -----------------------------------------------------------------------------
with tabs[5]:
    st.subheader("📈 Buyer Behaviour Intelligence Graph (The Moat)")
    st.markdown("Proprietary rejection patterns and payment distributions mined per CPSE unit across thousands of invoice lifecycles.")

    buyers = db.list_buyers()
    b_options = {b.name: b.id for b in buyers}
    b_sel = st.selectbox("Select CPSE Entity to inspect Graph Intelligence:", list(b_options.keys()))
    sel_buyer_id = b_options[b_sel]
    
    b_stats = db.get_buyer_stats(sel_buyer_id)
    b_rules = db.get_buyer_rules(sel_buyer_id)

    bcol1, bcol2, bcol3 = st.columns(3)
    with bcol1:
        st.metric("Avg. Days to Accept (SLA)", f"{b_stats.avg_acceptance_days:.1f} Days" if b_stats else "N/A")
    with bcol2:
        st.metric("Historical DSO (Settlement)", f"{b_stats.avg_payment_days:.1f} Days" if b_stats else "N/A")
    with bcol3:
        st.metric("Rejection Rate", f"{int(b_stats.rejection_rate*100)}%" if b_stats else "N/A", f"On-time: {int(b_stats.on_time_rate*100)}%" if b_stats else "")

    st.markdown("#### Learned Rejection Rules ('THE MOAT')")
    if not b_rules:
        st.info("No specific rejection rules recorded for this unit yet.")
    else:
        for r in b_rules:
            st.markdown(f"""
            <div style="background: #1E293B; border-left: 4px solid #F59E0B; padding: 12px 16px; border-radius: 8px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between;">
                    <strong style="color: #F8FAFC;">{r.rule_name} ({r.rule_code})</strong>
                    <span style="color: #EF4444; font-size: 12px; font-weight: 600;">Caused {r.rejection_count} Past Rejections</span>
                </div>
                <div style="color: #CBD5E1; font-size: 13px; margin-top: 4px;">{r.human_reason}</div>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 7: WHATSAPP BOT SIMULATOR
# -----------------------------------------------------------------------------
with tabs[6]:
    st.subheader("💬 WhatsApp-First Vernacular Conversational Interface")
    st.markdown("MSME business owners interact through WhatsApp. Voice-enabled, vernacular, with 1-tap actionable decisions.")

    wcol1, wcol2 = st.columns([2, 1])
    with wcol1:
        # Smartphone Mockup Shell
        st.markdown("""
        <div style="background: #0B141A; border: 3px solid #2A3942; border-radius: 24px; padding: 16px; max-width: 500px; margin: auto; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
            <div style="background: #202C33; padding: 10px 16px; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="background: #00A884; color: white; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700;">RX</span>
                    <div>
                        <div style="color: #E9EDEF; font-weight: 600; font-size: 14px;">RECEIVX Official Assistant</div>
                        <div style="color: #8696A0; font-size: 11px;">Verified Business Account • Online</div>
                    </div>
                </div>
                <span style="color: #00A884; font-size: 12px;">🔒 256-bit</span>
            </div>
            <div style="height: 380px; overflow-y: auto; padding: 6px;">
        """, unsafe_allow_html=True)

        for m in whatsapp.MESSAGE_HISTORY[-6:]:
            bubble_class = "whatsapp-chat-bubble-out" if m.get("direction") == "OUTBOUND" else "whatsapp-chat-bubble-in"
            st.markdown(f'<div class="{bubble_class}">{m["message"]}</div>', unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)

    with wcol2:
        st.markdown("### Try WhatsApp Interactive Simulation")
        st.caption("Type a message or click quick-actions:")
        
        q1, q2 = st.columns(2)
        with q1:
            if st.button("FIX", key="wa_fix", use_container_width=True):
                whatsapp.handle_inbound_message("+919876543210", "FIX")
                st.rerun()
            if st.button("STATUS", key="wa_status", use_container_width=True):
                whatsapp.handle_inbound_message("+919876543210", "STATUS")
                st.rerun()
        with q2:
            if st.button("ACCEPT", key="wa_accept", use_container_width=True):
                whatsapp.handle_inbound_message("+919876543210", "ACCEPT")
                st.rerun()
            if st.button("APPROVE", key="wa_approve", use_container_width=True):
                whatsapp.handle_inbound_message("+919876543210", "APPROVE")
                st.rerun()

        st.write("")
        user_msg = st.text_input("Send message to RECEIVX Bot:", placeholder="e.g. FIX, STATUS, ACCEPT")
        if st.button("Send 📤", use_container_width=True) and user_msg:
            whatsapp.handle_inbound_message("+919876543210", user_msg)
            st.rerun()

        st.divider()
        st.markdown("🎙️ **Simulate Vernacular Voice Note**")
        st.caption("Hindi Audio Simulation: *'नमस्ते, एनटीपीसी वाले बिल का क्या स्टेटस है?'*")
        if st.button("▶️ Play & Process Hindi Voice Query"):
            whatsapp.handle_inbound_message("+919876543210", "STATUS")
            st.rerun()
