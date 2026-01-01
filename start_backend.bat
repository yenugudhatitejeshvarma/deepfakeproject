@echo off
REM Start the Flask backend server
cd /d "%~dp0"
echo Starting Deepfake Detection Backend API...
echo.
call venv\Scripts\activate.bat
python backend_api.py
pause

