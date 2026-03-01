# Silver Tier Implementation Plan

**Status:** Planning Phase
**Created:** 2026-02-28
**Estimated Time:** 20-30 hours (per hackathon guidelines)

---

## Context

The Bronze Tier is complete with:
- File System Watcher operational
- Basic vault structure (Inbox → Needs_Action → Done)
- Core AI Employee skill for task processing
- Dashboard and Company Handbook

Silver Tier requires adding:
1. **Gmail Watcher** - Monitor Gmail inbox via API
2. **Email Sender MCP** - Send emails via SMTP
3. **Approval Workflow** - Human-in-the-loop for sensitive actions
4. **Task Scheduler** - Automate recurring tasks
5. **LinkedIn Poster** - Auto-post content (uses existing Playwright skill)
6. **Planning Agent** - Create structured project plans

---

## Implementation Strategy

### Phase Order & Dependencies

```
Phase 1: Foundation (2-3 hours)
├── Create Approval Workflow folders
└── Update Company Handbook

Phase 2: Gmail Integration (8-10 hours)
├── Set up Google Cloud Console
├── Create gmail_watcher.py
├── Implement OAuth authentication
└── Test Gmail monitoring

Phase 3: Email Sending (6-8 hours)
├── Create email_sender MCP server
├── Implement SMTP integration
└── Test sending with approval workflow

Phase 4: Scheduling (4-5 hours)
├── Create schedule.yaml configuration
├── Set up cron jobs (Unix) or Task Scheduler (Windows)
└── Test scheduled execution

Phase 5: LinkedIn Integration (3-4 hours)
├── Create linkedin_poster.py
├── Implement posting with Playwright
└── Test with approval workflow

Phase 6: Planning & Testing (2-3 hours)
├── Implement planning_agent utilities
├── End-to-end workflow testing
└── Documentation updates
```

---

## Critical Files to Modify/Create

### Existing Files to Update

1. **`AI_Employee_Vault/Company_Handbook.md`**
   - Add Silver Tier procedures
   - Add email handling protocols
   - Add approval workflow documentation

2. **`AI_Employee_Vault/Dashboard.md`**
   - Add Silver Tier status indicators
   - Add Gmail Watcher status
   - Add approval queue counts

3. **`watchers/requirements.txt`**
   - Add Gmail API dependencies
   - Add SMTP library dependencies

### New Files to Create

#### Phase 1: Foundation
```
AI_Employee_Vault/
├── Pending_Approval/
│   ├── Email/
│   ├── LinkedIn/
│   └── Sensitive/
├── Ready_To_Send/
│   └── Email/
├── Ready_To_Post/
│   └── LinkedIn/
├── Rejected/
│   ├── Email/
│   └── LinkedIn/
└── Approved/
    └── Email/
```

#### Phase 2: Gmail Watcher
```
watchers/
├── gmail_watcher.py (NEW)
├── credentials.json (not committed)
└── token.json (not committed)
```

**Key Implementation:**
- Use `google-auth-oauthlib` and `google-api-python-client`
- Follow existing `file_system_watcher.py` pattern
- Create action files in `Needs_Action/`
- State persistence in `gmail_watcher_state.json`

#### Phase 3: Email Sender MCP
```
mcp_servers/
└── email_sender/
    ├── email_server.py (NEW)
    └── requirements.txt (NEW)
```

**Key Implementation:**
- Use `aiosmtplib` for async SMTP
- Implement MCP server with tools:
  - `send_email` - Send via SMTP
  - `draft_email` - Create draft for approval
- Check `Ready_To_Send/Email/` folder
- Log sent emails to `Done/`

#### Phase 4: Task Scheduler
```
watchers/
├── scheduler.py (NEW)
└── schedule.yaml (NEW)
```

**Key Implementation:**
- YAML-based schedule configuration
- Python scheduler that reads schedule
- Actions: send_emails, post_linkedin, daily_report, health_check
- Support both cron (Unix) and Task Scheduler (Windows)

#### Phase 5: LinkedIn Poster
```
watchers/
└── linkedin_poster.py (NEW)
```

**Key Implementation:**
- Use existing `browsing-with-playwright` skill
- Check `Ready_To_Post/LinkedIn/` folder
- Login and post content
- Track engagement in `Accounting/LinkedIn_Metrics.md`

#### Phase 6: Planning Agent
```
watchers/
└── planning_agent.py (NEW)
```

**Key Implementation:**
- Create Plan.md files in `Plans/`
- Multi-phase project breakdown
- Progress tracking and updates
- Claude reasoning loop integration

---

## Implementation Details

### 1. Gmail Watcher (`watchers/gmail_watcher.py`)

**Architecture:**
```python
class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path, credentials_path):
        # Authenticate with Google OAuth
        # Load processed message IDs
        # Set up Gmail API service

    def check_for_updates(self):
        # Query Gmail API for unread messages
        # Filter by configured query
        # Return new messages not in processed_ids

    def create_action_file(self, message):
        # Get message details (headers, body)
        # Determine priority from subject/content
        # Create markdown action file in Needs_Action/
        # Add to processed_ids
        # Save state
```

**Dependencies:**
- `google-api-python-client`
- `google-auth-oauthlib`
- `google-auth-httplib2`

**Configuration:**
```yaml
# watchers/gmail_config.yaml
gmail:
  query: "is:unread is:inbox"
  check_interval: 120  # seconds
  priorities:
    high: ["urgent", "asap", "deadline"]
    normal: ["important", "priority"]
    low: ["fyi", "newsletter"]
```

