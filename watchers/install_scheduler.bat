@echo off
REM Install Windows Task Scheduler jobs for AI Employee

echo ========================================
echo AI Employee - Task Scheduler Setup
echo ========================================
echo.

REM Get the current directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo Installing Task Scheduler jobs...
echo.

REM Send pending emails every 15 minutes
schtasks /Create /TN "AI Employee - Send Emails" /TR "python \"%SCRIPT_DIR%watchers\scheduler.py\" --action send_emails" /SC MINUTE /MO 15 /F
if %ERRORLEVEL% EQU 0 (
    echo [OK] Task "AI Employee - Send Emails" installed
) else (
    echo [ERROR] Failed to create "AI Employee - Send Emails" task
)

REM Daily report at 8pm
schtasks /Create /TN "AI Employee - Daily Report" /TR "python \"%SCRIPT_DIR%watchers\scheduler.py\" --action daily_report" /SC DAILY /ST 20:00 /F
if %ERRORLEVEL% EQU 0 (
    echo [OK] Task "AI Employee - Daily Report" installed
) else (
    echo [ERROR] Failed to create "AI Employee - Daily Report" task
)

REM Health check every 2 hours
schtasks /Create /TN "AI Employee - Health Check" /TR "python \"%SCRIPT_DIR%watchers\scheduler.py\" --action health_check" /SC HOURLY /MO 2 /F
if %ERRORLEVEL% EQU 0 (
    echo [OK] Task "AI Employee - Health Check" installed
) else (
    echo [ERROR] Failed to create "AI Employee - Health Check" task
)

echo.
echo ========================================
echo Task Scheduler setup complete!
echo ========================================
echo.
echo To view tasks:
echo   schtasks /query /fo LIST /v ^| findstr "AI Employee"
echo.
echo To delete tasks:
echo   schtasks /Delete /TN "AI Employee - Send Emails"
echo   schtasks /Delete /TN "AI Employee - Daily Report"
echo   schtasks /Delete /TN "AI Employee - Health Check"
echo.
pause
