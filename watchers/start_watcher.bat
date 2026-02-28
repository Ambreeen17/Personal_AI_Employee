@echo off
REM File System Watcher Startup Script for Windows

echo ====================================
echo AI Employee - File System Watcher
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

REM Get script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Start the watcher
echo.
echo Starting File System Watcher...
echo Monitoring: ..\AI_Employee_Vault\Inbox
echo Press Ctrl+C to stop
echo.
python file_system_watcher.py

pause
