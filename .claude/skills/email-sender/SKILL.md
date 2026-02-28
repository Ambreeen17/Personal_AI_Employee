---
name: email-sender
description: |
  Email Sender MCP server for sending emails via SMTP.
  Part of human-in-the-loop workflow - emails require approval before sending.
  Integrates with Gmail, Outlook, and other email providers.
---

# Email Sender MCP Server

Send emails through SMTP with human-in-the-loop approval workflow.

## Overview

The Email Sender is an MCP (Model Context Protocol) server that enables sending emails. It integrates with Claude Code and requires human approval for all outgoing messages, ensuring no emails are sent without your confirmation.

## Architecture

```
Draft Email (AI)
    ↓
Needs Approval (You)
    ↓
Ready to Send (Approved)
    ↓
Email Sender MCP
    ↓
Sent ✅
    ↓
Logged (Done/)
```

## Prerequisites

### SMTP Credentials

For Gmail:
1. Enable 2-Factor Authentication
2. Generate App Password: https://myaccount.google.com/apppasswords
3. Save App Password (16 characters)

For Outlook/Office 365:
1. Go to Account Security
2. Create app password
3. Save credentials

For other providers:
- SMTP server address
- SMTP port (usually 587 for TLS, 465 for SSL)
- Username and password

## Configuration

### Environment Variables
```bash
# watchers/.env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=your_app_password
SMTP_FROM=your@email.com
SMTP_FROM_NAME="Your Name"
EMAIL_SENDING_ENABLED=true
```

### MCP Server Setup
```bash
# Install dependencies
pip install aiosmtplib mcp

# Start server
cd mcp_servers/email_sender
python email_server.py --port 8809
```

## MCP Server Tools

### send_email
Send an email via SMTP.

**Parameters:**
```json
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "body": "Email body in markdown",
  "cc": ["cc@example.com"],
  "bcc": ["bcc@example.com"],
  "attachments": ["/path/to/file.pdf"]
}
```

**Response:**
```json
{
  "success": true,
  "message_id": "abc123",
  "timestamp": "2026-02-28T14:00:00"
}
```

