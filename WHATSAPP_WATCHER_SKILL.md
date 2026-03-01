# WhatsApp Watcher Skill

**Created:** 2026-03-01
**Status:** Ready for Implementation
**Tier:** Silver (Optional)

---

## 🎯 Purpose

Monitor WhatsApp messages via WhatsApp Web automation and create action items for urgent communications.

**Use Cases:**
- Client inquiries requiring immediate attention
- Urgent business requests (pricing, invoices, support)
- Team coordination messages
- Keyword-triggered notifications (urgent, asap, help, payment)

---

## ⚠️ Important Disclaimer

**WhatsApp Terms of Service Warning:**
- Automating WhatsApp Web may violate WhatsApp's Terms of Service
- Use at your own risk - this is for educational/personal use
- WhatsApp may ban accounts detected using automation
- Consider using official WhatsApp Business API for production
- This implementation uses Playwright browser automation

**Recommendation:**
- Use responsibly with appropriate delays between actions
- Don't spam or send automated messages without consent
- Consider WhatsApp Business API for legitimate business use cases

---

## 🏗️ Architecture

### Technology Stack
- **Playwright:** Browser automation
- **Chromium:** Persistent browser context
- **Python:** Watcher script implementation
- **BaseWatcher:** Inherits from core watcher class

### Design Pattern
```python
WhatsAppWatcher(BaseWatcher)
├── Persistent browser session
├── Keyword detection
├── Message extraction
└── Action file creation
```

---

## 📁 File Structure

```
watchers/
├── whatsapp_watcher.py          # Main watcher script
├── whatsapp_session/            # Persistent browser session (gitignored)
│   └── [Playwright session files]
├── whatsapp_state.json          # Processed message IDs (gitignored)
└── whatsapp_keywords.yaml       # Configurable keywords

mcp_servers/
└── whatsapp_sender/             # Optional: WhatsApp reply MCP
    ├── server.py                # MCP server for sending messages
    ├── package.json             # Node.js dependencies
    └── .env                     # Authentication (gitignored)
```

---

## 🔧 Implementation

### 1. WhatsApp Watcher Script

