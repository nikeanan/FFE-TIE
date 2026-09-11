import os
import sys
from datetime import date
from decimal import Decimal

# Ensure project root in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.database.db_session import db
from src.database.seed_data import seed_database
from src.agents.validator_agent import validator_agent
from src.agents.tracker_agent import tracker_agent, InboundEmailParser
from src.agents.escalator_agent import escalator_agent
from src.agents.financier_agent import financier_agent
from src.agents.forecaster_agent import forecaster_agent
from src.agents.advisor_agent import advisor_agent
from src.agents.orchestrator import orchestrator


def main():
    print("=" * 80)
    print("⚡ RECEIVX — CPSE–MSME Receivables Intelligence Platform")
    print("Autonomous AI Layer from Created to Cash-in-Bank (6-Agent Demonstration)")
    print("=" * 80)

    # 0. Seed Database
    seed_database()
    print(f"\n[INIT] Seeded Database: {len(db.buyers)} CPSE Buyers | {len(db.invoices)} Invoices")

    # 1. AGENT 1: VALIDATOR (Pre-Submission Gatekeeper)
    print("\n" + "-" * 70)
    print("🔍 [AGENT 1: VALIDATOR] Auditing Pre-Submission Invoice INV/2026/2041 (NTPC Dadri)")
    val_res = validator_agent.run_sync("inv_ntpc_2041")
    print(f"• Verdict: {val_res.verdict} | First-Pass Acceptance Score: {int(val_res.score*100)}%")
    print(f"• Flags Detected ({len(val_res.flags)}):")
    for f in val_res.flags:
        print(f"   - [{f['severity']}] {f['code']}: {f['detail']}")

    print("\n📱 [WHATSAPP OUTBOUND ALERT TO MSME]:")
    print(val_res.whatsapp_message)

    # Auto-Remediation Demonstration
    print("\n⚡ [AUTO-REMEDIATION]: MSME replies 'FIX' -> Adjusting quantity to GRN & Stamping Udyam...")
    rem_res = orchestrator.auto_remediate_invoice("inv_ntpc_2041")
    print(f"• Result: {rem_res['message']} (New Score: {int(rem_res['new_score']*100)}%)")

    # 2. AGENT 2: TRACKER (Acceptance Velocity Engine)
    print("\n" + "-" * 70)
    print("⏱️ [AGENT 2: TRACKER] Monitoring Acceptance Velocity & Adaptive Cadence")
    track_res = tracker_agent.evaluate_invoice("inv_ongc_112")
    print(f"• Invoice INV/2026/112 at ONGC: Pending {track_res.days_pending} days")
    print(f"• Dynamic Thresholds: T1={track_res.t1_threshold}d, T2={track_res.t2_threshold}d, T3={track_res.t3_threshold}d")
    print(f"• Policy Recommendation: {track_res.type.value} via {track_res.channel}")

    print("\n🧠 [IMAP FEEDBACK LOOP]: Simulating Buyer Rejection Email from BHEL Accounts...")
    email_res = InboundEmailParser.process_buyer_email(
        from_email="stores.accounts@bhel.in",
        subject="Re: Bill Discrepancy INV/2026/088",
        body="Invoice returned. Reason: Missing BHEL internal vendor code in subject header.",
    )
    print(f"• Extracted Status: {email_res['detected_status']} | Reason: {email_res['extracted_reason']}")
    print(f"• The Moat Updated: New learned rejection rule auto-injected into Buyer Graph!")

    # 3. AGENT 3: ESCALATOR (Rights-Enforcement Engine)
    print("\n" + "-" * 70)
    print("⚖️ [AGENT 3: ESCALATOR] Statutory Enforcement for Overdue Receivables")
    esc_rec = escalator_agent.recommend_escalation("inv_ntpc_045")
    print(f"• Invoice INV/2026/045: {esc_rec.days_overdue} days overdue")
    print(f"• Outstanding Principal: INR {esc_rec.principal_amount:,.2f}")
    print(f"• Sec 16 Penal Interest (3x RBI Bank Rate, compounded monthly): INR {esc_rec.accrued_interest:,.2f}")
    print(f"• Total Claimable: INR {esc_rec.total_claimable:,.2f}")
    print(f"• Recommended Action: Step {esc_rec.recommended_step.step_number} — {esc_rec.recommended_step.action_name}")
    print(f"• Human-in-the-Loop Gate: {esc_rec.human_approval_status}")

    # 4. AGENT 4: FINANCIER (TReDS & Liquidity Optimizer)
    print("\n" + "-" * 70)
    print("💰 [AGENT 4: FINANCIER] TReDS Multi-Exchange Auction vs. Bank OD Optimization")
    fin_res = financier_agent.evaluate_financing("inv_bhel_088")
    print(f"• Invoice Amount: INR {fin_res.invoice_amount:,.2f} | Maturity: {fin_res.days_to_maturity} days")
    print(f"• Best TReDS Factoring Bid: {fin_res.best_offer.platform} by {fin_res.best_offer.financier} at {float(fin_res.best_offer.discount_rate_apr*100):.2f}% APR")
    print(f"• Supplier Bank Cash Credit / OD Rate: {float(fin_res.msme_cc_od_apr*100):.1f}% APR")
    print(f"• Net Working Capital Saved: INR {fin_res.net_working_capital_savings:,.2f} (Spread: +{fin_res.effective_apr_spread:.1f}%)")
    print(f"• Recommendation: {fin_res.recommended_action}")

    # 5. AGENT 5: FORECASTER (Buyer Behaviour ML Graph)
    print("\n" + "-" * 70)
    print("📈 [AGENT 5: FORECASTER] Predictive Settlement Dates & Cash-Flow Runway")
    pred = forecaster_agent.predict_settlement("inv_bhel_088")
    print(f"• Buyer: {pred.buyer_name}")
    print(f"• Statutory Due Date: {pred.statutory_due_date}")
    print(f"• Predicted P10 Date (Optimistic): {pred.predicted_p10_date}")
    print(f"• Predicted P50 Date (Median):     {pred.predicted_p50_date}")
    print(f"• Predicted P90 Date (Conservative): {pred.predicted_p90_date}")
    print(f"• Forecast Factors: {', '.join(pred.factors[:2])}")

    # 6. AGENT 6: ADVISOR (Daily Next-Best-Action Agenda)
    print("\n" + "-" * 70)
    print("🌟 [AGENT 6: ADVISOR] Daily Next-Best-Action Agenda for MSME Owner")
    agenda = advisor_agent.generate_daily_actions("msme_precision_01")
    print(f"• Active Book: INR {agenda.total_active_receivables:,.2f} | Overdue: INR {agenda.total_overdue_msmed:,.2f}")
    print(f"• Total Actions Queued: {len(agenda.actions)}")
    for i, act in enumerate(agenda.actions, 1):
        print(f"   {i}. [{act.urgency.value}] {act.title} -> Impact: {act.estimated_impact}")

    print("\n" + "=" * 80)
    print("✅ RECEIVX Multi-Agent Pipeline Completed Successfully.")
    print("=" * 80)


if __name__ == "__main__":
    main()
