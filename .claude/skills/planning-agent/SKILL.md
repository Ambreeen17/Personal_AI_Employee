---
name: planning-agent
description: |
  Planning Agent for creating structured Plan.md files for complex multi-step tasks.
  Breaks down projects into manageable steps, tracks progress, and updates plans.
  Implements Claude reasoning loop for iterative planning.
---

# Planning Agent

Create structured project plans with step-by-step breakdown and progress tracking.

## Overview

The Planning Agent creates comprehensive Plan.md files for complex multi-step projects. It implements a reasoning loop that:
1. Analyzes project requirements
2. Breaks down into manageable tasks
3. Identifies dependencies
4. Creates timeline estimates
5. Tracks progress and updates plans

## When to Use

### Complex Projects
- 🎯 Multi-step initiatives
- 🎯 Cross-domain tasks
- 🎯 Projects > 4 hours
- 🎯 Requires coordination

### Examples
- "Implement Gmail integration"
- "Set up LinkedIn auto-posting"
- "Create accounting system"
- "Launch marketing campaign"

## Plan Structure

### Plan.md Template
```markdown
---
type: project_plan
project: Project Name
status: planning | in_progress | completed | on_hold
created: 2026-02-28T14:00:00
updated: 2026-02-28T14:00:00
priority: high | normal | low
estimated_hours: 20
actual_hours: 0
completion_percentage: 0
---

# Project: Project Name

## Objectives
- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## Success Criteria
- ✅ Criteria 1
- ✅ Criteria 2
- ✅ Criteria 3

## Timeline
- **Start Date:** 2026-02-28
- **Target Complete:** 2026-03-15
- **Estimated Hours:** 20

## Phase 1: Planning
### Tasks
- [ ] Task 1.1 (2h) - @assigned_to
- [ ] Task 1.2 (1h) - @assigned_to
- [x] Task 1.3 (1h) - Completed 2026-02-28

**Status:** In Progress (1/3 complete)
**Hours Spent:** 2h / 4h estimated

## Phase 2: Implementation
### Tasks
- [ ] Task 2.1 (4h) - Blocked by Task 1.2
- [ ] Task 2.2 (3h)
- [ ] Task 2.3 (2h)

**Status:** Not Started
**Dependencies:** Phase 1 complete

## Phase 3: Testing
### Tasks
- [ ] Task 3.1 (2h)
- [ ] Task 3.2 (1h)
- [ ] Task 3.3 (2h)

**Status:** Not Started
**Dependencies:** Phase 2 complete

## Phase 4: Deployment
### Tasks
- [ ] Task 4.1 (1h)
- [ ] Task 4.2 (1h)
- [ ] Task 4.3 (1h)

**Status:** Not Started
**Dependencies:** Phase 3 complete

## Resources Needed
- Resource 1
- Resource 2
- Budget: $X

## Risks & Mitigation
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Risk 1 | Medium | High | Mitigation 1 |
| Risk 2 | Low | Medium | Mitigation 2 |

## Notes
- Additional context
- Important decisions
- Lessons learned

## Change Log
| Date | Change | Reason |
|------|--------|--------|
| 2026-02-28 | Initial plan | Project kickoff |
| 2026-03-01 | Updated timeline | Scope expansion |

---
*Created by Planning Agent*
*Last updated: 2026-02-28 14:00:00*
```

## Usage

### Create New Plan
```bash
# Via AI Employee
/ai-employee
"I need to implement Gmail integration for the AI Employee. Create a project plan."

# Creates:
AI_Employee_Vault/Plans/Plan_Gmail_Integration.md
```

### Update Existing Plan
```bash
# Update progress
/plan-update --project "Gmail Integration" --task "Task 1.1" --status "complete"

# Add new task
/plan-update --project "Gmail Integration" --add-task "Task 1.4 (2h) - Testing"

# Mark phase complete
/plan-update --project "Gmail Integration" --phase "Phase 1" --status "complete"
```

## Reasoning Loop

### Iterative Planning Process
```
1. Analyze Requirements
    ↓
2. Initial Plan Created
    ↓
3. Execute First Phase
    ↓
4. Review & Learn
    ↓
5. Update Plan
    ↓
6. Execute Next Phase
    ↓
7. Repeat until complete
```

### Example: Gmail Integration

#### Iteration 1 - Initial Plan
```markdown
## Phase 1: Setup
- [ ] Get API credentials (1h)
- [ ] Create watcher script (4h)
- [ ] Test basic functionality (2h)
```

#### Iteration 2 - After Testing
```markdown
## Phase 1: Setup
- [x] Get API credentials (1h) ✅
- [x] Create watcher script (4h) ✅
- [x] Test basic functionality (2h) ✅

## Phase 2: Enhancement (Added after learning)
- [ ] Add priority detection (2h)
- [ ] Implement categorization (3h)
- [ ] Create email templates (2h)
```

## Project Types

### 1. Feature Development
- Requirements gathering
- Design & architecture
- Implementation
- Testing
- Documentation
- Deployment

