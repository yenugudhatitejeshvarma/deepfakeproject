# PowerShell script to run the deepfake detector model
# This script automatically uses the virtual environment's Python
Set-Location $PSScriptRoot

# Check if venv exists
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please make sure you're in the project directory and venv is set up." -ForegroundColor Yellow
    exit 1
}

# Run the model with venv Python
& .\venv\Scripts\python.exe run_model.py $args

