---
name: linkedin-poster
description: |
  LinkedIn Poster for automatically posting content to LinkedIn.
  Creates professional posts about business updates, insights, and achievements.
  Requires human approval before posting (human-in-the-loop).
---

# LinkedIn Poster

Automatically generate and post professional content to LinkedIn to grow your business presence.

## Overview

The LinkedIn Poster creates engaging, professional posts about your business and publishes them to LinkedIn. It follows human-in-the-loop approval workflow - all posts are drafted first, require your approval, then posted.

## Prerequisites

### LinkedIn Account
- Active LinkedIn account
- LinkedIn company page (optional but recommended)
- LinkedIn cookies or API access

### LinkedIn Automation Setup

#### Option 1: Playwright MCP (Recommended)
```bash
# Already installed with browsing-with-playwright skill
# Uses browser automation for posting
```

#### Option 2: LinkedIn API
- Apply for LinkedIn Developer Program
- Create application
- Get API keys
- Request posting permissions

## Configuration

### Environment Variables
```bash
# watchers/.env
LINKEDIN_EMAIL=your@email.com
LINKEDIN_PASSWORD=your_password
LINKEDIN_POSTING_ENABLED=true
LINKEDIN_DEFAULT_AUDIENCE=PUBLIC  # PUBLIC or CONNECTIONS
```

### Post Templates
```yaml
# watchers/linkedin_templates.yaml
templates:
  business_update:
    format: "🚀 {headline}\n\n{content}\n\n{hashtags}"
    tone: professional

  achievement:
    format: "🎉 Proud to share: {achievement}\n\n{details}\n\n{hashtags}"
    tone: celebratory

  insight:
    format: "💡 {insight_title}\n\n{insight_content}\n\n{hashtags}"
    tone: thought_leadership

  product_launch:
    format: "✨ Introducing: {product_name}\n\n{description}\n\n{hashtags}"
    tone: promotional
```

## Workflow

### 1. Create Post Draft
```bash
# Manual trigger
/linkedin-poster --draft --topic "business update"

# Auto-generated from business content
/ai-employee will create post drafts in Needs_Action/
```

### 2. Review & Approve
Post drafts are created in:
```
AI_Employee_Vault/Pending_Approval/LinkedIn/YYYY-MM-DD_post_title.md
```

Review the draft, then approve:
```bash
mv "AI_Employee_Vault/Pending_Approval/LinkedIn/post.md" \
   "AI_Employee_Vault/Ready_To_Post/LinkedIn/"
```

### 3. Automatic Posting
Approved posts are picked up by scheduler and posted automatically.

## Post Format

### Draft File Structure
```markdown
---
type: linkedin_post
status: draft
created: 2026-02-28T14:00:00
scheduled: 2026-02-28T18:00:00
platform: linkedin
audience: PUBLIC
hashtags: AI, Automation, Technology
---

# LinkedIn Post: Business Update

## Content
🚀 Exciting update from our team!

We're making great progress on our AI Employee project. The Bronze Tier is complete with full task automation and vault integration.

## Key Achievements
- ✅ File System Watcher operational
- ✅ AI Employee Skill deployed
- ✅ 5+ tasks processed successfully
- ✅ Full audit logging

## What's Next
- Silver Tier: Gmail integration
- LinkedIn auto-posting (like this!)
- Email MCP server

Stay tuned for more updates! 🚀

## Hashtags
#AI #Automation #Productivity #Technology #Innovation

## Engagement Goals
- Likes: 50+
- Comments: 10+
- Shares: 5+

---
*Drafted by LinkedIn Poster*
*Requires approval before posting*
```

## Post Types

### 1. Business Updates
- Milestone achievements
- Product launches
- Team announcements
- Company news

### 2. Thought Leadership
- Industry insights
- Trend analysis
- Best practices
- Lessons learned

### 3. Product Features
- Feature highlights
- Use cases
- Tips & tricks
- Tutorials

### 4. Behind the Scenes
- Development journey
- Team culture
- Work process
- Day in the life

## Content Guidelines

### Do's ✅
- Be authentic and genuine
- Provide value to your audience
- Use professional yet conversational tone
- Include relevant hashtags (3-5)
- Add call-to-action when appropriate
- Use emojis sparingly (1-3 per post)
- Tag relevant people/companies

