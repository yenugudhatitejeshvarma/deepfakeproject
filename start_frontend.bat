@echo off
REM Start the React frontend development server
cd /d "%~dp0\frontend\deepfake"
echo Starting Frontend Development Server...
echo.
call npm run dev
pause

