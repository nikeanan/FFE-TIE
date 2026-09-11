# FFE TIE - AI-Enabled B2B Business Portfolio

This repository contains the complete architecture, source engines, REST APIs, Streamlit web applications, unit tests, and documentation for four shortlisted AI-enabled B2B business opportunities.

---

## Portfolio Overview

```
c:\Projects\FFE TIE
│
├── README.md                                          <-- Portfolio & Developer Guide
├── PRESENTATION_DECK.md                               <-- Professor Review Slide Deck
│
├── 01_cpse_msme_receivables_agent/                    <-- [Best Standalone Business]
│   ├── docs/BUSINESS_CASE.md
│   ├── data/sample_invoices.json
│   ├── src/ (schema, reconciliation, msmed, agent)
│   ├── tests/test_receivables.py                      <-- 100% Passed Pytest Suite
│   ├── api.py                                         <-- FastAPI REST Service
│   ├── app.py                                         <-- Dedicated Streamlit Web App
│   ├── main_runner.py                                 <-- CLI Demo Pipeline
│   └── requirements.txt
│
├── 02_construction_material_intelligence/             <-- [Recommended Civil Proposal]
│   ├── docs/DETAILED_PROPOSAL.md                      <-- Comprehensive Master Proposal
│   ├── docs/BUSINESS_CASE.md
│   ├── data/sample_batch_tickets.csv
│   ├── src/ (schema, is_codes, predictor, qc)
│   ├── tests/test_materials.py                        <-- 100% Passed Pytest Suite
│   ├── api.py                                         <-- FastAPI REST Service
│   ├── app.py                                         <-- Dedicated Streamlit Web App
│   ├── main_runner.py                                 <-- CLI Demo Pipeline
│   └── requirements.txt
│
├── 03_civil_evidence_claims_intelligence/             <-- [Civil Management Wedge]
│   ├── docs/BUSINESS_CASE.md
│   ├── data/sample_boq_items.csv
│   ├── src/ (schema, evidence graph, detector)
│   ├── tests/test_claims.py                           <-- 100% Passed Pytest Suite
│   ├── api.py                                         <-- FastAPI REST Service
│   ├── app.py                                         <-- Dedicated Streamlit Web App
│   ├── main_runner.py                                 <-- CLI Demo Pipeline
│   └── requirements.txt
│
└── 04_water_resilience_ai/                            <-- [Deep-Tech Long Term]
    ├── docs/BUSINESS_CASE.md
    ├── data/sample_catchment_data.json
    ├── src/ (schema, hydrology, surrogate, suds)
    ├── tests/test_water.py                            <-- 100% Passed Pytest Suite
    ├── api.py                                         <-- FastAPI REST Service
    ├── app.py                                         <-- Dedicated Streamlit Web App
    ├── main_runner.py                                 <-- CLI Demo Pipeline
    └── requirements.txt
```

---

## 🚀 Quick Execution Guide

### **1. Launch Any Standalone Web App**
```powershell
# Project 1: CPSE-MSME Receivables
uv run --with streamlit,pandas,pydantic streamlit run 01_cpse_msme_receivables_agent/app.py

# Project 2: Construction Material Intelligence
uv run --with streamlit,pandas,numpy,scipy,scikit-learn streamlit run 02_construction_material_intelligence/app.py

# Project 3: Civil Evidence & Claims Intelligence
uv run --with streamlit,pandas,networkx streamlit run 03_civil_evidence_claims_intelligence/app.py

# Project 4: WaterResilience AI
uv run --with streamlit,pandas,numpy,scipy streamlit run 04_water_resilience_ai/app.py
```

### **2. Run All Automated Test Suites**
```powershell
uv run --with pytest,pydantic pytest 01_cpse_msme_receivables_agent/tests -p no:cacheprovider; `
uv run --with pytest,pydantic,numpy,scipy,scikit-learn,pandas pytest 02_construction_material_intelligence/tests -p no:cacheprovider; `
uv run --with pytest,pydantic,networkx pytest 03_civil_evidence_claims_intelligence/tests -p no:cacheprovider; `
uv run --with pytest,pydantic,numpy,scipy,pandas pytest 04_water_resilience_ai/tests -p no:cacheprovider
```

### **3. Start Any Project's FastAPI REST Service**
```powershell
# Example: Launch CMI REST API on port 8000
uv run --with fastapi,uvicorn,pydantic,numpy uvicorn 02_construction_material_intelligence.api:app --reload --port 8000
```
Interactive OpenAPI / Swagger docs are available at `http://127.0.0.1:8000/docs`.