### Don'ts ❌
- Overly promotional content
- Controversial topics
- Political or religious content
- Excessive hashtags (>10)
- Poor grammar or typos
- Misleading information

### Best Practices
- **Optimal Length:** 1300-1500 characters (~3 paragraphs)
- **Best Times:** 8-10am, 12-2pm, 5-6pm (weekday)
- **Frequency:** 2-3 posts per week
- **Engagement:** Respond to comments within 24 hours

## Posting Schedule

### Automated Schedule
```bash
# watchers/schedule.yaml
linkedin_posts:
  - day: Monday
    time: "09:00"
    type: business_update

  - day: Wednesday
    time: "12:00"
    type: thought_leadership

  - day: Friday
    time: "17:00"
    type: product_highlight
```

### Ad-Hoc Posting
```bash
# Create immediate post
/linkedin-poster --create --content "Your post content here"

# Schedule for specific time
/linkedin-poster --schedule "2026-03-01 14:00" --content "..."
```

## Analytics

### Track Performance
```markdown
# AI_Employee_Vault/Accounting/LinkedIn_Metrics_YYYY-MM.md

## Post Performance - March 2026

| Date | Post | Likes | Comments | Shares | Reach |
|------|------|-------|----------|--------|-------|
| 03-01 | Business Update | 45 | 8 | 3 | 1,250 |
| 03-04 | AI Insights | 78 | 15 | 7 | 2,100 |
| 03-07 | Product Launch | 123 | 22 | 12 | 3,400 |
```

### Monthly Reports
Auto-generated summaries:
- Total posts this month
- Average engagement rate
- Top performing posts
- Follower growth
- Recommendations

## Human-in-the-Loop Approval

### Approval Workflow
```
1. Draft Created (AI)
   ↓
2. Review Required (You)
   ↓
3. Edit/Approve/Reject (You)
   ↓
4. Scheduled for Posting (AI)
   ↓
5. Posted (Automation)
   ↓
6. Performance Tracked (AI)
```

### Approval Actions
```bash
# Approve for posting
/approve --post "post_id"

# Edit before approval
/edit-post "post_id" --add "Additional content"

# Reject post
/reject --post "post_id" --reason "Not aligned with brand"
```

## Integration with AI Employee

### Content Generation
The AI Employee can auto-generate posts from:
- Completed tasks (achievements)
- New features (product updates)
- Lessons learned (thought leadership)
- Milestones (business updates)

### Example Workflow
```bash
# 1. Complete a task
/ai-employee processes task

# 2. Auto-generate LinkedIn post
"Bronze Tier complete! Creating LinkedIn post draft..."

# 3. Post appears in Pending_Approval
AI_Employee_Vault/Pending_Approval/LinkedIn/bronze_complete.md

# 4. You review and approve
mv Pending_Approval/LinkedIn/bronze_complete.md \
   Ready_To_Post/LinkedIn/

# 5. Scheduler posts it
"Posting to LinkedIn at scheduled time..."

# 6. Track performance
Metrics saved to Accounting/LinkedIn_Metrics.md
```

## Troubleshooting

### Login Issues
```bash
# Clear cookies and re-authenticate
rm watchers/linkedin_cookies.json
/start-linkedin-watcher.sh
```

### Post Failed
- Check LinkedIn account status
- Verify content meets LinkedIn guidelines
- Check for API rate limits
- Review browser automation logs

### Approval Not Working
- Verify file paths
- Check scheduler is running
- Review approval workflow logs

## Monitoring

### Check Status
```bash
# Pending approval
ls AI_Employee_Vault/Pending_Approval/LinkedIn/

# Scheduled to post
ls AI_Employee_Vault/Ready_To_Post/LinkedIn/

# Recent posts
tail -20 AI_Employee_Vault/Accounting/LinkedIn_Metrics.md
```

## Security

### Credentials Protection
- LinkedIn credentials in `.env` (never committed)
- Cookies encrypted locally
- No credentials in post drafts
- Session tokens auto-expire

### Posting Safety
- All posts require approval
- No direct posting without review
- Content validation before posting
- Post logging for audit trail

---

*For LinkedIn best practices: https://www.linkedin.com/help/linkedin/answer/49167*
*For LinkedIn API: https://learn.microsoft.com/en-us/linkedin/shared/references/v2/ *
