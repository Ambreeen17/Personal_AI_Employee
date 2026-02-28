---
name: gmail-watcher
description: |
  Gmail Watcher for monitoring Gmail inbox and creating action items.
  Monitors unread emails, extracts content, categorizes by priority,
  and creates action files in Needs_Action folder for processing.
---

# Gmail Watcher

Monitor Gmail inbox and automatically create action items for new emails.

## Overview

The Gmail Watcher connects to your Gmail account via Google API, monitors for new unread messages, and creates action items in the AI Employee vault for processing.

## Prerequisites

### Google Cloud Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download credentials.json

### Initial Authentication
```bash
cd watchers
python gmail_watcher.py --auth
```

This will:
- Open browser for Google authentication
- Save token.json for future use
- Verify Gmail API access

## Configuration

### Environment Variables
```bash
# watchers/.env
GMAIL_CREDENTIALS_PATH=credentials.json
GMAIL_TOKEN_PATH=token.json
GMAIL_CHECK_INTERVAL=120  # seconds
GMAIL_QUERY=is:unread is:inbox  # Gmail search query
```

### Gmail Query Options
```bash
# All unread important emails
is:unread is:important

# Unread from specific sender
is:unread from:newsletter@example.com

# High priority
is:unread is:important OR is:starred

# Work emails
is:unread from:@workplace.com
```

## Usage

### Start Gmail Watcher
```bash
# Windows
watchers\start_gmail_watcher.bat

# Unix/Linux/macOS
bash watchers/start_gmail_watcher.sh
```

### Manual Check
```bash
cd watchers
python gmail_watcher.py --check-once
```

## Action File Format

When a new email is detected, creates:

```markdown
---
type: email
source: gmail_watcher
priority: high/normal/low
status: pending
created: 2026-02-28T14:00:00
message_id: 1234567890abcdef
from: sender@example.com
subject: Email Subject
received: 2026-02-28T14:00:00
---

# New Email: Subject

## Email Details
- **From:** sender@example.com (Sender Name)
- **To:** me@example.com
- **Subject:** Email Subject
- **Date:** 2026-02-28 14:00:00
- **Priority:** High/Normal/Low

## Content Preview
[First 500 characters of email body]

## Full Content
[Complete email body in markdown format]

## Suggested Actions
- [ ] Review email content
- [ ] Categorize and respond
- [ ] Extract action items
- [ ] Update Dashboard

---
*Created by Gmail Watcher at 2026-02-28 14:00:00*
```

## Email Processing Rules

### Priority Detection
| Keyword/Pattern | Priority |
|-----------------|----------|
| "urgent", "asap", "deadline" | 🔴 High |
| "important", "priority" | 🟠 High |
| "fyi", "info", "update" | 🟡 Normal |
| "newsletter", "unsubscribe" | 🟢 Low |

### Categorization
- **Business:** @company.com domains, work-related keywords
- **Personal:** @gmail.com, @yahoo.com personal contacts
- **Finance:** "invoice", "payment", "receipt", "bank"
- **Social:** notifications from social platforms
- **Promotional:** "sale", "offer", "discount"

### Auto-Archive
These are automatically labeled and archived (no action file):
- Weekly newsletters (after 3 unopened)
- Promotional emails
- Already processed messages

## Integration with AI Employee

### Workflow
```
Gmail Inbox
    ↓ (Gmail Watcher detects new email)
Needs_Action/YYYY-MM-DD_gmail_subject.md
    ↓ (AI Employee processes via ai-employee skill)
Done/YYYY-MM-DD_processed_email.md
```

### Processing Steps
1. **Gmail Watcher** detects unread email
2. **Creates action file** in Needs_Action/
3. **AI Employee** reads and categorizes
4. **Drafts response** (autonomous)
5. **Requests approval** for sending (human-in-the-loop)
6. **Moves to Done** after processing

## Troubleshooting

### Authentication Issues
```bash
# Error: "Invalid credentials"
rm watchers/token.json
python watchers/gmail_watcher.py --auth
```

### API Quota Exceeded
- Gmail API quota: 250 quota units/day
- Each message.list() = 1-5 units
- Each message.get() = 5 units
- Solution: Increase check interval or reduce query scope

### No New Emails Detected
- Check Gmail query: `is:unread is:inbox`
- Verify token.json exists and is valid
- Check API permissions in Google Console

## Monitoring

### Watcher Status
```bash
# Check if running
ps aux | grep gmail_watcher

# View logs
tail -f AI_Employee_Vault/gmail_watcher.log

# View recent action files
ls -lt AI_Employee_Vault/Needs_Action/ | grep gmail
```

### Statistics
```bash
# Count processed today
grep "Created by Gmail Watcher" AI_Employee_Vault/Needs_Action/*.md | wc -l

# View breakdown by priority
grep "priority:" AI_Employee_Vault/Needs_Action/*.gmail*.md | sort | uniq -c
```

## Security

### Data Protection
- ✅ Credentials stored locally (credentials.json, token.json)
- ✅ No data sent to external servers
- ✅ Google OAuth 2.0 with required scopes only
- ⚠️ Never commit credentials.json or token.json to git

### Required Scopes
- `https://www.googleapis.com/auth/gmail.readonly` - Read emails
- `https://www.googleapis.com/auth/gmail.modify` - Mark as read

### .gitignore
```
watchers/credentials.json
watchers/token.json
watchers/.env
```

## Best Practices

1. **Start with high-priority filters** (`is:unread is:important`)
2. **Review categorization** before auto-archiving
3. **Use labels** in Gmail for manual organization
4. **Check logs regularly** for errors
5. **Respect rate limits** - don't check too frequently

## Examples

### Monitor Work Emails Only
```bash
# watchers/.env
GMAIL_QUERY=is:unread from:@yourcompany.com
```

### Skip Newsletters
```bash
GMAIL_QUERY=is:unread -from:@newsletter.com -subject:unsubscribe
```

### Monitor Specific Label
```bash
GMAIL_QUERY=is:unread in:Important
```

---

*For Gmail API documentation: https://developers.google.com/gmail/api*
*For OAuth 2.0 setup: https://developers.google.com/identity/protocols/oauth2*
