#!/usr/bin/env python3
"""
Gmail Watcher for AI Employee
Monitors Gmail inbox and creates action items for new emails.
"""
import time
import logging
import base64
import pickle
import os
from pathlib import Path
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
NEEDS_ACTION_PATH = VAULT_PATH / "Needs_Action"
STATE_FILE = VAULT_PATH / "gmail_watcher_state.json"
LOG_FILE = VAULT_PATH / "gmail_watcher.log"
CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"
TOKEN_PATH = Path(__file__).parent / "token.json"

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify']

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('GmailWatcher')


class GmailWatcher:
    """Gmail Watcher for monitoring Gmail inbox and creating action items."""

    def __init__(self, vault_path=VAULT_PATH, check_interval=120):
        """
        Initialize Gmail Watcher.

        Args:
            vault_path: Path to the vault directory
            check_interval: Seconds between checks (default: 120)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.processed_ids = set()
        self.service = None

        # Ensure directories exist
        self.needs_action.mkdir(parents=True, exist_ok=True)

        # Load state
        self._load_state()

        # Authenticate with Gmail
        self._authenticate()

    def _load_state(self):
        """Load processed message IDs from state file."""
        if STATE_FILE.exists():
            try:
                import json
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                    self.processed_ids = set(state.get('processed_ids', []))
                logger.info(f"Loaded state: {len(self.processed_ids)} previously processed emails")
            except Exception as e:
                logger.error(f"Error loading state: {e}")

    def _save_state(self):
        """Save current state to file."""
        try:
            import json
            with open(STATE_FILE, 'w') as f:
                json.dump({'processed_ids': list(self.processed_ids)}, f)
        except Exception as e:
            logger.error(f"Error saving state: {e}")

    def _authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0."""
        logger.info("Authenticating with Gmail API...")

        creds = None
        # Load existing token if available
        if TOKEN_PATH.exists():
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
            logger.info("Loaded existing credentials")

        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                logger.info("Refreshed expired credentials")
            else:
                if CREDENTIALS_PATH.exists():
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_PATH, SCOPES)
                    creds = flow.run_local_server(port=0)
                    logger.info("Completed OAuth flow")

                # Save credentials for next run
                with open(TOKEN_PATH, 'w') as token:
                    token.write(creds)
                logger.info(f"Saved credentials to {TOKEN_PATH}")

        try:
            self.service = build('gmail', 'v1', credentials=creds)
            logger.info("Successfully authenticated with Gmail API")
        except Exception as e:
            logger.error(f"Failed to build Gmail service: {e}")
            raise

    def check_for_updates(self):
        """
        Check for new unread emails.

        Returns:
            List of new message IDs not in processed_ids
        """
        try:
            # Query for unread messages
            results = self.service.users().messages().list(
                userId='me',
                q='is:unread is:inbox'
            ).execute()

            messages = results.get('messages', [])
            new_messages = [m for m in messages if m['id'] not in self.processed_ids]

            if new_messages:
                logger.info(f"Found {len(new_messages)} new messages")

            return new_messages

        except HttpError as error:
            logger.error(f"Gmail API error: {error}")
            return []

    def get_priority(self, message):
        """
        Determine priority based on subject and content.

        Args:
            message: Gmail message object

        Returns:
            Priority level: 'Critical', 'High', 'Normal', or 'Low'
        """
        try:
            # Get message content
            msg_data = self.service.users().messages().get(
                userId='me',
                id=message['id'],
                format='metadata',
                metadataHeaders=['Subject']
            ).execute()

            # Extract subject
            headers = {h['name']: h['value'] for h in msg_data['payload'].get('headers', [])}
            subject = headers.get('Subject', '').lower()

            # Priority keywords
            critical_keywords = ['urgent', 'emergency', 'critical', 'asap', 'deadline']
            high_keywords = ['important', 'priority', 'please review', 'action required']
            low_keywords = ['fyi', 'for your information', 'newsletter', 'unsubscribe', 'update']

            # Check priority
            for keyword in critical_keywords:
                if keyword in subject:
                    return 'Critical'

            for keyword in high_keywords:
                if keyword in subject:
                    return 'High'

            for keyword in low_keywords:
                if keyword in subject:
                    return 'Low'

            return 'Normal'

        except Exception as e:
            logger.error(f"Error determining priority: {e}")
            return 'Normal'

    def get_message_content(self, message_id):
        """
        Get full message content including body.

        Args:
            message_id: Gmail message ID

        Returns:
            Dictionary with message details
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()

            # Extract headers
            headers = {}
            for h in message['payload'].get('headers', []):
                headers[h['name']] = h['value']

            # Extract body
            body = ""
            if 'parts' in message['payload']:
                # Multipart message
                for part in message['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
            elif 'body' in message['payload']:
                # Single part message
                if 'data' in message['payload']['body']:
                    body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')

            return {
                'headers': headers,
                'body': body,
                'snippet': message.get('snippet', ''),
                'timestamp': message['internalDate']
            }

        except Exception as e:
            logger.error(f"Error getting message content: {e}")
            return {'headers': {}, 'body': '', 'snippet': '', 'timestamp': ''}

    def create_action_file(self, message):
        """
        Create action file in Needs_Action folder for a new email.

        Args:
            message: Gmail message object

        Returns:
            Path to created action file
        """
        try:
            # Get message details
            content = self.get_message_content(message['id'])
            headers = content['headers']
            priority = self.get_priority(message)

            # Extract key fields
            from_email = headers.get('From', 'Unknown')
            subject = headers.get('Subject', 'No Subject')
            to_email = headers.get('To', 'me')
            date = headers.get('Date', '')

            # Create timestamp for filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            safe_subject = subject.replace(' ', '_')[:50]  # Limit length
            action_filename = f"{timestamp}_gmail_{safe_subject}.md"
            action_path = self.needs_action / action_filename

            # Create action file content
            action_content = f"""---
