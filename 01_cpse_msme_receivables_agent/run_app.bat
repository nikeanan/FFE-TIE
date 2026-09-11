@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting RECEIVX - CPSE-MSME Receivables Intelligence App
echo ============================================================
uv run --with streamlit,pandas,pydantic streamlit run app.py
pause
