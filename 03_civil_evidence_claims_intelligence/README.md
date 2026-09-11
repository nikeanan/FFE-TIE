# Project 03: Civil Engineering Evidence & Claims Intelligence

## Problem Statement
Large civil infrastructure projects suffer from fragmented documentation—engineering drawings, Bill of Quantities (BOQ), Measurement Books (MB), Request for Inspection (RFI) logs, site progress photos, and formal contractor-client letters. This causes delayed RA (Running Account) bill certifications, missed variation/extra-item claims, and protracted dispute arbitrations.

## Architecture
- **Engineering Evidence Graph**: Connects heterogeneous artifacts into an RDF/property graph (BOQ Item $\leftrightarrow$ Structural Component $\leftrightarrow$ Measurement Sheet $\leftrightarrow$ Site Inspection Photo $\leftrightarrow$ Email/Letter).
- **BOQ & Quantity Discrepancy Detector**: Automatically flags deviation limits (>10% or >25% variation clauses under CPWD/FIDIC contracts).
- **Claim & Dispute Dossier Generator**: Assembles audit-proof evidence dossiers with cited drawing revisions and certified measurement proofs.

## Quick Start
```bash
pip install -r requirements.txt
python main_runner.py
```