type: email
source: gmail_watcher
priority: {priority}
status: pending
created: {datetime.now().isoformat()}
message_id: {message['id']}
from: {from_email}
to: {to_email}
subject: {subject}
received: {date}
---

# New Email: {subject}

## Email Details
- **From:** {from_email}
- **To:** {to_email}
- **Subject:** {subject}
- **Date:** {date}
- **Priority:** {priority}
- **Message ID:** {message['id']}

## Content Preview
{content['snippet'][:500]}

## Full Content
```
{content['body'][:2000]}
```

{('[...]' if len(content['body']) > 2000 else '')}

## Suggested Actions
- [ ] Review email content
- [ ] Categorize and process
- [ ] Draft response if needed
- [ ] Extract action items
- [ ] Update Dashboard

---
*Created by Gmail Watcher at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

            # Write action file
            with open(action_path, 'w', encoding='utf-8') as f:
                f.write(action_content)

            logger.info(f"Created action file: {action_filename}")

            # Mark as processed
            self.processed_ids.add(message['id'])
            self._save_state()

            return action_path

        except Exception as e:
            logger.error(f"Error creating action file: {e}")
            return None

    def mark_as_read(self, message_id):
        """
        Mark message as read in Gmail.

        Args:
            message_id: Gmail message ID
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            logger.debug(f"Marked message {message_id} as read")
        except Exception as e:
            logger.error(f"Error marking message as read: {e}")

    def run(self):
        """Main loop - check for updates and process them."""
        logger.info("="*60)
        logger.info("AI Employee - Gmail Watcher")
        logger.info("="*60)
        logger.info(f"Monitoring Gmail for unread messages")
        logger.info(f"Check interval: {self.check_interval} seconds")
        logger.info(f"Action files will be created in: {self.needs_action}")
        logger.info("Press Ctrl+C to stop")

        try:
            while True:
                try:
                    # Check for new messages
                    messages = self.check_for_updates()

                    # Process each new message
                    for message in messages:
                        self.create_action_file(message)

                except Exception as e:
                    logger.error(f"Error in main loop: {e}")

                # Wait before next check
                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            logger.info("Shutting down Gmail Watcher...")
        finally:
            self._save_state()


def main():
    """Main entry point for Gmail Watcher."""
    import argparse

    parser = argparse.ArgumentParser(description='Gmail Watcher for AI Employee')
    parser.add_argument('--auth', action='store_true',
                       help='Run authentication flow')
    parser.add_argument('--check-once', action='store_true',
                       help='Check once and exit')
    parser.add_argument('--interval', type=int, default=120,
                       help='Check interval in seconds (default: 120)')

    args = parser.parse_args()

    # Create watcher
    watcher = GmailWatcher(check_interval=args.interval)

    if args.auth:
        # Re-authenticate
        logger.info("Running authentication flow...")
        watcher._authenticate()
        logger.info("Authentication complete")
    elif args.check_once:
        # Check once and exit
        logger.info("Checking once for new messages...")
        messages = watcher.check_for_updates()
        logger.info(f"Found {len(messages)} new messages")
        for message in messages:
            watcher.create_action_file(message)
        logger.info("Check complete")
    else:
        # Run continuously
        watcher.run()


if __name__ == "__main__":
    main()
