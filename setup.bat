@echo off
REM Medication Health Reminder - Setup Script (Windows)
REM This script creates a virtual environment and installs all dependencies.

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ================================================================
echo.
echo    Medication Health Reminder - Setup
echo.
echo ================================================================
echo.

REM Check Python version
echo [1/4] Checking Python version...

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+
    echo Download from: https://python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PYTHON_VERSION=%%i
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.version_info.major)"') do set PYTHON_MAJOR=%%i
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.version_info.minor)"') do set PYTHON_MINOR=%%i

if %PYTHON_MAJOR% lss 3 (
    echo [ERROR] Python 3.10+ required. You have Python %PYTHON_VERSION%
    pause
    exit /b 1
)
if %PYTHON_MAJOR% equ 3 if %PYTHON_MINOR% lss 10 (
    echo [ERROR] Python 3.10+ required. You have Python %PYTHON_VERSION%
    pause
    exit /b 1
)

echo [OK] Python %PYTHON_VERSION% detected

REM Create virtual environment
echo [2/4] Creating virtual environment...

if exist "venv" (
    echo [WARNING] Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    echo [OK] Virtual environment created at .\venv
)

REM Install dependencies
echo [3/4] Installing dependencies...

call venv\Scripts\activate.bat

pip install --upgrade pip --quiet
pip install -r requirements.txt

echo [OK] All dependencies installed successfully

REM Completion message
echo [4/4] Setup complete!
echo.
echo ================================================================
echo                    Setup Complete!
echo ================================================================
echo.
echo To run the application:
echo.
echo   Option 1 - Using virtual environment directly:
echo     .\venv\Scripts\python.exe app.py
echo.
echo   Option 2 - Activate virtual environment first:
echo     .\venv\Scripts\activate.bat
echo     python app.py
echo.
echo Quick Start:
echo   1. Run the app
echo   2. Click "Create an Account" to register
echo   3. Sign in and start managing your medications!
echo.
echo Enjoy using Medication Health Reminder!
echo.

pause

