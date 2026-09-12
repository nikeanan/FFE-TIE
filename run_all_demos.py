#!/usr/bin/env python3
"""Unified CLI Demo Runner for all 4 AI-Enabled B2B Ventures (FFE-TIE Portfolio).

Executes live pilot demonstrations and proof-of-value audits across:
1. CPSE-MSME Receivables Agent (5 MSME Suppliers)
2. Construction Material Intelligence (5 Ready-Mix Concrete & EPC Plants)
3. Civil Evidence & Claims Intelligence (5 Mega-Infrastructure Contractors)
4. WaterResilience AI (5 Smart City Municipal Corporations)
"""
import sys
import os
import subprocess
import time

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

PROJECTS = [
    {
        "id": "01",
        "name": "CPSE–MSME Receivables Agent",
        "dir": os.path.join(ROOT_DIR, "01_cpse_msme_receivables_agent"),
        "script": "run_pilot_demo.py",
        "description": "5 MSME Suppliers • GeM CRAC • TReDS • MSMED Sec 15/16 Interest",
    },
    {
        "id": "02",
        "name": "Construction Material Intelligence (CMI)",
        "dir": os.path.join(ROOT_DIR, "02_construction_material_intelligence"),
        "script": "run_pilot_demo.py",
        "description": "5 RMC Plants • Moisture Anomaly • IS 10262 / ASTM C1074 • Carbon Offset",
    },
    {
        "id": "03",
        "name": "Civil Evidence & Claims Intelligence (CECI)",
        "dir": os.path.join(ROOT_DIR, "03_civil_evidence_claims_intelligence"),
        "script": "run_pilot_demo.py",
        "description": "5 Mega-Contractors • FIDIC / CPWD Cl 12/5/10CA • Time Impact Analysis • LD Shield",
    },
    {
        "id": "04",
        "name": "WaterResilience AI (WRAI)",
        "dir": os.path.join(ROOT_DIR, "04_water_resilience_ai"),
        "script": "run_pilot_demo.py",
        "description": "5 Smart Cities • 1D/2D Stormwater Hydraulics • Sponge City SUDS • Aquifer Recharge",
    },
]


def print_header():
    print("=" * 84)
    print("  🌟  FFE-TIE MASTER PORTFOLIO — 4 AI-ENABLED B2B VENTURES")
    print("  Executive Live Pilot Benchmark & Zero-Rejection Proof-of-Value Suite")
    print("=" * 84)
    print()


def run_project_demo(proj_idx: int):
    p = PROJECTS[proj_idx]
    print(f"\n🚀 Running Live Pilot Demo for [{p['id']}] {p['name']}...")
    print(f"   Directory: {p['dir']}")
    print("-" * 84)
    script_path = os.path.join(p["dir"], p["script"])
    subprocess.run([sys.executable, script_path, "--auto"], cwd=p["dir"])


def run_all_in_sequence():
    print_header()
    print("Running all 4 venture pilot audits in sequence (20 Production Entities Total)...\n")
    time.sleep(1)
    for i in range(len(PROJECTS)):
        run_project_demo(i)
        if i < len(PROJECTS) - 1:
            print("\n" + "=" * 84 + "\n")
            time.sleep(0.5)


def interactive_menu():
    while True:
        print_header()
        print("Select a venture demo to run:")
        for idx, p in enumerate(PROJECTS, 1):
            print(f"  [{idx}] {p['name']}")
            print(f"      👉 {p['description']}")
        print("  [5] 🚀 Run ALL 4 Venture Pilots in Sequence (Full Portfolio Audit)")
        print("  [6] 🌐 Launch Unified Master Streamlit Hub (app.py)")
        print("  [7] 🧪 Run All 52 Pytest Unit Tests across Portfolio")
        print("  [8] Exit")
        print()

        choice = input("Enter choice [1-8]: ").strip()

        if choice in ["1", "2", "3", "4"]:
            run_project_demo(int(choice) - 1)
            input("\nPress Enter to return to main menu...")
        elif choice == "5":
            run_all_in_sequence()
            input("\nPress Enter to return to main menu...")
        elif choice == "6":
            print("\nLaunching Streamlit Master Hub...")
            subprocess.run(["uv", "run", "--with", "streamlit,pandas,pydantic,numpy,networkx,scipy", "streamlit", "run", "app.py"], cwd=ROOT_DIR)
            break
        elif choice == "7":
            print("\nRunning complete 52-test test suite across all 4 projects...")
            for p in PROJECTS:
                print(f"\n--- Testing {p['name']} ---")
                subprocess.run(["uv", "run", "--with", "pytest,pydantic,numpy,pandas,networkx,scipy", "pytest", "tests/"], cwd=p["dir"])
            input("\nPress Enter to return to main menu...")
        elif choice == "8":
            print("\nExiting Master Portfolio Runner. Thank you!")
            break
        else:
            print("\nInvalid selection. Please enter a number between 1 and 8.")
            time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        run_all_in_sequence()
    else:
        interactive_menu()
