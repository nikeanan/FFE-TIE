# Project 04: WaterResilience AI

## Problem Statement
Municipal corporations, smart cities, and infrastructure engineering consultants struggle to model urban flood risk rapidly. Traditional 1D/2D hydrodynamic engines (EPA-SWMM, MIKE Urban, TUFLOW) take hours to run high-resolution simulations, making real-time emergency response and iterative master-drainage planning painfully slow.

## Architecture
- **Hydrological Ingestion**: Ingests IDF (Intensity-Duration-Frequency) rainfall curves, DEM/topography, land-use imperviousness, and stormwater conduit networks.
- **Physics-Informed ML Surrogate**: Approximates 1D/2D Saint-Venant hydraulic equations to predict peak water levels and pipe surcharge in milliseconds rather than hours.
- **Intervention Evaluator**: Compares Sponge City / SUDS interventions (retention ponds, bioswales, conduit upsizing) for maximum flood volume mitigation per rupee spent.

## Quick Start
```bash
pip install -r requirements.txt
python main_runner.py
```
