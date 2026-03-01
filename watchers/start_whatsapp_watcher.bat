@echo off
REM WhatsApp Watcher Startup Script (Windows)
REM This script starts the WhatsApp Watcher to monitor for urgent messages

echo Starting WhatsApp Watcher...
echo.

REM Change to the watchers directory
cd /d "%~dp0"

REM Run the WhatsApp Watcher
python whatsapp_watcher.py ../AI_Employee_Vault

REM Pause if there's an error
if errorlevel 1 (
    echo.
    echo Error occurred. Press any key to exit...
    pause
)
