#!/usr/bin/env python3
"""
WhatsApp Watcher - Monitor WhatsApp Web for urgent messages

This script uses Playwright to automate WhatsApp Web and detect
urgent messages based on keywords. Creates action files in the
Needs_Action folder for processing by the AI Employee.

WARNING: Automating WhatsApp Web may violate WhatsApp's Terms of Service.
Use at your own risk for educational/personal purposes only.

Usage:
    python whatsapp_watcher.py [vault_path] [session_path]

Example:
    python whatsapp_watcher.py ../AI_Employee_Vault
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: Playwright not installed. Run: pip install playwright")
    print("Then run: playwright install chromium")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Run: pip install pyyaml")
    yaml = None


class WhatsAppWatcher:
    """Monitor WhatsApp Web for urgent messages and create action items."""

    def __init__(
        self,
        vault_path: str,
        session_path: Optional[str] = None,
        keywords_file: Optional[str] = None,
        check_interval: int = 60
    ):
        """
        Initialize WhatsApp Watcher.

        Args:
            vault_path: Path to Obsidian vault
            session_path: Path to store browser session (default: vault_path/watchers/whatsapp_session)
            keywords_file: Path to keywords YAML config (default: whatsapp_keywords.yaml)
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.session_path = Path(session_path or self.vault_path / 'watchers/whatsapp_session')
        self.state_file = self.vault_path / 'watchers/whatsapp_state.json'
        self.check_interval = check_interval

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.session_path.mkdir(parents=True, exist_ok=True)
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        # Load keywords
        self.keywords = self._load_keywords(keywords_file)

        # Load processed messages
        self.processed_ids = self._load_state()

        print(f"WhatsApp Watcher initialized")
        print(f"  Vault: {self.vault_path}")
        print(f"  Session: {self.session_path}")
        print(f"  Keywords: {', '.join(self.keywords)}")
        print(f"  Check interval: {self.check_interval}s")

    def _load_keywords(self, keywords_file: Optional[str]) -> List[str]:
        """Load urgency keywords from config file."""
        default_keywords = [
            'urgent', 'asap', 'invoice', 'payment', 'help',
            'pricing', 'quote', 'meeting', 'deadline', 'emergency',
            'immediately', 'support', 'delivery', 'status'
        ]

        keywords_path = Path(keywords_file or self.vault_path / 'watchers/whatsapp_keywords.yaml')

        if yaml and keywords_path.exists():
            try:
                with open(keywords_path, 'r') as f:
                    config = yaml.safe_load(f)
                    keywords = config.get('keywords', default_keywords)
                    print(f"Loaded keywords from {keywords_path}")
                    return keywords
            except Exception as e:
                print(f"Warning: Could not load keywords file: {e}")
                print("Using default keywords")

        return default_keywords

    def _load_state(self) -> set:
        """Load processed message IDs from state file."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return set(json.load(f))
            except Exception as e:
                print(f"Warning: Could not load state file: {e}")
                return set()
        return set()

    def _save_state(self):
        """Save processed message IDs to state file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(list(self.processed_ids), f)
        except Exception as e:
            print(f"Error saving state: {e}")

    def _determine_priority(self, message_text: str) -> str:
        """Determine message priority based on content."""
        urgent_keywords = ['urgent', 'asap', 'emergency', 'immediately']
        message_lower = message_text.lower()

        if any(keyword in message_lower for keyword in urgent_keywords):
            return "High"
        return "Normal"

    def check_for_updates(self) -> List[Dict]:
        """
        Check for new WhatsApp messages containing keywords.

        Returns:
            List of message dictionaries with id, sender, message, timestamp
        """
        messages = []

        try:
            with sync_playwright() as p:
                # Launch persistent browser context
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.session_path),
                    headless=False,  # Set to False for first-time QR scan
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                        '--disable-setuid-sandbox'
                    ]
                )

                page = browser.new_page()

                print("Navigating to WhatsApp Web...")
                page.goto('https://web.whatsapp.com', timeout=60000)

                # Wait for page to load
                try:
                    # Wait for either QR code or chat list (already logged in)
                    page.wait_for_selector('div[contenteditable="true"]', timeout=30000)
                    print("WhatsApp Web loaded successfully")
                except Exception as e:
                    print(f"Timeout waiting for WhatsApp Web: {e}")
                    print("You may need to scan the QR code manually")
                    browser.close()
                    return messages

                # Wait a bit for messages to load
                time.sleep(3)

                # Get all chats
                print("Checking for new messages...")
                chats = page.query_selector_all('div[role="listitem"]')

                # Limit to recent 20 chats to avoid overwhelming
                for idx, chat in enumerate(chats[:20]):
                    try:
                        # Get chat name/title before clicking
                        title_elem = chat.query_selector('span[title]')
                        sender_name = title_elem.get_attribute('title') if title_elem else f'Chat_{idx}'

                        # Click on chat to open
                        chat.click()
                        time.sleep(0.5)  # Small delay to load messages

                        # Get messages in this chat
                        message_divs = page.query_selector_all('div.copyable-area')

                        if message_divs:
                            # Get the last message
                            last_msg_div = message_divs[-1]
                            message_text = last_msg_div.inner_text().strip()

                            # Check for keywords
                            if message_text and any(
                                keyword.lower() in message_text.lower()
                                for keyword in self.keywords
                            ):
                                # Generate unique ID
                                timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                                message_id = f"whatsapp_{sender_name}_{timestamp_str}"

                                if message_id not in self.processed_ids:
                                    print(f"  Found urgent message from {sender_name}")
                                    messages.append({
                                        'id': message_id,
                                        'sender': sender_name,
                                        'message': message_text,
                                        'timestamp': datetime.now().isoformat()
                                    })

                                    self.processed_ids.add(message_id)

                    except Exception as e:
                        # Skip problematic chats
                        continue

                browser.close()

        except Exception as e:
            print(f"Error in WhatsApp watcher: {e}")
            import traceback
            traceback.print_exc()

        return messages

    def create_action_file(self, message: Dict) -> Path:
        """
        Create an action file for the urgent message.

        Args:
            message: Message dictionary with id, sender, message, timestamp

        Returns:
            Path to created action file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_sender = message['sender'].replace(' ', '_').replace('/', '_')[:50]
        filename = f"WHATSAPP_{safe_sender}_{timestamp}.md"
        filepath = self.needs_action / filename

        # Determine priority
        priority = self._determine_priority(message['message'])

        content = f"""# WhatsApp Message from {message['sender']}

