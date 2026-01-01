# PowerShell script to start the React frontend
Set-Location "$PSScriptRoot\frontend\deepfake"
Write-Host "Starting Frontend Development Server..." -ForegroundColor Cyan
Write-Host ""
npm run dev