```python
# watchers/whatsapp_watcher.py
from playwright.sync_api import sync_playwright
from pathlib import Path
import json
import time
from datetime import datetime
from typing import Optional, Dict, List
import yaml

class WhatsAppWatcher:
    """Monitor WhatsApp Web for urgent messages."""

    def __init__(
        self,
        vault_path: str,
        session_path: Optional[str] = None,
        keywords_file: Optional[str] = None,
        check_interval: int = 60
    ):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.session_path = Path(session_path or self.vault_path / 'watchers/whatsapp_session')
        self.state_file = self.vault_path / 'watchers/whatsapp_state.json'
        self.check_interval = check_interval

        # Load keywords
        self.keywords = self._load_keywords(keywords_file)

        # Load processed messages
        self.processed_ids = self._load_state()

        # Ensure session directory exists
        self.session_path.mkdir(parents=True, exist_ok=True)

    def _load_keywords(self, keywords_file: Optional[str]) -> List[str]:
        """Load urgency keywords from config file."""
        default_keywords = [
            'urgent', 'asap', 'invoice', 'payment', 'help',
            'pricing', 'quote', 'meeting', 'deadline', 'emergency'
        ]

        if keywords_file and Path(keywords_file).exists():
            with open(keywords_file, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('keywords', default_keywords)

        return default_keywords

    def _load_state(self) -> set:
        """Load processed message IDs from state file."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                return set(json.load(f))
        return set()

    def _save_state(self):
        """Save processed message IDs to state file."""
        with open(self.state_file, 'w') as f:
            json.dump(list(self.processed_ids), f)

    def check_for_updates(self) -> List[Dict]:
        """Check for new WhatsApp messages containing keywords."""
        messages = []

        try:
            with sync_playwright() as p:
                # Launch persistent browser context
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.session_path),
                    headless=True,
                    args=['--disable-blink-features=AutomationControlled']
                )

                page = browser.new_page()

                # Navigate to WhatsApp Web
                page.goto('https://web.whatsapp.com', timeout=60000)

                # Wait for login (if not authenticated)
                # You'll need to manually scan QR code on first run

                # Wait for chat list to load
                page.wait_for_selector('div[contenteditable="true"]', timeout=30000)

                # Get all chats
                chats = page.query_selector_all('div[role="listitem"]')

                for chat in chats[:50]:  # Limit to recent 50 chats
                    try:
                        # Click on chat to open
                        chat.click()

                        # Wait for messages to load
                        time.sleep(1)

                        # Get last message
                        last_message = page.query_selector('div[role="listitem"] div.copyable-area')

                        if last_message:
                            message_text = last_message.inner_text().lower()

                            # Check for keywords
                            if any(keyword.lower() in message_text for keyword in self.keywords):
                                # Get sender info
                                sender = page.query_selector('span[title]')
                                sender_name = sender.get_attribute('title') if sender else 'Unknown'

                                # Generate unique ID
                                message_id = f"whatsapp_{sender_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

                                if message_id not in self.processed_ids:
                                    messages.append({
                                        'id': message_id,
                                        'sender': sender_name,
                                        'message': last_message.inner_text(),
                                        'timestamp': datetime.now().isoformat()
                                    })

                                    self.processed_ids.add(message_id)

                    except Exception as e:
                        print(f"Error processing chat: {e}")
                        continue

                browser.close()

        except Exception as e:
            print(f"Error in WhatsApp watcher: {e}")

        return messages

    def create_action_file(self, message: Dict) -> Path:
        """Create an action file for the urgent message."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"WHATSAPP_{message['sender'].replace(' ', '_')}_{timestamp}.md"
        filepath = self.needs_action / filename

        # Determine priority
        priority = "High" if any(k in message['message'].lower() for k in ['urgent', 'asap', 'emergency']) else "Normal"

        content = f"""# WhatsApp Message from {message['sender']}

**Priority:** {priority}
**Received:** {message['timestamp']}
**Source:** WhatsApp

## Message

{message['message']}

## Action Required

- [ ] Review message
- [ ] Determine response needed
- [ ] Draft response (if applicable)
- [ ] Move to Done/ after processing

## Context

This message was detected by the WhatsApp Watcher because it contains one of the monitored keywords: {', '.join(self.keywords)}.

---
*Created by WhatsApp Watcher*
"""

        filepath.write_text(content)
        return filepath

    def run(self):
        """Main loop to continuously check for messages."""
        print(f"Starting WhatsApp Watcher (checking every {self.check_interval}s)")
        print(f"Monitoring keywords: {', '.join(self.keywords)}")
        print(f"Session path: {self.session_path}")

        while True:
            try:
                messages = self.check_for_updates()

                for message in messages:
                    print(f"New urgent message from {message['sender']}")
                    filepath = self.create_action_file(message)
                    print(f"Created: {filepath}")

                # Save state
                self._save_state()

            except KeyboardInterrupt:
                print("\nStopping WhatsApp Watcher...")
                break
            except Exception as e:
                print(f"Error in watcher loop: {e}")

            # Wait before next check
            time.sleep(self.check_interval)


if __name__ == '__main__':
    import sys

    vault_path = sys.argv[1] if len(sys.argv) > 1 else '../AI_Employee_Vault'
    session_path = sys.argv[2] if len(sys.argv) > 2 else None

    watcher = WhatsAppWatcher(
        vault_path=vault_path,
        session_path=session_path,
        check_interval=60
    )

    watcher.run()
```

### 2. Keywords Configuration