### draft_email
Create email draft for approval (doesn't send).

**Parameters:**
```json
{
  "to": "recipient@example.com",
  "subject": "Draft Subject",
  "body": "Draft content",
  "save_to": "AI_Employee_Vault/Pending_Approval/Email/"
}
```

## Usage

### 1. Create Email Draft
```bash
# Via AI Employee
/ai-employee
"I received an email from client@company.com asking about project status. Draft a response."

# Creates:
AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md
```

### 2. Draft Format
```markdown
---
type: email_draft
status: pending_approval
from: your@email.com
to: client@company.com
subject: Re: Project Status Update
created: 2026-02-28T14:00:00
priority: normal
---

# Email Draft: Project Status Update

## To
client@company.com (Client Name)

## Subject
Re: Project Status Update

## Body
Dear Client,

Thank you for your inquiry about our project status.

I'm pleased to report that we're making excellent progress:

**Completed:**
- ✅ File System Watcher deployed
- ✅ Task automation operational
- ✅ Integration testing complete

**In Progress:**
- 🔄 Gmail integration setup
- 🔄 LinkedIn poster configuration

**Next Steps:**
- Complete Silver Tier implementation
- Begin testing and validation

Please let me know if you have any questions.

Best regards,
Your Name

## Attachments
None

---
*Drafted by AI Employee*
*Awaits your approval before sending*
```

### 3. Approval Workflow
```bash
# Review draft
cat AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md

# Edit if needed
nano AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md

# Approve for sending
mv AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md \
   AI_Employee_Vault/Ready_To_Send/Email/

# Reject (keep for reference)
mv AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md \
   AI_Employee_Vault/Rejected/Email/
```

### 4. Send Approved Email
```bash
# Via MCP server (automatic when in Ready_To_Send/)
# Or manual trigger:
/send-email --file "Ready_To_Send/Email/2026-02-28_client_response.md"
```

## Email Templates

### Business Response
```markdown
Dear {{name}},

Thank you for your {{inquiry_type}}.

{{response_content}}

Please let me know if you need any additional information.

Best regards,
{{your_name}}
{{your_title}}
{{company}}
```

### Project Update
```markdown
Hi {{name}},

Here's your weekly project update:

**Completed This Week:**
- {{completed_items}}

**Planned Next Week:**
- {{planned_items}}

** blockers:**
- {{blockers}}

**Questions?** Please reach out.

Best,
{{your_name}}
```

### Follow-up
```markdown
Hi {{name}},

Just following up on our {{previous_conversation}}.

{{follow_up_content}}

Looking forward to hearing from you.

Best regards,
{{your_name}}
```

## Human-in-the-Loop Safety

### Approval Required For:
- ✅ All outgoing emails
- ✅ Emails with attachments
- ✅ Emails to new recipients
- ✅ Mass emails (multiple recipients)

### Auto-Send Only When:
- Explicitly pre-approved templates
- Recurring scheduled emails (once approved)
- Internal notifications (same domain)

### Approval Options
```bash
# Approve as-is
/approve-email "draft_id"

# Approve with edits
/edit-email "draft_id" --replace "old text" "new text"
/approve-email "draft_id"

# Reject
/reject-email "draft_id" --reason "Not appropriate"

# Request changes
/request-changes "draft_id" --comment "Add more details"
```

## Integration with Gmail Watcher

### Complete Email Workflow
```
1. Gmail Watcher detects new email
    ↓
2. Creates action file in Needs_Action/
    ↓
3. AI Employee analyzes and drafts response
    ↓
4. Draft saved to Pending_Approval/Email/
    ↓
5. You review and approve
    ↓
6. Moved to Ready_To_Send/Email/
    ↓
7. Email Sender MCP sends it
    ↓
8. Logged to Done/ with sent status
    ↓
9. Original email marked as read in Gmail
```

## Logging & Audit

### Sent Email Log
```markdown
# AI_Employee_Vault/Accounting/Email_Log_YYYY-MM.md

## Sent Emails - February 2026

| Date | To | Subject | Status | Message ID |
|------|-------|---------|--------|------------|
| 02-28 | client@company.com | Project Update | ✅ Sent | abc123 |
| 02-28 | team@company.com | Meeting Notes | ✅ Sent | def456 |
| 02-27 | vendor@xyz.com | Invoice Inquiry | ✅ Sent | ghi789 |
```

### Complete Record
```markdown
# Done/2026-02-28_sent_email_client_response.md

---
type: sent_email
original_draft: 2026-02-28_client_response.md
sent: 2026-02-28T14:05:00
message_id: abc123def456
status: sent
---

# Email Sent: Project Status Update

## Details
- **To:** client@company.com
- **From:** your@email.com
- **Subject:** Re: Project Status Update
- **Sent:** 2026-02-28 14:05:00
- **Message ID:** abc123def456

## Content
[Full email content that was sent]

## Approval Log
- Drafted: 2026-02-28 14:00:00
- Approved: 2026-02-28 14:04:00
- Sent: 2026-02-28 14:05:00
- Approved by: User

---
*Sent via Email Sender MCP*
*SMTP: smtp.gmail.com:587*
```

## Troubleshooting

### Authentication Failed
```bash
# Check credentials
cat watchers/.env | grep SMTP

# For Gmail: regenerate app password
# https://myaccount.google.com/apppasswords

# Update and restart server
```

### Email Not Sending
```bash
# Check if MCP server is running
ps aux | grep email_server

# Check server logs
tail -50 mcp_servers/email_sender/server.log

# Verify network connectivity
telnet smtp.gmail.com 587
```

### Attachment Issues
```bash
# Verify file exists
ls -la /path/to/attachment.pdf

# Check file size (< 25MB for most providers)
du -h /path/to/attachment.pdf

# Verify file permissions
chmod 644 /path/to/attachment.pdf
```

## Security

### Credentials Protection
- ✅ SMTP password in `.env` (never committed)
- ✅ No passwords in email drafts
- ✅ Encryption in transit (TLS)
- ✅ No credential logging

### Data Privacy
- ✅ Email content stored locally only
- ✅ No third-party email services
- ✅ Human approval required
- ✅ Complete audit trail

### Rate Limiting
- Gmail: 500 emails/day (free account)
- Outlook: 10,000 emails/day
- Implement backoff for bounces
- Queue for rate limit handling

## Best Practices

1. **Always Review Drafts** - Even AI-generated content
2. **Test Recipient** - Send test email first
3. **Attachments** - Keep under 10MB when possible
4. **Subject Lines** - Clear and descriptive
5. **Professional Tone** - Follow Company Handbook
6. **Proofread** - Check for typos before approval
7. **CC/BCC** - Use appropriately
8. **Response Time** - Reply within 24 hours

---

*For SMTP configuration: https://support.google.com/mail/answer/7104828*
*For Python email: https://docs.python.org/3/library/smtplib.html*
