# ⚡ RECEIVX — CPSE–MSME Receivables Intelligence Platform
> **Production-Grade Autonomous AI Layer: From Invoice "Created" to "Cash in Bank"**

---

## 1. System Vision & Competitive Advantage

MSMEs supplying Central Public Sector Enterprises (CPSEs) face severe working-capital locks due to delayed acceptance, documentation mismatches, and opaque verification procedures. While statutory protections exist (**MSMED Act Section 15 & 16**, **Income Tax Act Section 43B(h)**, and **TReDS mandates**), manual chasing keeps average collection periods at 60–90+ days.

RECEIVX wins on **5 axes competitors cannot match**:

| Axis | Our Standard | Market Standard |
| :--- | :--- | :--- |
| **Entry Point** | **Pre-acceptance** (gatekeeper checks before submission) | Post-acceptance |
| **Interface** | **WhatsApp-first**, vernacular (English & Hindi), voice-enabled | Web dashboards only |
| **Rails** | **All 4 TReDS** (RXIL, M1x, Invoicemart, C2FO) + GeM + Samadhaan | Single platform |
| **Intelligence** | **Buyer-behaviour ML graph** (predictive P10/P50/P90 settlement) | Static reminders |
| **Autonomy** | **Agents that act** (validate, track, file, escalate, bid) | Tools that show |

---

## 2. The Six Autonomous AI Agents

1. **Agent 1: VALIDATOR (Pre-Submission Gatekeeper)**
   - 5-Node Pipeline: `Extract` ➔ `3-Way Match` ➔ `Compliance` ➔ `Buyer Rules (The Moat)` ➔ `Score & Verdict`.
   - Checks PO lines, physical Store GRN, 64-char IRN hash, HSN rates, and Udyam number.
   - Mines learned rejection rules per CPSE unit (e.g., *NTPC Dadri requires quantity to match GRN; BHEL Trichy requires 6-digit vendor code in header*).
   - Generates instant proactive WhatsApp alerts with one-click auto-remediation (boosting acceptance probability from 41% ➔ 94%).

2. **Agent 2: TRACKER (Acceptance Velocity Engine)**
   - Adaptive follow-up cadence based on dynamic median thresholds (T1: 60%, T2: 100%, T3: 150% of CPSE average acceptance days).
   - Dispatches polite soft nudges, statutory reminders citing MSMED §15 and IT §43B(h), and escalates overdue invoices to Agent 3.
   - **Inbound Email Parser (IMAP):** Reads buyer replies, auto-extracts rejection reasons, and feeds them back into the Buyer Graph (*"The agents teach each other"*).

3. **Agent 3: ESCALATOR (Rights-Enforcement Engine)**
   - 5-Step Escalation Ladder:
     1. Senior Contact Polite Inquiry
     2. Certified MSMED Section 16 Interest Memo (3x RBI Bank Rate, compounded monthly)
     3. Formal Statutory Demand Notice
     4. Auto-Compiled MSME Samadhaan (MSEFC) Petition Dossier
     5. Section 43B(h) CFO & Auditor Tax Disallowance Notice
   - **Strict Human-in-the-Loop Gate:** Escalation steps > 2 require explicit MSME WhatsApp authorization to protect buyer relationships.

4. **Agent 4: FINANCIER (TReDS Multi-Exchange & Liquidity Optimizer)**
   - Aggregates live reverse factoring bids across RXIL, M1xchange, Invoicemart, and C2FO.
   - Compares factoring discount costs against the supplier's Bank Cash Credit / OD facility rate (12.5% APR).
   - Calculates net working capital savings and executes 1-click bid acceptance with T+1 bank credit.

5. **Agent 5: FORECASTER (Buyer Behaviour ML & Cash-Flow Simulator)**
   - Predicts settlement dates with confidence intervals: **P10 (Optimistic)**, **P50 (Expected)**, **P90 (Conservative)**.
   - Accounts for fiscal year-end budget rushes (Q4) vs. post-budget allocation lags (Q1).
   - Simulates 12-week forward cash balances under Direct CPSE Collections vs. TReDS Early Factoring.

6. **Agent 6: ADVISOR (Daily Next-Best-Action Engine)**
   - Daily morning briefing for the MSME business owner.
   - Prioritizes actions across four urgency tiers: Immediate Action, Financing Opportunity, Routine Cadence, and Informational.

---

## 3. High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                                │
│  WhatsApp Bot (Bilingual Hindi/English • Voice & Text Simulation)  │
│  React Web App / Streamlit Executive Console (7 Comprehensive Views)│
│  CPSE Buyer Portal (Compliance & Verification Dashboards)          │
└──────────────────────────┬─────────────────────────────────────────┘
                           │ HTTPS / WSS
┌──────────────────────────▼─────────────────────────────────────────┐
│                     REST API GATEWAY (FastAPI)                     │
│    Auth │ Rate Limiting │ OpenAPI Spec │ Agent Webhook Handlers    │
└──────────────────────────┬─────────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────────┐
│                   AI AGENT ORCHESTRATION LAYER                     │
│                                                                    │
│   Agent 1: VALIDATOR    — 4-way match, GST/IRN, learned moat rules │
│   Agent 2: TRACKER      — acceptance velocity, adaptive cadence    │
│   Agent 3: ESCALATOR    — MSMED Sec 16 interest, 43B(h), Samadhaan │
│   Agent 4: FINANCIER    — 4 TReDS rails, rate shopping, OD spread  │
│   Agent 5: FORECASTER   — P10/P50/P90 prediction, cash-flow sim    │
│   Agent 6: ADVISOR      — daily next-best-action agenda per MSME   │
└──────────────────────────┬─────────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────────┐
│                   INTEGRATION LAYER (ADAPTERS)                     │
│  GSTN e-Invoice IRP │ GeM Milestones │ RXIL │ M1xchange │ Invoicemart│
│  MSME Samadhaan (MSEFC) │ WhatsApp Business API │ IMAP Email Parser│
└──────────────────────────┬─────────────────────────────────────────┘
                           │
┌──────────────────────────▼─────────────────────────────────────────┐
│                      DATA LAYER                                    │
│  Transactional Models │ Event Sourced Audit Log │ Buyer Moat Graph │
└────────────────────────────────────────────────────────────────────┘
```

---

## 4. Quick Start & Execution

### Installation
```bash
pip install -r requirements.txt
```

### Run Multi-Agent Terminal Pipeline Demo
```bash
python main_runner.py
```

### Launch Interactive Executive Web Console
```bash
streamlit run app.py
```

### Launch REST API Service
```bash
uvicorn api:app --reload --port 8000
```
Interactive Swagger API documentation will be available at: `http://localhost:8000/docs`.

### Run Automated Tests
```bash
pytest tests/ -v
```
