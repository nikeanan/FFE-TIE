# Project 02: Construction Material Intelligence

## Problem Statement
Ready-Mix Concrete (RMC) and construction companies produce voluminous batching and lab testing data, but records are fragmented across batching PLC outputs, Excel sheets, and laboratory registers. This leads to over-design (excess cement buffer costs), undetected aggregate moisture fluctuations, and delayed 7-day / 28-day compressive strength failure warnings.

## Architecture
- **Data Ingestion & Cleaning**: Ingests batch weights (cement, fly ash, ggbs, coarse/fine aggregate, water, admixtures) and ambient conditions.
- **Indian Standards Compliance (IS 10262:2019 & IS 456:2000)**: Target mean strength calculation ($f'_{ck} = f_{ck} + 1.65 s$), minimum cement content, max water-binder ratio constraints.
- **Predictive Strength Model**: Hybrid physics-empirical (Abrams/Bolomey Law) + ML regression for early 7-day and 28-day compressive strength forecasting.
- **Real-Time QC Anomaly Engine**: Detects batch-scale variances (free moisture errors, admixture overdosing, batching scale drift).

## Quick Start
```bash
pip install -r requirements.txt
python main_runner.py
```