**Priority:** {priority}
**Received:** {message['timestamp']}
**Source:** WhatsApp
**Message ID:** {message['id']}

## Message

{message['message']}

## Action Required

- [ ] Review message
- [ ] Determine response needed
- [ ] Draft response (if applicable)
- [ ] Move to Done/ after processing

## Context

This message was detected by the WhatsApp Watcher because it contains one of the monitored keywords: {', '.join(self.keywords[:5])}{'...' if len(self.keywords) > 5 else ''}.

**Note:** To respond, you can use WhatsApp Web directly or use the WhatsApp Sender MCP (if configured).

---
*Created by WhatsApp Watcher at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

        try:
            filepath.write_text(content, encoding='utf-8')
            print(f"Created action file: {filepath.name}")
        except Exception as e:
            print(f"Error creating action file: {e}")

        return filepath

    def run(self):
        """Main loop to continuously check for messages."""
        print("\n" + "="*60)
        print("WHATSAPP WATCHER RUNNING")
        print("="*60)
        print(f"Checking every {self.check_interval} seconds for keywords:")
        print(f"  {', '.join(self.keywords)}")
        print("\nPress Ctrl+C to stop")
        print("="*60 + "\n")

        while True:
            try:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for messages...")

                messages = self.check_for_updates()

                if messages:
                    print(f"Found {len(messages)} new message(s)")

                    for message in messages:
                        self.create_action_file(message)
                else:
                    print("No new urgent messages")

                # Save state
                self._save_state()

            except KeyboardInterrupt:
                print("\n\nStopping WhatsApp Watcher...")
                self._save_state()
                print("State saved. Goodbye!")
                break
            except Exception as e:
                print(f"Error in watcher loop: {e}")
                import traceback
                traceback.print_exc()

            # Wait before next check
            print(f"Waiting {self.check_interval} seconds...")
            time.sleep(self.check_interval)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        vault_path = sys.argv[1]
    else:
        # Default vault path
        vault_path = Path(__file__).parent.parent / 'AI_Employee_Vault'
        print(f"No vault path specified, using default: {vault_path}")

    if len(sys.argv) > 2:
        session_path = sys.argv[2]
    else:
        session_path = None

    watcher = WhatsAppWatcher(
        vault_path=str(vault_path),
        session_path=session_path,
        check_interval=60
    )

    watcher.run()


if __name__ == '__main__':
    main()
