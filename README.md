# Personal AI Employee - Silver Tier ✅

**Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

## Project Overview

This is a Personal AI Employee (Digital FTE) built using Claude Code and Obsidian. The AI Employee proactively manages personal and business affairs 24/7 by monitoring inputs, processing tasks, and maintaining a dashboard.

## Current Tier: Silver ✅

### Silver Tier Features (Implemented)
- ✅ **All Bronze Tier features**
- ✅ **Gmail Watcher** - Monitor Gmail inbox via Google API
- ✅ **Email Sender MCP** - Send emails via SMTP with approval workflow
- ✅ **Approval Workflow** - Human-in-the-loop for sensitive actions
- ✅ **Task Scheduler** - Automate recurring tasks via cron/Task Scheduler
- ✅ **LinkedIn Poster** - Auto-post content with browser automation
- ✅ **Complete documentation** and setup guides

## Project Structure

```
Personal_AI_Employee/
├── AI_Employee_Vault/          # Obsidian vault (GUI & Memory)
│   ├── Dashboard.md            # Real-time status dashboard
│   ├── Company_Handbook.md     # Rules & procedures
│   ├── Inbox/                  # Raw incoming data
│   ├── Needs_Action/           # Items requiring processing
│   ├── In_Progress/            # Items being worked on
│   ├── Done/                   # Completed items
│   ├── Plans/                  # Multi-step project plans
│   ├── Pending_Approval/       # Items awaiting human review
│   │   ├── Email/              # Email drafts
│   │   ├── LinkedIn/           # LinkedIn post drafts
│   │   └── Sensitive/          # Critical actions
│   ├── Ready_To_Send/          # Approved items ready to execute
│   │   └── Email/
│   ├── Ready_To_Post/          # Approved posts ready to publish
│   │   └── LinkedIn/
│   └── Rejected/               # Items that were not approved
├── watchers/                   # Monitoring scripts
│   ├── file_system_watcher.py  # File system monitor
│   ├── gmail_watcher.py        # Gmail API integration
│   ├── linkedin_poster.py      # LinkedIn auto-poster
│   ├── scheduler.py            # Task scheduler
│   ├── validate_silver_tier.py # Validation script
│   ├── requirements.txt        # Python dependencies
│   ├── schedule.yaml           # Schedule configuration
│   ├── install_scheduler.sh    # Cron job installer
│   ├── install_scheduler.bat   # Task Scheduler installer
│   ├── start_watcher.bat       # Windows startup script
│   └── start_watcher.sh        # Unix startup script
├── mcp_servers/                # MCP servers
│   └── email_sender/
│       ├── email_server.py     # Email MCP server
│       ├── .env.template       # Configuration template
│       └── requirements.txt
├── .claude/
│   └── skills/                  # Agent Skills
│       ├── ai-employee/        # AI Employee skill
│       ├── gmail-watcher/      # Gmail monitoring
│       ├── email-sender/       # Email sending
│       ├── linkedin-poster/    # LinkedIn posting
│       ├── approval-workflow/  # Approval system
│       ├── planning-agent/     # Project planning
│       └── task-scheduler/     # Task scheduling
├── README.md                    # This file
├── SILVER_TIER_IMPLEMENTATION_PLAN.md  # Implementation guide
└── SILVER_TIER_SETUP.md        # Setup instructions
```

## Quick Start

### 1. Install Dependencies

```bash
# Python dependencies (for Watcher)
pip install -r watchers/requirements.txt

# Or use the startup scripts (auto-install)
# Windows:
watchers\start_watcher.bat

# Unix/Linux/macOS:
bash watchers/start_watcher.sh
```

### 2. Start the File System Watcher

The Watcher monitors the `/Inbox` folder and automatically creates action items.

**Windows:**
```bash
cd watchers
start_watcher.bat
```

**Unix/Linux/macOS:**
```bash
cd watchers
chmod +x start_watcher.sh
./start_watcher.sh
```

### 3. Use the AI Employee

With Claude Code, use the AI Employee skill to process tasks:

```
/ai-employee
```

## How It Works

### Architecture

```
┌─────────────────┐
│   File System   │
│    Watcher      │
└────────┬────────┘
         │ detects new files
         ▼
┌─────────────────┐
│  /Inbox folder  │
└────────┬────────┘
         │ creates action file
         ▼
┌─────────────────┐
│ /Needs_Action/  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Claude Code    │
│   (AI Brain)    │
└────────┬────────┘
         │ processes tasks
         ▼
┌─────────────────┐
│   /Done/        │
│   (Archive)     │
└─────────────────┘
```

