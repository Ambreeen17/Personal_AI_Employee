---
name: task-scheduler
description: |
  Task Scheduler for running AI Employee tasks on schedule via cron or Task Scheduler.
  Automates periodic tasks like sending reports, posting to social media, and system maintenance.
  Supports Windows Task Scheduler and Unix cron jobs.
---

# Task Scheduler

Schedule and automate recurring AI Employee tasks using cron (Unix/Linux/macOS) or Task Scheduler (Windows).

## Overview

The Task Scheduler enables periodic execution of AI Employee tasks:
- Daily reports and summaries
- Scheduled social media posts
- Email sending at optimal times
- System maintenance and cleanup
- Data backups and audits
- Watcher health checks

## Architecture

```
Scheduler (cron/Task Scheduler)
    │
    ├──[Trigger]──> Check Ready_To_Send/Email/
    │              └──> Email Sender MCP sends emails
    │
    ├──[Trigger]──> Check Ready_To_Post/LinkedIn/
    │              └──> LinkedIn Poster posts
    │
    ├──[Trigger]──> Generate Daily Report
    │              └──> Creates report in Accounting/
    │
    ├──[Trigger]──> System Health Check
    │              └──> Updates Dashboard status
    │
    └──[Trigger]──> Cleanup Old Logs
                   └──> Archives logs > 30 days
```

## Configuration

### Schedule Definition
```yaml
# watchers/schedule.yaml
schedule:
  # Email tasks
  - name: "Send pending emails"
    frequency: "*/15 * * * *"  # Every 15 minutes
    command: "python watchers/scheduler.py --action send_emails"
    enabled: true

  - name: "Process new emails"
    frequency: "*/30 * * * *"  # Every 30 minutes
    command: "python watchers/scheduler.py --action process_emails"
    enabled: true

  # Social media
  - name: "Post to LinkedIn"
    frequency: "0 18 * * 1,3,5"  # 6pm Mon, Wed, Fri
    command: "python watchers/scheduler.py --action post_linkedin"
    enabled: true

  # Reports
  - name: "Daily summary"
    frequency: "0 20 * * *"  # 8pm daily
    command: "python watchers/scheduler.py --action daily_report"
    enabled: true

  - name: "Weekly audit"
    frequency: "0 9 * * 1"  # 9am Monday
    command: "python watchers/scheduler.py --action weekly_audit"
    enabled: true

  # Maintenance
  - name: "Health check"
    frequency: "0 */2 * * *"  # Every 2 hours
    command: "python watchers/scheduler.py --action health_check"
    enabled: true

  - name: "Cleanup logs"
    frequency: "0 3 * * 0"  # 3am Sunday
    command: "python watchers/scheduler.py --action cleanup_logs"
    enabled: true
```

## Setup

### Unix/Linux/macOS (cron)

#### Install Cron Jobs
```bash
# Open crontab
crontab -e

# Add AI Employee schedule
# m h  dom mon dow   command

# Email sending (every 15 minutes)
*/15 * * * * cd /path/to/Personal_AI_Employee && python watchers/scheduler.py --action send_emails

# LinkedIn posting (6pm Mon, Wed, Fri)
0 18 * * 1,3,5 cd /path/to/Personal_AI_Employee && python watchers/scheduler.py --action post_linkedin

# Daily report (8pm daily)
0 20 * * * cd /path/to/Personal_AI_Employee && python watchers/scheduler.py --action daily_report

# Health check (every 2 hours)
0 */2 * * * cd /path/to/Personal_AI_Employee && python watchers/scheduler.py --action health_check

# Log cleanup (3am Sunday)
0 3 * * 0 cd /path/to/Personal_AI_Employee && python watchers/scheduler.py --action cleanup_logs
```

#### Verify Cron Jobs
```bash
# List current cron jobs
crontab -l

# Check cron logs
grep CRON /var/log/syslog | tail -20
```

### Windows (Task Scheduler)

#### Create Task
```powershell
# Open Task Scheduler
taskschd.msc

# Create Basic Task:
# 1. Name: "AI Employee - Send Emails"
# 2. Trigger: Daily, repeat every 15 minutes
# 3. Action: Start a program
#    Program: python
#    Arguments: watchers\scheduler.py --action send_emails
#    Start in: C:\Users\User\Documents\GitHub\Personal_AI_Employee
```

