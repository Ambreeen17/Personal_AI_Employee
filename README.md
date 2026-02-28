# Personal AI Employee - Bronze Tier

**Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.

## Project Overview

This is a Personal AI Employee (Digital FTE) built using Claude Code and Obsidian. The AI Employee proactively manages personal and business affairs 24/7 by monitoring inputs, processing tasks, and maintaining a dashboard.

## Current Tier: Bronze ✅

### Bronze Tier Features (Completed)
- ✅ Obsidian vault with Dashboard.md and Company_Handbook.md
- ✅ File system Watcher (monitors /Inbox folder)
- ✅ Basic folder structure: /Inbox, /Needs_Action, /Done, /Plans, /In_Progress
- ✅ Agent Skills for AI functionality
- ✅ Claude Code integration for reading/writing to vault

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
│   └── watcher.log             # Watcher activity log
├── watchers/                   # Monitoring scripts
│   ├── file_system_watcher.py  # File system monitor
│   ├── requirements.txt        # Python dependencies
│   ├── start_watcher.bat       # Windows startup script
│   └── start_watcher.sh        # Unix startup script
└── .claude/
    └── skills/
        ├── ai-employee/        # AI Employee skill
        └── browsing-with-playwright/  # Browser automation
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

## Testing the Bronze Tier

### Test 1: File System Watcher

1. Start the Watcher using the startup script
2. Create a test file in `AI_Employee_Vault/Inbox/`:
   ```bash
   echo "Test task" > AI_Employee_Vault/Inbox/test.txt
   ```
3. Check `AI_Employee_Vault/Needs_Action/` for a new action file
4. Verify the action file contains the test content

### Test 2: AI Employee Processing

1. Open Claude Code
2. Use the AI Employee skill to process pending items
3. Verify items are moved to `/Done/`
4. Check Dashboard.md for updates

### Test 3: Dashboard Integration

1. Read `AI_Employee_Vault/Dashboard.md`
2. Verify system status shows "Online"
3. Check that pending tasks are reflected

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

## Next Steps: Silver Tier

To upgrade to Silver Tier, add:
1. Gmail Watcher (email monitoring)
2. Email draft responses
3. MCP server for sending emails
4. Human-in-the-loop approval workflow
5. Social media integration (LinkedIn)
6. Scheduling via cron or Task Scheduler

## Resources

- **Hackathon Document**: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`
- **Company Handbook**: `AI_Employee_Vault/Company_Handbook.md`
- **Dashboard**: `AI_Employee_Vault/Dashboard.md`

## License

This project is part of the Personal AI Employee Hackathon.

---

**Bronze Tier Completed**: 2026-02-28
**Version**: 1.0
