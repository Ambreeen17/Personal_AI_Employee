---
name: approval-workflow
description: |
  Human-in-the-loop approval workflow for sensitive actions.
  Ensures no emails, posts, or critical actions are taken without explicit user approval.
  Manages Pending_Approval, Ready_To_Send, Rejected, and Approved folders.
---

# Approval Workflow

Human-in-the-loop system ensuring all sensitive actions require explicit approval before execution.

## Overview

The Approval Workflow manages all actions that require human review and approval:
- Sending emails
- Posting to social media
- Making payments
- Deleting files
- Sharing data externally
- Other sensitive operations

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AI Employee                          │
│                    (Autonomous)                         │
└───────────────────┬─────────────────────────────────────┘
                    │
                    │ Creates Draft
                    ▼
┌─────────────────────────────────────────────────────────┐
│         Pending_Approval/ (Review Required)             │
│  ├── Email/                                             │
│  ├── LinkedIn/                                           │
│  ├── Payments/                                           │
│  └── Sensitive/                                          │
└───────────────────┬─────────────────────────────────────┘
                    │
                    │ Human Review
                    ▼
┌─────────────────────────────────────────────────────────┐
│                   Decision                               │
└───┬──────────────┬──────────────┬────────────────────────┘
    │              │              │
    ▼              ▼              ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ Approve│   │ Reject  │   │  Edit   │
└────┬────┘   └────┬────┘   └────┬────┘
     │             │             │
     ▼             ▼             ▼
┌─────────┐   ┌─────────┐   ┌─────────┐
│ Ready_  │   │Rejected/│   │ Return  │
│ To_Send/│   │         │   │ to      │
└────┬────┘   └─────────┘   │Pending  │
     │                      └─────────┘
     ▼
┌─────────────────────────────────────────────────────────┐
│              Execution (Automated)                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
│  │Email Sender│  │LinkedIn    │  │Payment     │        │
│  │MCP         │  │Poster     │  │Processor   │        │
│  └────────────┘  └────────────┘  └────────────┘        │
└─────────────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│                    Done/ (Archive)                       │
│  └── All actions logged with timestamp and status       │
└─────────────────────────────────────────────────────────┘
```

## Folder Structure

```
AI_Employee_Vault/
├── Pending_Approval/
│   ├── Email/
│   ├── LinkedIn/
│   ├── Payments/
│   └── Sensitive/
├── Ready_To_Send/
│   ├── Email/
│   ├── LinkedIn/
│   └── Scheduled/
├── Ready_To_Post/
│   ├── LinkedIn/
│   └── Social_Media/
├── Rejected/
│   ├── Email/
│   ├── LinkedIn/
│   └── Archived/
└── Approved/
    ├── Email/
    └── Actions/
```

## Approval Process

### 1. Draft Creation (AI)
```markdown
# Pending_Approval/Email/2026-02-28_client_response.md

---
type: email_draft
status: pending_approval
created: 2026-02-28T14:00:00
priority: normal
requires_approval: true
---

# Email: Client Response

[Email content here]

---
⚠️ REQUIRES YOUR APPROVAL BEFORE SENDING
```

### 2. Human Review
```bash
# List pending items
ls AI_Employee_Vault/Pending_Approval/Email/

# Review specific item
cat AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md
```

### 3. Decision

#### Option A: Approve
```bash
# Move to ready queue
mv "AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md" \
   "AI_Employee_Vault/Ready_To_Send/Email/"

# System will automatically send it
```

#### Option B: Reject
```bash
# Move to rejected with reason
mv "AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md" \
   "AI_Employee_Vault/Rejected/Email/"

# Optional: Add rejection note
echo "Rejected: Tone too casual. Please revise." >> \
   "AI_Employee_Vault/Rejected/Email/2026-02-28_client_response.md"
```

#### Option C: Edit
```bash
# Edit the draft
nano "AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md"

# Then approve
mv "AI_Employee_Vault/Pending_Approval/Email/2026-02-28_client_response.md" \
   "AI_Employee_Vault/Ready_To_Send/Email/"
```

## Approval Categories

### 🔴 Critical Approval (Always Required)
- Sending emails
- Posting to social media
- Making payments/transfers
- Deleting files
- Sharing data externally
- Configuration changes

### 🟠 High Priority (Usually Required)
- Replies to clients
- Business announcements
- File operations
- API calls with side effects

### 🟡 Normal (Sometimes Required)
- Internal communications
- File organization
- Task creation
- Plan updates

### 🟢 Low (Rarely Required)
- Logging
- Status updates
- Dashboard updates
- Report generation

## Approval Commands

### Quick Approve
```bash
# Approve all pending emails
/approve-all --category Email

# Approve specific item
/approve --item "2026-02-28_client_response.md"

# Approve with comment
/approve --item "post.md" --note "Approved for 5pm posting"
```

### Quick Reject
```bash
# Reject specific item
/reject --item "email.md" --reason "Inappropriate content"