```yaml
# watchers/whatsapp_keywords.yaml
keywords:
  # Urgency indicators
  - urgent
  - asap
  - emergency
  - immediately
  - deadline

  # Business terms
  - invoice
  - payment
  - pricing
  - quote
  - proposal
  - contract

  # Requests
  - help
  - support
  - meeting
  - call
  - discuss

  # Project terms
  - delivery
  - shipment
  - status
  - update
```

### 3. Startup Script (Windows)

```batch
@echo off
REM watchers/start_whatsapp_watcher.bat
cd /d "%~dp0"
python whatsapp_watcher.py ../AI_Employee_Vault
pause
```

### 4. Startup Script (Unix/Linux/macOS)

```bash
#!/bin/bash
# watchers/start_whatsapp_watcher.sh
cd "$(dirname "$0")"
python whatsapp_watcher.py ../AI_Employee_Vault
```

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install playwright pyyaml
playwright install chromium
```

### Step 2: Initial QR Code Scan

1. Run the watcher for the first time:
   ```bash
   python watchers/whatsapp_watcher.py
   ```

2. A Chromium browser window will open with WhatsApp Web

3. Scan the QR code with your phone:
   - Open WhatsApp on your phone
   - Go to Settings → Linked Devices
   - Tap "Link a Device"
   - Scan the QR code

4. The session will be saved and reused for future runs

### Step 3: Configure Keywords (Optional)

Edit `watchers/whatsapp_keywords.yaml` to customize which keywords trigger alerts:

```yaml
keywords:
  - urgent
  - asap
  - your-custom-keyword
```

### Step 4: Run the Watcher

**Windows:**
```bash
watchers\start_whatsapp_watcher.bat
```

**Unix/Linux/macOS:**
```bash
chmod +x watchers/start_whatsapp_watcher.sh
watchers/start_whatsapp_watcher.sh
```

---

## 🔄 Integration with Approval Workflow

The WhatsApp Watcher integrates seamlessly with the existing approval workflow:

```
WhatsApp Message
    ↓
[Keyword Detection]
    ↓
Needs_Action/WHATSAPP_sender_timestamp.md
    ↓
[AI Employee Processing]
    ↓
Draft Response (if needed)
    ↓
Pending_Approval/WhatsApp/
    ↓
[Human Review]
    ↓
Ready_To_Send/WhatsApp/
    ↓
[WhatsApp Sender MCP / Manual Send]
    ↓
Done/
```

---

## 📊 Workflow Examples

### Example 1: Client Invoice Request

**Incoming WhatsApp:**
```
"Hey, can you send me the invoice for January?"
```

**Action File Created:**
```markdown
# WhatsApp Message from Client_A

**Priority:** Normal
**Received:** 2026-03-01T10:30:00
**Source:** WhatsApp

## Message

Hey, can you send me the invoice for January?

## Action Required

- [ ] Review message
- [ ] Generate January invoice
- [ ] Send invoice via email
- [ ] Move to Done/ after processing
```

**AI Employee Action:**
1. Reads action file
2. Checks accounting records
3. Generates invoice
4. Creates email draft in `Pending_Approval/Email/`
5. Waits for approval
6. Sends invoice via Email Sender MCP

### Example 2: Urgent Support Request

**Incoming WhatsApp:**
```
"URGENT! The system is down, we need help ASAP!"
```

**Action File Created:**
```markdown
# WhatsApp Message from Customer_X

**Priority:** High
**Received:** 2026-03-01T14:15:00
**Source:** WhatsApp

## Message

URGENT! The system is down, we need help ASAP!

## Action Required

