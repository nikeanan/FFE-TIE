#!/usr/bin/env python3
"""CECI — Civil Engineering Evidence & Claims Intelligence: 5-Contractor Live Pilot & Proof-of-Value CLI.

Demonstrates automated variation claim recovery, Time Impact Analysis (TIA), 
statutory price escalation (CPWD 10CA/10CC & FIDIC 13.7), and liquidated damage (LD) protection
across 5 mega-infrastructure projects in India.
"""
import sys
import os
import time

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure project directory is in python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.pilot.pilot_contractors import PILOT_CONTRACTORS
from src.pilot.pilot_evaluator import ceci_pilot_evaluator, CECIPilotReport


def print_banner():
    print("=" * 82)
    print("  ⚖️  CECI — CIVIL EVIDENCE & CLAIMS INTELLIGENCE PILOT SUITE")
    print("  Multi-Modal Evidence Graph, EoT Time Impact & Variation Claims Engine")
    print("  Standards: FIDIC Red/Yellow • CPWD Cl 12/5/10CA/10CC • NHAI EPC Schedule J")
    print("=" * 82)
    print()


def run_full_pilot_audit():
    print_banner()
    print("🚀 Running Automated Claims Audit across 5 Mega-Infrastructure Contractors...\n")
    time.sleep(0.5)

    report: CECIPilotReport = ceci_pilot_evaluator.run_all_pilots()

    print(f"📊 SUMMARY AUDIT BENCHMARK — {report.total_contractors_audited} INFRASTRUCTURE PROJECTS")
    print("-" * 82)
    print(f"  • Total Portfolio Contract Value:  ₹ {report.total_contract_value_cr:,.1f} Crores")
    print(f"  • Approved BOQ Variation Claims:    ₹ {report.total_variation_claims_inr:,.2f} (₹ {report.total_variation_claims_inr/10000000:.2f} Cr)")
    print(f"  • Prolongation Site Overheads:      ₹ {report.total_prolongation_claims_inr:,.2f} (₹ {report.total_prolongation_claims_inr/10000000:.2f} Cr)")
    print(f"  • Statutory Material Escalations:   ₹ {report.total_escalation_claims_inr:,.2f} (₹ {report.total_escalation_claims_inr/10000000:.2f} Cr)")
    print(f"  • Liquidated Damages (LD) Shielded: ₹ {report.total_ld_liability_shielded_inr:,.2f} (₹ {report.total_ld_liability_shielded_inr/10000000:.2f} Cr)")
    print(f"  --------------------------------------------------------------------------------")
    print(f"  🌟 TOTAL VALUE UNLOCKED BY CECI:    ₹ {report.total_monetary_value_unlocked_inr:,.2f} (₹ {report.total_monetary_value_unlocked_inr/10000000:.2f} Cr)")
    print("-" * 82)
    print()

    print("📋 CONTRACTOR-BY-CONTRACTOR BREAKDOWN:")
    print("=" * 82)

    for idx, r in enumerate(report.results, 1):
        print(f"[{idx}/5] {r.contractor_name}")
        print(f"     Project:    {r.project_name}")
        print(f"     Authority:  {r.client_authority}")
        print(f"     Contract:   {r.contract_type}")
        print(f"     ----------------------------------------------------------------------------")
        print(f"     💰 Variation Claim Approved:     ₹ {r.variation_claim_amount_inr:>12,.2f} (+{r.variation_percent:.1f}% deviation)")
        print(f"     ⏱️  Extension of Time (EoT):      {r.eot_days_approved:>12} Days Approved")
        print(f"     🏢 Prolongation Overhead Claim:  ₹ {r.prolongation_cost_recovered_inr:>12,.2f}")
        print(f"     📈 Price Escalation Claim:       ₹ {r.escalation_claim_amount_inr:>12,.2f}")
        print(f"     🛡️  LD Liability Shielded:        ₹ {r.ld_liability_shielded_inr:>12,.2f}")
        print(f"     🔥 Net Financial Delta:          ₹ {r.total_financial_impact_inr:>12,.2f}")
        print(f"     📜 Notice Compliance:           {r.notice_compliance_status}")
        print(f"     🛠️  CECI Remediation:            {r.ceci_remediation_summary}")
        print("=" * 82)
        print()


def interactive_menu():
    while True:
        print_banner()
        print("Select an option:")
        print("  [1] Run Full 5-Contractor Claims & Proof-of-Value Audit")
        print("  [2] Inspect Specific Infrastructure Contractor")
        print("  [3] Launch Streamlit Visual Interactive Dashboard")
        print("  [4] Exit")
        print()

        choice = input("Enter choice [1-4]: ").strip()

        if choice == "1":
            run_full_pilot_audit()
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            contractor_keys = list(PILOT_CONTRACTORS.keys())
            print("\nSelect Contractor:")
            for i, k in enumerate(contractor_keys, 1):
                p = PILOT_CONTRACTORS[k]
                print(f"  [{i}] {p.contractor_name} — {p.scenario.project_name}")
            print()
            sub_choice = input(f"Enter choice [1-{len(contractor_keys)}]: ").strip()
            try:
                sel_idx = int(sub_choice) - 1
                if 0 <= sel_idx < len(contractor_keys):
                    profile = PILOT_CONTRACTORS[contractor_keys[sel_idx]]
                    res = ceci_pilot_evaluator.evaluate_contractor(profile)
                    print("\n" + "=" * 80)
                    print(f"🏗️  {profile.contractor_name}")
                    print(f"Headquarters:       {profile.headquarters}")
                    print(f"Lead Specialist:    {profile.lead_contract_specialist}")
                    print(f"Project:            {profile.scenario.project_name}")
                    print(f"Client Authority:   {profile.scenario.client_authority}")
                    print(f"Contract Value:     ₹ {profile.scenario.tender_contract_value_cr:,.1f} Cr")
                    print("-" * 80)
                    print(f"Variation Claim:    ₹ {res.variation_claim_amount_inr:,.2f}")
                    print(f"EoT Days Granted:   {res.eot_days_approved} Days")
                    print(f"Prolongation Cost:  ₹ {res.prolongation_cost_recovered_inr:,.2f}")
                    print(f"Escalation Claim:   ₹ {res.escalation_claim_amount_inr:,.2f}")
                    print(f"LD Risk Shielded:   ₹ {res.ld_liability_shielded_inr:,.2f}")
                    print(f"Total Value:        ₹ {res.total_financial_impact_inr:,.2f}")
                    print("=" * 80)
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input.")
            input("\nPress Enter to return to menu...")
        elif choice == "3":
            print("\nLaunching Streamlit Dashboard: streamlit run app.py ...")
            os.system("streamlit run app.py")
            break
        elif choice == "4":
            print("\nExiting CECI Pilot Runner. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please choose 1, 2, 3, or 4.")
            time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_full_pilot_audit()
    else:
        run_full_pilot_audit()