#### Import Tasks Script
```batch
# watchers/install_windows_tasks.bat
@echo off
echo Installing AI Employee scheduled tasks...

schtasks /Create /TN "AI Employee - Send Emails" /TR "python watchers\scheduler.py --action send_emails" /SC MINUTE /MO 15 /F
schtasks /Create /TN "AI Employee - LinkedIn Post" /TR "python watchers\scheduler.py --action post_linkedin" /SC WEEKLY /D MON,WED,FRI /T 18:00 /F
schtasks /Create /TN "AI Employee - Daily Report" /TR "python watchers\scheduler.py --action daily_report" /SC DAILY /T 20:00 /F
schtasks /Create /TN "AI Employee - Health Check" /TR "python watchers\scheduler.py --action health_check" /SC HOURLY /MO 2 /F

echo Tasks installed successfully!
```

## Scheduled Actions

### 1. Send Pending Emails
```python
# Runs every 15 minutes
# Checks Ready_To_Send/Email/
# Sends via Email Sender MCP
# Logs results to Done/
```

### 2. Post to LinkedIn
```python
# Runs at scheduled times (e.g., 6pm Mon/Wed/Fri)
# Checks Ready_To_Post/LinkedIn/
# Posts via LinkedIn Poster
# Tracks engagement metrics
```

### 3. Process New Emails
```python
# Runs every 30 minutes
# Checks for new action files in Needs_Action/
# Processes according to Company Handbook
# Updates Dashboard
```

### 4. Daily Report
```python
# Runs at 8pm daily
# Generates summary of day's activities
# Saves to Accounting/Daily_Reports/
```

#### Daily Report Format
```markdown
# AI Employee Daily Report - 2026-02-28

## Summary
- Tasks Processed: 5
- Emails Sent: 2
- LinkedIn Posts: 1
- Errors: 0

## Tasks Completed
- ✅ Processed test_task.md
- ✅ Archived duplicate test file
- ✅ Acknowledged greeting
- ✅ Updated Dashboard
- ✅ Created daily report

## Pending Items
- 0 items in Needs_Action
- 2 emails awaiting approval
- 1 LinkedIn post scheduled

## System Status
- Vault: 🟢 Online
- Watchers: 🟢 Running
- Pending Approvals: 2

## Metrics
- Uptime: 24 hours
- CPU Usage: 2%
- Memory: 150MB
- Disk Space: 45GB free

---
*Generated: 2026-02-28 20:00:00*
```

### 5. Weekly Audit
```python
# Runs Monday 9am
# Reviews week's activities
# Generates CEO Briefing
# Identifies improvements
```

#### Weekly Audit Format
```markdown
# CEO Briefing - Week of 2026-02-22

## Business Overview
- Revenue: $X (Y% vs last week)
- New Clients: N
- Tasks Completed: 25
- Client Satisfaction: 98%

## Key Achievements
- ✅ Bronze Tier complete
- ✅ Gmail integration deployed
- ✅ LinkedIn auto-posting operational

## Challenges
- ⚠️ 2 emails bounced (invalid addresses)
- ⚠️ LinkedIn engagement lower than expected

## Opportunities
- Expand to Silver Tier features
- Add WhatsApp integration
- Improve content quality

## Financial Summary
- Income: $X
- Expenses: $Y
- Profit: $Z

## Action Items
- [ ] Fix email bounce issue
- [ ] Improve LinkedIn content strategy
- [ ] Schedule Silver Tier planning

---
*Generated: 2026-02-24 09:00:00*
```

### 6. Health Check
```python
# Runs every 2 hours
# Checks if watchers are running
# Verifies folder structure
# Tests connectivity
# Updates Dashboard status
```

### 7. Cleanup Logs
```python
# Runs 3am Sunday
# Archives logs older than 30 days
# Compresses large files
# Removes temporary files
```

## Manual Trigger

### Run Scheduled Task Now
```bash
# Unix/Linux/macOS
python watchers/scheduler.py --action send_emails

# Windows
python watchers\scheduler.py --action send_emails

# Run all scheduled tasks
python watchers/scheduler.py --action all
```

### Test Schedule
```bash
# Dry run (shows what would execute)
python watchers/scheduler.py --dry-run

# Show next scheduled runs
python watchers/scheduler.py --next-runs

# Validate schedule configuration
python watchers/scheduler.py --validate
```

## Monitoring