- [ ] Review message
- [ ] Check system status
- [ ] Identify issue
- [ ] Provide immediate response
- [ ] Move to Done/ after processing
```

---

## 🔐 Security & Privacy

### Data Handling

✅ **Secure:**
- Session data stored locally (never synced)
- State file contains only message IDs (no content)
- No message content transmitted externally

❌ **NOT Recommended:**
- Don't sync `whatsapp_session/` folder
- Don't commit `whatsapp_state.json` to version control
- Don't use for spam or unsolicited messages

### .gitignore Entries

```gitignore
# WhatsApp Watcher
watchers/whatsapp_session/
watchers/whatsapp_state.json
watchers/whatsapp_keywords.yaml
```

---

## 🎛️ Configuration Options

### Watcher Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `vault_path` | string | Required | Path to Obsidian vault |
| `session_path` | string | `watchers/whatsapp_session/` | Browser session storage |
| `keywords_file` | string | `whatsapp_keywords.yaml` | Keywords config file |
| `check_interval` | int | 60 | Seconds between checks |

### Advanced Configuration

```python
# Custom initialization
watcher = WhatsAppWatcher(
    vault_path='../AI_Employee_Vault',
    session_path='./my_whatsapp_session',
    keywords_file='./custom_keywords.yaml',
    check_interval=30  # Check every 30 seconds
)
```

---

## 🐛 Troubleshooting

### Issue: QR Code Required Every Time

**Cause:** Session not being saved properly

**Solution:**
- Ensure `whatsapp_session/` directory exists
- Check file permissions on session directory
- Use absolute path for `session_path`

### Issue: No Messages Detected

**Cause:** Keywords not matching or page not loaded

**Solution:**
- Check `whatsapp_keywords.yaml` for correct keywords
- Increase wait time in `check_for_updates()`
- Verify WhatsApp Web is fully loaded

### Issue: WhatsApp Bans Account

**Cause:** Violation of ToS through automation

**Solution:**
- Stop using automation immediately
- Use official WhatsApp Business API for business use
- Increase delays between actions to avoid detection

### Issue: Browser Won't Launch Headless

**Cause:** Playwright or Chromium not installed

**Solution:**
```bash
playwright install chromium
playwright install-deps chromium
```

---

## 📈 Monitoring & Logging

### Add Logging to Watcher

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('whatsapp_watcher.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('WhatsAppWatcher')
```

### Log Rotation

```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'whatsapp_watcher.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
```

---

## 🚀 Future Enhancements

### Potential Features

1. **WhatsApp Sender MCP**
   - Send automated responses
   - Requires human approval via workflow
   - Integration with existing approval system

2. **Message Categorization**
   - Auto-categorize by sender (client, team, family)
   - Priority scoring algorithm
   - Smart filtering

3. **Reply Suggestions**
   - AI-generated reply drafts
   - Template-based responses
   - Context-aware suggestions

4. **Analytics Dashboard**
   - Message frequency tracking
   - Response time metrics
   - Keyword effectiveness analysis

---

## 📚 Related Documentation

- **Company Handbook:** `AI_Employee_Vault/Company_Handbook.md` - WhatsApp communication rules
- **Approval Workflow:** `SILVER_TIER_SKILLS.md` - Approval system details
- **Gmail Watcher:** `watchers/gmail_watcher.py` - Similar pattern for email
- **Hackathon Document:** `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`

---

## 🎓 Best Practices

### Do's ✅

- Use for legitimate business purposes
- Add appropriate delays between checks (60s minimum)
- Monitor for keyword spam
- Keep session data secure and local
- Test thoroughly before production use
- Respect WhatsApp's rate limits

### Don'ts ❌

- Don't use for mass messaging or spam
- Don't automate without consent
- Don't sync session data to cloud
- Don't commit sensitive session files
- Don't ignore WhatsApp's ToS
- Don't use for unsolicited marketing

---

## 📄 License & Disclaimer

This implementation is for educational and personal use only. Use of automated WhatsApp tools may violate WhatsApp's Terms of Service. Users are responsible for ensuring compliance with applicable laws and platform policies.

**Always respect user privacy and obtain consent before automated interactions.**

---

**WhatsApp Watcher Skill Document Complete!**

*Last Updated: 2026-03-01*
*Version: 1.0*
