#!/usr/bin/env python3
"""WRAI — WaterResilience AI: 5-City Smart Flood & Sponge City Pilot CLI.

Demonstrates automated 1D/2D urban flood simulation, conduit surcharge assessment,
Sponge City (SUDS) optimization, and Managed Aquifer Recharge across 5 Indian mega-cities
(Bengaluru, Mumbai, Chennai, Gurugram, Hyderabad).
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

from src.pilot.pilot_cities import PILOT_CITIES
from src.pilot.pilot_evaluator import wrai_pilot_evaluator, WRAIPilotReport


def print_banner():
    print("=" * 82)
    print("  🌊  WRAI — WATER RESILIENCE AI PILOT SUITE")
    print("  Physics-Informed Stormwater Hydraulics & Sponge City (SUDS) Optimizer")
    print("  Standards: CPHEEO Drainage Manual • MoHUA Guidelines • NDMA Flood Norms")
    print("=" * 82)
    print()


def run_full_pilot_audit():
    print_banner()
    print("🚀 Running Automated Urban Flood Resilience Simulations across 5 Smart Cities...\n")
    time.sleep(0.5)

    report: WRAIPilotReport = wrai_pilot_evaluator.run_all_pilots()

    print(f"📊 SUMMARY AUDIT BENCHMARK — {report.total_cities_audited} SMART CITIES / MUNICIPALITIES")
    print("-" * 82)
    print(f"  • Total Drainage Area Modeled:       {report.total_catchment_area_ha:,.0f} Hectares")
    print(f"  • Total Baseline Flood Risk:        ₹ {report.total_baseline_damage_risk_cr:,.2f} Crores")
    print(f"  • Total Sponge City / SUDS Capex:   ₹ {report.total_intervention_capex_cr:,.2f} Crores")
    print(f"  • Total Flood Damage Prevented:     ₹ {report.total_flood_damage_prevented_cr:,.2f} Crores")
    print(f"  • Annual Groundwater Harvested:     {report.total_annual_water_harvested_mld:,.2f} MLD (Million Liters/Day)")
    print(f"  • Annual Freshwater Value:          ₹ {report.total_annual_water_value_cr:,.2f} Cr / Year")
    print(f"  --------------------------------------------------------------------------------")
    print(f"  🌟 AVERAGE BENEFIT-COST RATIO (BCR): {report.average_benefit_cost_ratio:.2f}x Municipal ROI")
    print("-" * 82)
    print()

    print("📋 CITY-BY-CITY BREAKDOWN:")
    print("=" * 82)

    for idx, r in enumerate(report.results, 1):
        print(f"[{idx}/5] {r.city_name} — {r.municipal_authority}")
        print(f"     Critical Zone:     {r.zone_name}")
        print(f"     Catchment Area:    {r.catchment_area_ha:.0f} ha | Peak Discharge: {r.peak_inflow_discharge_m3s:.1f} m³/s")
        print(f"     ----------------------------------------------------------------------------")
        print(f"     🌊 Baseline Flood Depth:   {r.baseline_flood_depth_m:.2f} m ({r.baseline_flood_volume_m3:,.0f} m³ flood volume)")
        print(f"     💸 Baseline Damage Risk:   ₹ {r.baseline_economic_loss_cr:>8.2f} Crores")
        print(f"     🛠️  Intervention:          {r.recommended_intervention}")
        print(f"     💰 Capex Investment:       ₹ {r.capex_cost_cr:>8.2f} Crores")
        print(f"     🛡️  Post-Intervention Depth: {r.post_intervention_flood_depth_m:.2f} m (Below Inundation Damage Level)")
        print(f"     🛡️  Flood Damage Prevented: ₹ {r.flood_damage_prevented_cr:>8.2f} Crores")
        print(f"     💧 Aquifer Recharged:      {r.annual_groundwater_recharge_mld:>8.2f} MLD")
        print(f"     🌟 Municipal BCR:          {r.benefit_cost_ratio_bcr:>8.2f}x ROI")
        print(f"     🔬 WRAI Solution:          {r.wrai_remediation_summary}")
        print("=" * 82)
        print()


def interactive_menu():
    while True:
        print_banner()
        print("Select an option:")
        print("  [1] Run Full 5-City Flood Resilience & Sponge City Audit")
        print("  [2] Inspect Specific Smart City Catchment")
        print("  [3] Launch Streamlit Visual Interactive Dashboard")
        print("  [4] Exit")
        print()

        choice = input("Enter choice [1-4]: ").strip()

        if choice == "1":
            run_full_pilot_audit()
            input("\nPress Enter to return to menu...")
        elif choice == "2":
            city_keys = list(PILOT_CITIES.keys())
            print("\nSelect City:")
            for i, k in enumerate(city_keys, 1):
                p = PILOT_CITIES[k]
                print(f"  [{i}] {p.city_name} — {p.scenario.zone_name}")
            print()
            sub_choice = input(f"Enter choice [1-{len(city_keys)}]: ").strip()
            try:
                sel_idx = int(sub_choice) - 1
                if 0 <= sel_idx < len(city_keys):
                    profile = PILOT_CITIES[city_keys[sel_idx]]
                    res = wrai_pilot_evaluator.evaluate_city(profile)
                    print("\n" + "=" * 80)
                    print(f"🏙️  {profile.city_name} — {profile.municipal_authority}")
                    print(f"Zone:                {profile.scenario.zone_name}")
                    print(f"Mission Lead:        {profile.smart_city_mission_lead}")
                    print("-" * 80)
                    print(f"Baseline Flood:      {res.baseline_flood_depth_m:.2f} meters (₹ {res.baseline_economic_loss_cr:.2f} Cr Damage Risk)")
                    print(f"Intervention:        {res.recommended_intervention}")
                    print(f"Capex:               ₹ {res.capex_cost_cr:.2f} Cr")
                    print(f"Post-Intervention:   {res.post_intervention_flood_depth_m:.2f} meters")
                    print(f"Damage Prevented:    ₹ {res.flood_damage_prevented_cr:.2f} Cr")
                    print(f"Water Recharged:     {res.annual_groundwater_recharge_mld:.2f} MLD")
                    print(f"Municipal BCR:       {res.benefit_cost_ratio_bcr:.2f}x ROI")
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
            print("\nExiting WRAI Pilot Runner. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please choose 1, 2, 3, or 4.")
            time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        run_full_pilot_audit()
    else:
        run_full_pilot_audit()
