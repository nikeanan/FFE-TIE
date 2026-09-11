Set-Location -Path $PSScriptRoot
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Starting RECEIVX - CPSE-MSME Receivables Intelligence App" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
uv run --with streamlit,pandas,pydantic streamlit run app.py
