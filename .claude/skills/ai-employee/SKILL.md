---
name: ai-employee
description: |
  AI Employee skill for managing personal and business affairs through Obsidian vault.
  Includes reading/writing to vault, processing tasks, updating dashboard, and following
  the Company Handbook rules.
---

# AI Employee

Personal AI Employee for managing tasks and workflows through Obsidian vault integration.

## Configuration

The AI Employee vault is located at: `./AI_Employee_Vault/`

### Folder Structure
- `/Inbox` - Raw incoming data (auto-processed by Watchers)
- `/Needs_Action` - Items requiring processing
- `/In_Progress` - Items currently being worked on
- `/Done` - Completed items (archive)
- `/Plans` - Multi-step project plans

## Core Commands

### Read Dashboard
```bash
# View current status
cat AI_Employee_Vault/Dashboard.md
```

### Process Pending Items
```bash
# List items needing action
ls -la AI_Employee_Vault/Needs_Action/
```

### Read Company Handbook
```bash
# Review rules and procedures
cat AI_Employee_Vault/Company_Handbook.md
```

## Workflows

### Task Processing
1. Check `/Needs_Action/` for pending items
2. Read the item details from its markdown file
3. Follow Company Handbook procedures
4. Execute the task or draft response
5. Move completed item to `/Done/` with notes
6. Update Dashboard.md

### Create Task Entry
When processing items, use this template:

```markdown
---
type: processed_task
original_item: [original file name]
processed_by: AI Employee
completed: [timestamp]
---

# Task: [Task Name]

## Summary
[Brief description of what was done]

## Actions Taken
- [ ] Action 1
- [x] Action 2

## Result
[Outcome of the task]

## Next Steps (if any)
[Follow-up actions needed]
```

### Update Dashboard
After processing tasks, update Dashboard.md:
- Update pending count
- Add to recently completed
- Update system status if needed

## Rules from Company Handbook

### Communication Style
- Be polite and professional
- Use clear, concise language
- Ask for permission before sensitive actions
- Admit uncertainty

### Decision Authority
| Action | Authority |
|--------|-----------|
| Draft responses | ✅ Autonomous |
| Send emails | ❌ Approval Required |
| Make payments | ❌ Approval Required |
| File organization | ✅ Autonomous |
| Social media posts | ❌ Approval Required |

### Priority Levels
- 🔴 Critical - Immediate
- 🟠 High - < 1 hour
- 🟡 Normal - < 4 hours
- 🟢 Low - < 24 hours

## File Operations

### Move Item to Done
```bash
mv "AI_Employee_Vault/Needs_Action/item.md" "AI_Employee_Vault/Done/"
```

### Create Plan
```bash
# Create multi-step project plan
cat > "AI_Employee_Vault/Plans/Project_Name.md" << 'EOF'
# Project: [Name]

## Objectives
- [ ] Objective 1
- [ ] Objective 2

## Steps
1. Step one
2. Step two

## Status
Status: In Progress
Updated: [timestamp]
EOF
```

## Examples

### Process Inbox Item
```bash
# 1. List pending items
ls AI_Employee_Vault/Needs_Action/

# 2. Read the item
cat AI_Employee_Vault/Needs_Action/2026-02-28_inbox_example.md

# 3. Process according to handbook
# (Take actions based on item type)

# 4. Move to done when complete
mv "AI_Employee_Vault/Needs_Action/2026-02-28_inbox_example.md" \
   "AI_Employee_Vault/Done/"

# 5. Update dashboard
# (Edit Dashboard.md with updated counts)
```

### Create Action Item
```bash
cat > "AI_Employee_Vault/Needs_Action/$(date +%Y-%m-%d)_manual_task.md" << 'EOF'
---
type: manual_task
priority: Normal
status: pending
created: $(date -Iseconds)
---

# Task Title

## Description
[Task description]

## Steps
- [ ] Step 1
- [ ] Step 2
EOF
```

## Monitoring

### Check Watcher Status
```bash
# Check if watcher is running
ps aux | grep file_system_watcher
# or on Windows:
tasklist | findstr python

# Check watcher log
tail -f AI_Employee_Vault/watcher.log
```

### List Active Items
```bash
# Count pending items
ls AI_Employee_Vault/Needs_Action/ | wc -l

# Show recent items
ls -lt AI_Employee_Vault/Needs_Action/ | head -10
```

## Best Practices

1. **Always read Company_Handbook.md** before processing sensitive items
2. **Update Dashboard.md** after completing tasks
3. **Move items to /Done/** when complete (don't delete)
4. **Use the correct priority** when creating new items
5. **Ask for approval** before sending messages or making changes
6. **Log all actions** in task completion files

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No items in Needs_Action | Check if Watcher is running |
| Can't find files | Verify VAULT_PATH in watcher script |
| Dashboard not updating | Manually edit Dashboard.md |
| Task not processing | Check Company Handbook for procedures |

## Integration with Watchers

The File System Watcher automatically monitors `/Inbox` and creates action items:
1. Drop a file in `AI_Employee_Vault/Inbox/`
2. Watcher detects it within 1 second
3. Action file created in `/Needs_Action/`
4. AI Employee processes the item
5. Item moved to `/Done/`

## Skills Available

- **Reading Vault**: Access all markdown files
- **Writing Tasks**: Create and update task files
- **Dashboard Updates**: Modify Dashboard.md
- **Task Processing**: Follow Company Handbook procedures
- **File Organization**: Move and organize vault files

---

*For more details, see AI_Employee_Vault/Company_Handbook.md*