### 2. Email Sender MCP (`mcp_servers/email_sender/email_server.py`)

**Architecture:**
```python
class EmailSenderMCPServer:
    def __init__(self, smtp_config):
        # Load SMTP credentials from .env
        # Set up MCP server on port 8809

    async def send_email(self, to, subject, body, attachments):
        # Compose email
        # Send via SMTP
        # Log to Done/
        # Return message_id

    async def check_queue(self):
        # Monitor Ready_To_Send/Email/
        # Send all approved emails
        # Move to Done/ after sending
```

**MCP Tools:**
- `send_email` - Send immediately
- `draft_email` - Create draft for approval
- `check_queue` - Process approved emails

### 3. Task Scheduler (`watchers/scheduler.py`)

**Architecture:**
```python
class TaskScheduler:
    def __init__(self, schedule_file):
        # Load schedule.yaml
        # Parse scheduled actions

    def run_action(self, action):
        # Execute scheduled action
        # Log results

    def main_loop(self):
        # Check schedule every minute
        # Execute due actions
```

**Schedule Configuration:**
```yaml
# watchers/schedule.yaml
schedule:
  - name: "Send pending emails"
    frequency: "*/15 * * * *"
    action: "send_emails"
    enabled: true

  - name: "Post to LinkedIn"
    frequency: "0 18 * * 1,3,5"
    action: "post_linkedin"
    enabled: true

  - name: "Daily report"
    frequency: "0 20 * * *"
    action: "daily_report"
    enabled: true
```

### 4. Approval Workflow Integration

**Folder Structure Already Defined** in skills, just needs to be created:
```bash
mkdir -p AI_Employee_Vault/{Pending_Approval,Ready_To_Send,Ready_To_Post,Rejected}/
mkdir -p AI_Employee_Vault/Pending_Approval/{Email,LinkedIn,Sensitive}
mkdir -p AI_Employee_Vault/Ready_To_Send/Email
mkdir -p AI_Employee_Vault/Ready_To_Post/LinkedIn
```

**Workflow:**
1. AI creates draft in `Pending_Approval/`
2. Human reviews (can edit, approve, or reject)
3. Approved → `Ready_To_Send/` or `Ready_To_Post/`
4. Scheduler picks up and executes
5. Results logged to `Done/`

---

## Verification Plan

### Phase 1: Foundation
- [ ] Verify folder structure created
- [ ] Test approval workflow with sample file
- [ ] Update Dashboard with new status indicators

### Phase 2: Gmail Integration
- [ ] Test Google OAuth authentication flow
- [ ] Verify Gmail API access
- [ ] Send test email to self
- [ ] Confirm action file created in Needs_Action
- [ ] Verify priority detection works

### Phase 3: Email Sending
- [ ] Start MCP server on port 8809
- [ ] Test draft_email tool
- [ ] Create email in Ready_To_Send/
- [ ] Verify email sent via SMTP
- [ ] Check log in Done/
- [ ] Test with attachment

### Phase 4: Scheduling
- [ ] Create schedule.yaml
- [ ] Set up cron job (Unix) or Task Scheduler (Windows)
- [ ] Test scheduled action runs
- [ ] Verify logs created
- [ ] Check Dashboard updates

### Phase 5: LinkedIn Posting
- [ ] Create sample LinkedIn post
- [ ] Post via approval workflow
- [ ] Verify post appears on LinkedIn
- [ ] Check engagement tracking

### Phase 6: End-to-End
- [ ] Test complete workflow:
  - Email arrives → Gmail Watcher detects → Draft response → Approve → Send → Log
- [ ] Test LinkedIn workflow:
  - Create post → Approve → Schedule → Post → Track metrics
- [ ] Verify all components working together
- [ ] Update documentation

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Gmail API quota exceeded | Medium | High | Implement rate limiting, cache results |
| OAuth token expires | Low | Medium | Auto-refresh token, error handling |
| SMTP authentication fails | Low | High | Clear credentials, retry with backoff |
| LinkedIn blocks automation | Medium | Medium | Use realistic posting patterns, rate limiting |
| Cron jobs don't run | Low | High | Add logging, health check monitoring |
| Approval workflow bottleneck | Low | Medium | Batch operations, notifications |

---

## Success Criteria

### Minimum Viable Silver Tier (MVP)
- ✅ Gmail Watcher monitoring inbox
- ✅ Email Sender MCP operational
- ✅ Approval workflow functional
- ✅ Basic scheduling configured
- ✅ End-to-end email workflow tested

### Complete Silver Tier
- ✅ All MVP criteria
- ✅ LinkedIn Poster working
- ✅ Planning Agent operational
- ✅ Daily reports generating
- ✅ All workflows documented
- ✅ Dashboard showing Silver Tier status

---

## Time Estimate

| Phase | Tasks | Estimated Hours |
|-------|-------|-----------------|
| Phase 1: Foundation | Folders, handbook update | 2-3 |
| Phase 2: Gmail Watcher | Google API, OAuth, testing | 8-10 |
| Phase 3: Email Sender MCP | SMTP server, approval workflow | 6-8 |
| Phase 4: Scheduling | Cron/Task Scheduler setup | 4-5 |
| Phase 5: LinkedIn Poster | Browser automation | 3-4 |
| Phase 6: Planning & Testing | Planning agent, E2E tests | 2-3 |
| **Total** | | **25-33 hours** |

This aligns with hackathon guidelines of 20-30 hours for Silver Tier.
