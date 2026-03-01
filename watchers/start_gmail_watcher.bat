@echo off
REM Gmail Watcher Startup Script for Windows

echo ====================================
echo AI Employee - Gmail Watcher
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

REM Check if credentials exist
if not exist "credentials.json" (
    echo.
    echo ========================================
    echo Gmail Setup Required
    echo ========================================
    echo.
    echo Please follow these steps to set up Gmail API:
    echo.
    echo 1. Go to Google Cloud Console: https://console.cloud.google.com/
    echo 2. Create a new project or select existing
    echo 3. Enable Gmail API
    echo 4. Create OAuth 2.0 credentials (Desktop app)
    echo 5. Download credentials.json and place in this directory
    echo.
    echo See: .claude/skills/gmail-watcher/SKILL.md for detailed instructions
    echo.
    pause
)

REM Start the watcher
echo.
echo Starting Gmail Watcher...
echo Monitoring for unread emails...
echo Press Ctrl+C to stop
echo.
python gmail_watcher.py

pause
