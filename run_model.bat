@echo off
REM Run the deepfake detector model using the virtual environment
cd /d "%~dp0"

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please make sure you're in the project directory and venv is set up.
    pause
    exit /b 1
)

REM Run using venv Python directly (no need to activate)
venv\Scripts\python.exe run_model.py %*

if errorlevel 1 (
    echo.
    echo Error occurred. Make sure you're using the correct Python from venv.
    pause
)

