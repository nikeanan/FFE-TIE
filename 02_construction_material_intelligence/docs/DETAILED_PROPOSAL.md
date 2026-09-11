# Construction Material Intelligence (CMI)
## *A Physics-Informed Decision-Support System for Concrete Quality, Cost and Material Optimization*

**Document Version:** 3.0 — Defensible FFE TIE Proposal  
**Domain:** Civil Engineering × Artificial Intelligence × Construction Technology  
**Status:** Prototype / Research-to-Market Stage  

---

## 1. Executive Summary & Problem
Ready-Mix Concrete (RMC) and batching operations must maintain structural compressive strength, workability, and standards compliance (IS 10262:2019, IS 456:2000, IS 4926:2003) amid severe raw material variability (quarry changes, aggregate moisture swings). 

Because compressive strength is traditionally verified weeks later (28-day water-cured cube crush tests), batching plants routinely over-design mixes by adding safety cement buffers. 

**CMI provides a real-time decision-support layer** that uses existing batching PLC logs and laboratory records to predict strength at batching ($t=0$), detect moisture/scale anomalies, and identify validated opportunities for material optimization without compromising structural safety.

---

## 2. Core Technical Architecture

```
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                         EXISTING PLANT DATA STREAMS                         │
 │ • Batching PLC Logs (Weights of Cement, SCMs, Aggregates, Water, Admixture) │
 │ • Laboratory Registers (Slump, 7-day & 28-day Cube Compressive Strengths)   │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        │
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │                  PHYSICS-INFORMED MACHINE LEARNING ENGINE                   │
 │                                                                             │
 │   [Layer 1: Engineering Prior]                                              │
 │   • Abram's / Bolomey's water-binder phenomenological equations             │
 │   • IS 10262:2019 (f'ck = fck + 1.65s) & IS 456 Table 5 Durability Bounds   │
 │                                                                             │
 │   [Layer 2: Plant-Specific Residual ML]                                     │
 │   • Learns local quarry shape, mineralogy, and cement brand reactivities    │
 │                                                                             │
 │   [Layer 3: Uncertainty Quantification]                                     │
 │   • Outputs: Predicted Strength + Prediction Intervals + Confidence Score   │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
 ┌──────────────────────────────────────┐ ┌──────────────────────────────────┐
 │    REAL-TIME BATCH QC ALERTS (t=0)   │ │  HUMAN-IN-THE-LOOP QC DASHBOARD  │
 │ • IS 4926 scale drift detection      │ │ • Plant-specific calibration     │
 │ • Uncompensated moisture alerts      │ │ • Candidate mix optimization     │
 │   before dispatch                    │ │   (Reviewed by QC Engineer)      │
 └──────────────────────────────────────┘ └──────────────────────────────────┘
```

---

## 3. Human-in-the-Loop Safety Governance
* **Decision Support Only:** CMI does not replace laboratory testing, certified QA/QC engineers, or statutory compliance procedures.
* **Auditability:** Retains raw source data, displays prediction uncertainty bounds, and logs all engineer approvals.

---

## 4. Sensitivity Scenario (Economic Impact)
* **Monthly Plant Volume:** 7,500 m³
* **Validated Cementitious Optimization:** 12 kg/m³
* **Monthly Material Saved:** 90,000 kg (1,800 Bags)
* **Illustrative Value (at ₹360/bag):** ₹6.48 Lakhs/month
*(Actual savings depend on local material costs, grade, durability limits, and plant variability).*

---

## 5. 4-Phase Pilot Validation Protocol
1. **Phase 1 — Data Audit (Weeks 1–4):** Ingest 3–6 months historical batch and lab registers; evaluate data quality.
2. **Phase 2 — Offline Benchmark (Weeks 5–8):** Train physics-informed vs baseline ML models; evaluate MAE, RMSE, and prediction interval coverage.
3. **Phase 3 — Shadow Deployment (Weeks 9–14):** Run CMI in read-only mode alongside live plant operations.
4. **Phase 4 — Controlled Optimization (Weeks 15–20):** Supervised test of candidate mix optimizations on non-critical grades.

---

## 6. Commercial Model (Indicative Hypotheses)
* **Pilot Engagement:** ₹25,000 – ₹75,000 flat per pilot.
* **Single-Plant SaaS:** ₹15,000 – ₹30,000 / month / plant.
* **Enterprise Multi-Plant Cockpit:** ₹1,00,000 – ₹3,00,000 / month.
