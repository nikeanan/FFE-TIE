@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting WaterResilience AI App
echo ============================================================
uv run --with streamlit,pandas,numpy,scipy streamlit run app.py
pause