### Workflow

1. **Input**: Drop a file in `/Inbox` or Watcher detects it
2. **Detect**: Watcher creates an action file in `/Needs_Action/`
3. **Process**: AI Employee reads the item and follows Company Handbook
4. **Complete**: Item moved to `/Done/` with completion notes
5. **Update**: Dashboard.md updated with current status

## Quick Start

### 1. Install Dependencies

```bash
# Python dependencies
pip install -r watchers/requirements.txt
```

### 2. Validate Setup

```bash
# Run validation script
python watchers/validate_silver_tier.py
```

### 3. Configure Components

See [SILVER_TIER_SETUP.md](SILVER_TIER_SETUP.md) for detailed setup:
- Gmail API setup
- SMTP configuration
- Cron/Task Scheduler jobs

### 4. Use the AI Employee

With Claude Code, use the AI Employee skill:

```
/ai-employee
```

## Testing the Silver Tier

### Validation

```bash
# Run validation script
cd watchers
python validate_silver_tier.py
```

### Test Complete Workflow

1. **Gmail Integration** (after OAuth setup)
   ```bash
   python watchers/gmail_watcher.py --auth
   bash watchers/start_gmail_watcher.sh
   ```

2. **Email Sending** (after SMTP config)
   ```bash
   # Create draft in Pending_Approval/Email/
   # Move to Ready_To_Send/Email/
   # Email Sender MCP will send automatically
   ```

3. **LinkedIn Posting**
   ```bash
   python watchers/linkedin_poster.py --check-queue
   ```

4. **Scheduled Tasks** (after cron/Task Scheduler setup)
   ```bash
   # Unix: crontab -l
   # Windows: schtasks /query | findstr "AI Employee"
   ```

## Configuration

### Vault Location
By default, the vault is at: `./AI_Employee_Vault/`

To change, update the path in:
- `watchers/file_system_watcher.py` (VAULT_PATH variable)

### Watcher Settings
Edit `watchers/file_system_watcher.py`:
- `check_interval`: How often to check for new files (default: immediate via watchdog)
- Priority detection based on filename keywords

## Company Handbook Rules

The AI Employee follows rules defined in `Company_Handbook.md`:

| Action | Authority |
|--------|-----------|
| Draft responses | ✅ Autonomous |
| Send emails | ❌ Approval Required |
| Make payments | ❌ Approval Required |
| File organization | ✅ Autonomous |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher not detecting files | Check if Watcher script is running |
| No action files created | Check `watcher.log` for errors |
| Claude can't find vault | Verify VAULT_PATH in watcher script |
| Permission denied | Run with appropriate permissions |

## Silver Tier Features ✅

### Implemented Components
- ✅ **Gmail Watcher** - Monitor Gmail inbox with Google API OAuth
- ✅ **Email Sender MCP** - Send emails via SMTP with approval
- ✅ **Approval Workflow** - Human-in-the-loop for sensitive actions
- ✅ **Task Scheduler** - Automate tasks via cron/Task Scheduler
- ✅ **LinkedIn Poster** - Auto-post content with browser automation
- ✅ **Complete Documentation** - Setup guides and implementation plan

### To Configure (One-Time Setup)

1. **Gmail API Setup**
   - Create project at Google Cloud Console
   - Enable Gmail API
   - Create OAuth credentials
   - Run: `python watchers/gmail_watcher.py --auth`

2. **SMTP Configuration**
   - Copy `mcp_servers/email_sender/.env.template` to `.env`
   - Add SMTP credentials

3. **Scheduler Setup**
   - Unix: Run `watchers/install_scheduler.sh`
   - Windows: Run `watchers\install_scheduler.bat`

4. **LinkedIn Setup**
   - Install Playwright: `pip install playwright && playwright install chromium`
   - Run: `python watchers/linkedin_poster.py --check-queue`

See [SILVER_TIER_SETUP.md](SILVER_TIER_SETUP.md) for details.

## Resources

- **Hackathon Document**: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Company Handbook**: `AI_Employee_Vault/Company_Handbook.md`
- **Dashboard**: `AI_Employee_Vault/Dashboard.md`

## License

This project is part of the Personal AI Employee Hackathon.

---

**Silver Tier Completed**: 2026-02-28
**Version**: 2.0
**Status**: ✅ Implementation Complete, Ready for Configuration