### Check Scheduler Status
```bash
# Unix/Linux/macOS
# Verify cron is running
systemctl status cron  # Linux
launchctl list | grep cron  # macOS

# Check last execution
grep "scheduler.py" /var/log/syslog | tail -10

# Windows
# View scheduled tasks
schtasks /query /fo LIST /v

# Check last run result
schtasks /query /TN "AI Employee - Send Emails" /FO LIST
```

### Scheduler Dashboard
```markdown
# Dashboard shows:

## Scheduler Status
| Task | Frequency | Last Run | Next Run | Status |
|------|-----------|----------|----------|--------|
| Send Emails | */15 * * * * | 14:45 | 15:00 | 🟢 Active |
| LinkedIn Post | 0 18 * * 1,3,5 | 17:00 | 18:00 | 🟢 Scheduled |
| Daily Report | 0 20 * * * | 20:00 | Tomorrow 20:00 | 🟢 Scheduled |
| Health Check | 0 */2 * * * | 14:00 | 16:00 | 🟢 Active |
```

## Logging

### Scheduler Logs
```bash
# watchers/scheduler.log
2026-02-28 14:00:00 - INFO - Starting scheduled action: send_emails
2026-02-28 14:00:01 - INFO - Found 2 emails in Ready_To_Send/
2026-02-28 14:00:05 - INFO - Sent email: client_response.md
2026-02-28 14:00:08 - INFO - Sent email: team_update.md
2026-02-28 14:00:09 - INFO - Completed action: send_emails
```

### Execution Log
```markdown
# AI_Employee_Vault/Scheduler_Log_YYYY-MM.md

## Scheduler Execution Log - February 2026

| Date | Task | Started | Completed | Status | Notes |
|------|------|---------|-----------|--------|-------|
| 02-28 | Send Emails | 14:00:00 | 14:00:09 | ✅ Success | 2 emails sent |
| 02-28 | LinkedIn Post | 18:00:00 | 18:00:15 | ✅ Success | Posted successfully |
| 02-28 | Daily Report | 20:00:00 | 20:00:05 | ✅ Success | Report generated |
| 02-28 | Health Check | 22:00:00 | 22:00:02 | ✅ Success | All systems normal |
```

## Best Practices

### Schedule Design
1. **Stagger Tasks** - Don't run everything at once
2. **Off-Peak Hours** - Heavy tasks at night/early morning
3. **Business Hours** - User-facing tasks during work day
4. **Frequency Balance** - Often enough but not wasteful
5. **Time Zones** - Consider recipient's time zone

### Error Handling
1. **Retry Logic** - Failed tasks retry after delay
2. **Alerts** - Notify on repeated failures
3. **Logs** - Detailed error logging
4. **Recovery** - Auto-recover when possible
5. **Manual Override** - Easy to disable problematic tasks

### Resource Management
1. **CPU Limits** - Don't overload system
2. **Memory** - Monitor usage
3. **Disk I/O** - Batch operations
4. **Network** - Respect rate limits
5. **Cleanup** - Regular maintenance

## Troubleshooting

### Tasks Not Running
```bash
# Check cron is running
systemctl status cron  # Linux
launchctl list | grep cron  # macOS

# Verify crontab
crontab -l

# Check script permissions
ls -la watchers/scheduler.py

# Manual test
python watchers/scheduler.py --action health_check
```

### Tasks Failing
```bash
# Check error logs
tail -50 watchers/scheduler.log

# Test specific action
python watchers/scheduler.py --action send_emails --verbose

# Verify dependencies
pip install -r watchers/requirements.txt
```

### Wrong Schedule
```bash
# Verify cron syntax
# Use: https://crontab.guru/

# Check system time
date

# View timezone
timedatectl  # Linux
date +%Z     # macOS
```

## Advanced Features

### Conditional Scheduling
```yaml
# Only run if working day
condition: "is_weekday()"

# Only run if pending items exist
condition: "count('Ready_To_Send/Email') > 0"

# Only run if system healthy
condition: "health_check() == 'ok'"
```

### Task Dependencies
```yaml
# Run after another task completes
depends_on: "daily_report"

# Run only if previous succeeded
run_if: "previous_task.status == 'success'"
```

### Dynamic Scheduling
```python
# Calculate next run time based on workload
if pending_items > threshold:
    schedule_next_run(sooner=True)
```

---

*For cron setup: https://crontab.guru/*
*For Windows Task Scheduler: https://www.microsoft.com/documentation/windows-task-scheduler*
