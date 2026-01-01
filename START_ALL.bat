@echo off
echo ========================================
echo Starting Deepfake Detection Web App
echo ========================================
echo.
echo This will start both backend and frontend
echo.
echo Press Ctrl+C to stop both servers
echo.
pause

start "Backend Server" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python backend_api.py"
timeout /t 3 /nobreak >nul
start "Frontend Server" cmd /k "cd /d %~dp0\frontend\deepfake && npm run dev"

echo.
echo Backend and Frontend are starting in separate windows
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo.
pause

