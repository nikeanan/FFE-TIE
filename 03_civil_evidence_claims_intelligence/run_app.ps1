Set-Location -Path $PSScriptRoot
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting Civil Evidence & Claims Intelligence App" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
uv run --with streamlit,pandas,networkx streamlit run app.py
