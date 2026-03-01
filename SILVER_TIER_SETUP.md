# Silver Tier Setup Guide

**Last Updated:** 2026-02-28
**Status:** Implementation Complete - Configuration Required

---

## 🎯 Overview

All Silver Tier scripts have been created and are ready for configuration. This guide walks you through setting up each component.

---

## 📋 Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Bronze Tier complete
- [ ] Google account (for Gmail)
- [ ] Email account with SMTP access
- [ ] LinkedIn account (for posting)

---

## 1️⃣ Gmail Watcher Setup

### Step 1: Google Cloud Console

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API:
   - Search for "Gmail API"
   - Click "Enable"

### Step 2: Create OAuth 2.0 Credentials

1. Go to **Credentials** → **Create Credentials**
2. Choose **OAuth client ID**
3. Application type: **Desktop app**
4. Name: "AI Employee Gmail Watcher"
5. Click **Create**
6. Download the credentials JSON file

### Step 3: Configure Credentials

```bash
# Move credentials to watchers folder
mv ~/Downloads/client_secret_*.json watchers/credentials.json
```

### Step 4: Test Gmail Watcher

```bash
cd watchers
python gmail_watcher.py --auth
```

This will:
- Open your browser
- Request OAuth permission
- Save token.json for future use

### Step 5: Run Gmail Watcher

```bash
# Unix/Linux/macOS
bash watchers/start_gmail_watcher.sh

# Windows
watchers\start_gmail_watcher.bat
```

---

## 2️⃣ Email Sender MCP Setup

### Step 1: Generate App Password (Gmail)

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not enabled)
3. Go to **App Passwords**
4. Select **Mail** → **Other (Custom name)**
5. Name: "AI Employee Email Sender"
6. Click **Generate**
7. Copy the 16-character password

### Step 2: Configure Environment

```bash
# Copy template
cd mcp_servers/email_sender
cp .env.template .env
```

### Step 3: Edit .env File

```bash
# Edit .env and add your credentials
# SMTP_SERVER=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USERNAME=your@email.com
# SMTP_PASSWORD=your_16_char_app_password
# SMTP_FROM=your@email.com
# SMTP_FROM_NAME=Your Name
```

### Step 4: Install Dependencies & Test

```bash
cd mcp_servers/email_sender
pip install -r requirements.txt

# Test email sending
python email_server.py
# (Will check Ready_To_Send/Email/ folder)
```

---

## 3️⃣ Task Scheduler Setup

### Unix/Linux/macOS (Cron)

```bash
# Edit crontab
crontab -e

# Add these lines:
# Send emails every 15 minutes
*/15 * * * * cd /path/to/Personal_AI_Employee && python watchers/scheduler.py --action send_emails

# Daily report at 8pm
0 20 * * * cd /path/to/Personal_AI_Employee && python watchers/scheduler.py --action daily_report

# Health check every 2 hours
0 */2 * * * cd /path/to/Personal_AI_Employee && python watchers/scheduler.py --action health_check
```

### Windows (Task Scheduler)

1. Open **Task Scheduler**
2. Create **Basic Task**:
   - Name: "AI Employee - Send Emails"
   - Trigger: Daily, repeat every 15 minutes
   - Action: Start a program
     - Program: `python`
     - Arguments: `watchers\scheduler.py --action send_emails`
     - Start in: `C:\Users\User\Documents\GitHub\Personal_AI_Employee`

3. Create additional tasks for:
   - Daily Report (8pm daily)
   - Health Check (every 2 hours)

### Test Scheduler

```bash
cd watchers
python scheduler.py --list
python scheduler.py --action daily_report
```

---

## 4️⃣ LinkedIn Poster Setup

### Step 1: Install Playwright Browsers

```bash
cd watchers
pip install playwright
playwright install chromium
```

### Step 2: Test LinkedIn Poster

```bash
# List pending posts
python linkedin_poster.py --list

# Check queue and post
python linkedin_poster.py --check-queue
```

### Note on LinkedIn Posting

The LinkedIn Poster will:
1. Open a browser window
2. Navigate to LinkedIn
3. Wait for you to log in (first time only)
4. Post your content
5. Take a screenshot for verification
6. Keep browser open for 30 seconds

---

## 5️⃣ Approval Workflow Usage

### Creating Email Drafts

```bash
# AI Employee creates drafts in:
AI_Employee_Vault/Pending_Approval/Email/

# You review and either:
# - Approve: Move to Ready_To_Send/Email/
# - Reject: Move to Rejected/Email/
# - Edit: Modify and approve
```

### Approving Emails

```bash
# Review draft
cat AI_Employee_Vault/Pending_Approval/Email/2026-02-28_draft.md

# Approve
mv AI_Employee_Vault/Pending_Approval/Email/2026-02-28_draft.md \
   AI_Employee_Vault/Ready_To_Send/Email/

# Scheduler will pick up and send automatically
```

---

## 6️⃣ Testing the Complete Workflow

### Test 1: File System → Done

```bash
# Create test file
echo "Test task" > AI_Employee_Vault/Inbox/test.txt

# Check if action file created in Needs_Action
ls AI_Employee_Vault/Needs_Action/
```

### Test 2: Email Draft → Approved → Sent

1. Create email draft manually in `Pending_Approval/Email/`
2. Move to `Ready_To_Send/Email/`
3. Run: `python mcp_servers/email_sender/email_server.py`
4. Check if email sent

### Test 3: Daily Report Generation

```bash
python watchers/scheduler.py --action daily_report

# Check if report created
ls AI_Employee_Vault/Accounting/Daily_Report_*.md
```

---

## 🔧 Troubleshooting

### Gmail Watcher Issues

**Problem:** "Invalid credentials"
- **Solution:** Delete `token.json` and run `--auth` again

**Problem:** "API quota exceeded"
- **Solution:** Increase check interval in script

### Email Sender Issues

**Problem:** "Authentication failed"
- **Solution:** Verify SMTP password in `.env`

**Problem:** "Email not sending"
- **Solution:** Check if files in `Ready_To_Send/Email/`

### LinkedIn Poster Issues

**Problem:** "Could not find text editor"
- **Solution:** LinkedIn UI may have changed, check selector

**Problem:** "Login required"
- **Solution:** Log in manually within 30-second window

---

## ✅ Verification Checklist

- [ ] Gmail Watcher authenticates successfully
- [ ] Action files created in Needs_Action/ for new emails
- [ ] Email Sender MCP can send test email
- [ ] Scheduler executes scheduled actions
- [ ] LinkedIn Poster can access LinkedIn
- [ ] Approval workflow folders working
- [ ] Dashboard shows Silver Tier progress
- [ ] Daily reports generating
- [ ] Complete workflow tested end-to-end

---

## 🎉 Silver Tier Complete!

Once all components are configured and tested, your AI Employee will:

✅ Monitor Gmail inbox automatically
✅ Draft email responses for approval
✅ Send approved emails via SMTP
✅ Post to LinkedIn with approval
✅ Generate daily reports
✅ Perform health checks
✅ Maintain comprehensive logs

Your Personal AI Employee is now a **Silver Tier Digital FTE!** 🚀
