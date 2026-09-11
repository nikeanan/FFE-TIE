@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting CMI - Construction Material Intelligence App
echo ============================================================
uv run --with streamlit,pandas,numpy,scipy,scikit-learn streamlit run app.py
pause
