@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting Civil Evidence & Claims Intelligence App
echo ============================================================
uv run --with streamlit,pandas,networkx streamlit run app.py
pause