### 2. Integration Project
- API research
- Authentication setup
- Core implementation
- Error handling
- Testing & validation
- Documentation

### 3. Process Improvement
- Current state analysis
- Future state design
- Gap analysis
- Implementation plan
- Training & rollout
- Metrics & review

### 4. Research Project
- Literature review
- Hypothesis formation
- Data collection
- Analysis
- Conclusions
- Report writing

## Dependencies

### Task Dependencies
```
Task A (Foundation)
    ↓
Task B (Builds on A)
    ↓
Task C (Requires B)
```

### Parallel Tasks
```
Task A ──┐
         ├──→ Task D (Combine results)
Task B ──┘
```

### Blocking Tasks
```
Task A (Blocked by external dependency)
    ↓ (wait for dependency)
Task B (Can start when A unblocks)
```

## Progress Tracking

### Task States
| Status | Symbol | Description |
|--------|--------|-------------|
| Not Started | [ ] | Task defined, not started |
| In Progress | [~] | Currently being worked on |
| Complete | [x] | Finished and verified |
| Blocked | [⏸] | Waiting for dependency |
| Cancelled | [-] | No longer needed |

### Phase Tracking
```markdown
## Phase Summary

| Phase | Status | Tasks | Complete | Hours |
|-------|--------|-------|----------|-------|
| Phase 1 | ✅ Complete | 3/3 | 100% | 4h |
| Phase 2 | 🔄 In Progress | 2/4 | 50% | 7h |
| Phase 3 | ⏳ Not Started | 0/3 | 0% | 0h |
| Phase 4 | ⏳ Not Started | 0/3 | 0% | 0h |

**Overall Progress:** 5/13 tasks (38%)
**Hours:** 11h / 20h estimated
```

## Integration with AI Employee

### Auto-Create Plans
When AI Employee detects complex task:
```
Task: "Implement Gmail integration"
    ↓ (AI Employee recognizes complexity)
Planning Agent activated
    ↓
Plan created: Plans/Plan_Gmail_Integration.md
    ↓
Tasks broken into actionable items
    ↓
Added to Needs_Action/ as sub-tasks
```

### Update Plans from Progress
```
Task completed in Done/
    ↓
Planning Agent updates Plan.md
    ↓
Marks task complete
    ↓
Updates progress percentage
    ↓
Identifies next tasks
    ↓
Creates new items in Needs_Action/
```

## Best Practices

### Planning
1. **Start Simple** - Initial plan doesn't need to be perfect
2. **Break Down** - Large tasks → smaller subtasks
3. **Estimate Conservatively** - Double initial estimates
4. **Identify Dependencies** - What blocks what
5. **Define Success** - Clear criteria for completion

### Execution
1. **One Phase at a Time** - Don't jump ahead
2. **Update Regularly** - Keep plan current
3. **Track Time** - Compare estimates vs actual
4. **Document Decisions** - Why changes were made
5. **Celebrate Milestones** - Mark phase completions

### Updates
1. **Be Honest** - If behind, update plan
2. **Learn & Adapt** - Use lessons learned
3. **Communicate** - Flag issues early
4. **Maintain History** - Keep change log
5. **Archive Completed** - Move to Done/ when finished

## Plan Review

### Weekly Review
```markdown
## Weekly Review - Week of 2026-02-28

### Accomplishments
- ✅ Completed Phase 1
- ✅ Stayed within timeline
- ✅ No critical issues

### Challenges
- ⚠️ Task 2.1 took longer than estimated
- ⚠️ Dependency delayed start of Phase 2

### Next Week Goals
- Complete Phase 2
- Start Phase 3
- Resolve blocking issues

### Updated Timeline
- Original: 2026-03-15
- New: 2026-03-20 (+5 days)
- Reason: Added enhancement scope
```

## Templates

### Quick Plan Template
```bash
# Create quick plan
/plan-create --name "Quick Task" --hours 4

# Creates:
## Phase 1: Execution
- [ ] Research (1h)
- [ ] Implementation (2h)
- [ ] Testing (1h)
```

### Standard Plan Template
```bash
# Create standard plan
/plan-create --name "Standard Project" --template standard

# Creates with:
- 4 phases (Planning, Implementation, Testing, Deployment)
- Risk assessment
- Resource requirements
- Success criteria
```

### Complex Plan Template
```bash
# Create complex plan
/plan-create --name "Complex Initiative" --template complex

# Creates with:
- Multiple workstreams
- Cross-dependencies
- Milestone tracking
- Budget tracking
- Stakeholder analysis
```

## Troubleshooting

### Plan Not Created
- Check if Plans/ folder exists
- Verify task complexity warrants plan
- Review planning agent logs

### Plan Not Updated
- Check file permissions
- Verify plan file format
- Review update logs

### Tasks Not Created
- Confirm plan has phases
- Check if tasks are already in Needs_Action/
- Review task generation logic

---

*For project planning best practices: https://www.projectmanagement.com/ *
*For agile planning: https://www.atlassian.com/agile*
