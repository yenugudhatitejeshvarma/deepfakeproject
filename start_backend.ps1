# PowerShell script to start the Flask backend server
Set-Location $PSScriptRoot
Write-Host "Starting Deepfake Detection Backend API..." -ForegroundColor Cyan
Write-Host ""
& .\venv\Scripts\python.exe backend_api.py

