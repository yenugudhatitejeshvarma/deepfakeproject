# PowerShell script to start both backend and frontend
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Deepfake Detection Web App" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$backendScript = "Start-Process powershell -ArgumentList '-NoExit', '-Command', \"cd '$PSScriptRoot'; .\venv\Scripts\python.exe backend_api.py\""
$frontendScript = "Start-Process powershell -ArgumentList '-NoExit', '-Command', \"cd '$PSScriptRoot\frontend\deepfake'; npm run dev\""

Write-Host "Starting Backend Server..." -ForegroundColor Yellow
Invoke-Expression $backendScript

Write-Host "Waiting 3 seconds for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Invoke-Expression $frontendScript

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Both servers are starting in separate windows" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit this window (servers will keep running)..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

