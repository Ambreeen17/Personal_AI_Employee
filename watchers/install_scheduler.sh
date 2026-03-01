#!/bin/bash
# Install Cron Jobs for AI Employee Task Scheduler

echo "========================================"
echo "AI Employee - Task Scheduler Setup"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if crontab is installed
if ! command -v crontab &> /dev/null; then
    echo "Error: crontab not found"
    exit 1
fi

echo "Installing cron jobs..."
echo ""

# Create temporary cron file
CRON_FILE="/tmp/ai_employee_cron"

# Add cron jobs
cat > "$CRON_FILE" << EOF
# AI Employee Task Scheduler Jobs

# Send pending emails every 15 minutes
*/15 * * * * cd "$SCRIPT_DIR" && python scheduler.py --action send_emails

# Daily report at 8pm
0 20 * * * cd "$SCRIPT_DIR" && python scheduler.py --action daily_report

# Health check every 2 hours
0 */2 * * * cd "$SCRIPT_DIR" && python scheduler.py --action health_check

# Log cleanup (Sunday 3am)
0 3 * * 0 cd "$SCRIPT_DIR" && python scheduler.py --action cleanup_logs
EOF

# Install crontab
crontab "$CRON_FILE" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[OK] Cron jobs installed successfully"
    echo ""
    echo "Current crontab:"
    crontab -l | grep "AI Employee"
else
    echo "[ERROR] Failed to install cron jobs"
    exit 1
fi

rm "$CRON_FILE"

echo ""
echo "========================================"
echo "Setup complete!"
echo "========================================"
echo ""
echo "To view cron jobs:"
echo "  crontab -l"
echo ""
echo "To edit cron jobs:"
echo "  crontab -e"
echo ""
echo "To remove jobs:"
echo "  crontab -r"
echo ""