# Reject all from category
/reject-all --category Payments --reason "Not authorized"
```

### Batch Operations
```bash
# Review all pending
/review-pending

# Approve multiple
/approve --items "item1.md,item2.md,item3.md"

# Batch approve by priority
/approve-all --priority high
```

## Approval Interface

### Command Line
```bash
# Interactive review
/approval-workflow --review

# Shows:
# ┌─────────────────────────────────────────┐
# │ Pending Approval Items: 3               │
# ├─────────────────────────────────────────┤
# │ [1] Email: client_response.md           │
# │     Priority: High                      │
# │     From: AI Employee                   │
# │     Preview: "Thank you for your..."    │
# ├─────────────────────────────────────────┤
# │ [2] LinkedIn: product_launch.md         │
# │     Priority: Normal                    │
# │     Scheduled: 2026-03-01 18:00         │
# ├─────────────────────────────────────────┤
# │ [3] Payment: invoice_123.md             │
# │     Priority: Critical                  │
# │     Amount: $250.00                     │
# └─────────────────────────────────────────┘
#
# Actions: [1] View [2] Approve [3] Reject [4] Edit [5] Skip
# Your choice: _
```

### File-Based
Simply move files between folders:
```bash
# Approve
Pending_Approval/ → Ready_To_Send/

# Reject
Pending_Approval/ → Rejected/

# Edit and approve
Pending_Approval/ → (edit) → Ready_To_Send/
```

## Tracking & Logging

### Approval Log
```markdown
# AI_Employee_Vault/Approval_Log_YYYY-MM.md

## Approval Log - February 2026

| Date | Item | Type | Decision | Reviewer | Notes |
|------|------|------|----------|----------|-------|
| 02-28 | client_response.md | Email | ✅ Approved | User | Sent successfully |
| 02-28 | product_launch.md | LinkedIn | ✅ Approved | User | Scheduled for 6pm |
| 02-28 | promo_post.md | LinkedIn | ❌ Rejected | User | Off-brand content |
| 02-27 | vendor_payment.md | Payment | ⏸️ Hold | User | Awaiting invoice |
```

### Statistics
```bash
# Monthly approval rate
/approval-stats --month 2026-02

# Shows:
# Total Pending: 50
# Approved: 42 (84%)
# Rejected: 6 (12%)
# Pending: 2 (4%)
#
# By Category:
# Email: 35 approved, 3 rejected
# LinkedIn: 5 approved, 2 rejected
# Payments: 2 approved, 1 rejected
```

## Safety Features

### Double-Check for Critical Actions
Before executing critical actions, system asks:
```
⚠️ CRITICAL ACTION REQUIRED

You are about to:
- Send email to: client@company.com
- Subject: Project Update
- Action: SEND

Confirm? [yes/NO]: _
```

### Undo Window
- 30-second undo window for emails
- 1-minute undo for social media posts
- Cancel from Ready_To_Send/ to stop execution

### Approval Notifications
```bash
# Get notified of pending items
# Add to crontab:
*/30 * * * * /path/to/notify-pending.sh

# Sends desktop notification when items need approval
```

## Integration with Skills

### Email Sender
```
Email Sender creates draft
    ↓
Saved to Pending_Approval/Email/
    ↓
You review and approve
    ↓
Moved to Ready_To_Send/Email/
    ↓
Email Sender picks up and sends
    ↓
Logged to Done/
```

### LinkedIn Poster
```
LinkedIn Poster creates draft
    ↓
Saved to Pending_Approval/LinkedIn/
    ↓
You review and approve
    ↓
Moved to Ready_To_Post/LinkedIn/
    ↓
LinkedIn Poster posts at scheduled time
    ↓
Logged to Done/
```

## Best Practices

### For Approvals
1. **Review Promptly** - Don't let items pile up
2. **Be Decisive** - Approve or reject, don't hoard
3. **Provide Feedback** - Note why you rejected
4. **Edit When Needed** - Improve drafts before approving
5. **Track Patterns** - Learn from repeated rejections

### For Drafts
1. **Be Clear** - State what needs approval
2. **Provide Context** - Why is this action needed?
3. **Show Preview** - First few lines of content
4. **Estimate Impact** - What will happen when approved?
5. **Include Alternatives** - Options if rejected

## Troubleshooting

### Items Not Being Approved
- Check Ready_To_Send/ folder
- Verify scheduler is running
- Review approval workflow logs

### Items Stuck in Pending
- Check folder permissions
- Verify file format is correct
- Review system logs for errors

### Accidental Approval
- Move from Ready_To_Send/ back to Pending_Approval/
- Or delete if already sent (may not be undoable)

### Too Many Pending Items
- Set up approval notifications
- Schedule daily review time
- Consider auto-approval rules for low-risk items

---

*For approval workflow design: https://www.workflowtools.com/approval-workflows*
*For human-in-the-loop AI: https://www.anthropic.com/research/human-in-the-loop*
