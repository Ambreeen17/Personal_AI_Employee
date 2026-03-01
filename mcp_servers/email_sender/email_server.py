#!/usr/bin/env python3
"""
Email Sender MCP Server
Send emails via SMTP with human-in-the-loop approval workflow.
"""
import asyncio
import os
import smtplib
import logging
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path
from datetime import datetime
from typing import Optional

# MCP imports
from mcp.server import Server
from mcp.types import Tool, TextContent

# Configuration
VAULT_PATH = Path(__file__).parent.parent.parent / "AI_Employee_Vault"
READY_TO_SEND_PATH = VAULT_PATH / "Ready_To_Send" / "Email"
DONE_PATH = VAULT_PATH / "Done"
ENV_FILE = Path(__file__).parent / ".env"

# Default SMTP configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
SMTP_FROM = os.getenv('SMTP_FROM', '')
SMTP_FROM_NAME = os.getenv('SMTP_FROM_NAME', 'AI Employee')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('EmailSender')


class EmailSenderServer:
    """Email Sender MCP Server with SMTP integration."""

    def __init__(self):
        """Initialize Email Sender server."""
        self.server = Server("email-sender")
        self.setup_tools()

    def setup_tools(self):
        """Set up MCP tools."""
        self.server.tool("send_email")(self.send_email)
        self.server.tool("draft_email")(self.draft_email)
        self.server.tool("check_queue")(self.check_queue)

    async def send_email(self, to: str, subject: str, body: str,
                        cc: Optional[str] = None, bcc: Optional[str] = None,
                        attachments: Optional[str] = None) -> str:
        """
        Send email via SMTP.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (markdown or plain text)
            cc: CC recipients (comma-separated)
            bcc: BCC recipients (comma-separated)
            attachments: File paths to attach (comma-separated)

        Returns:
            JSON string with message_id and timestamp
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM}>"
            msg['To'] = to

            if cc:
                msg['Cc'] = cc
            if bcc:
                msg['Bcc'] = bcc

            # Add body
            # Check if body is markdown (contains markdown syntax)
            if any(md in body for md in ['#', '**', '*', '```', '- ']):
                # For markdown, send as HTML (simple conversion)
                html_body = self._markdown_to_html(body)
                part1 = MIMEText(body, 'plain')
                part2 = MIMEText(html_body, 'html')
                msg.attach(part1)
                msg.attach(part2)
            else:
                # Plain text
                msg.attach(MIMEText(body, 'plain'))

            # Add attachments
            if attachments:
                for att_path in attachments.split(','):
                    att_path = att_path.strip()
                    if Path(att_path).exists():
                        self._add_attachment(msg, att_path)

            # Send email
            await self._send_via_smtp(msg)

            # Log to Done/
            message_id = self._generate_message_id()
            self._log_sent_email(to, subject, message_id)

            return json.dumps({
                'success': True,
                'message_id': message_id,
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return json.dumps({
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })

    async def draft_email(self, to: str, subject: str, body: str,
                          save_to: Optional[str] = None) -> str:
        """
        Create email draft for approval (doesn't send).

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            save_to: Path to save draft (default: Pending_Approval/Email/)

        Returns:
            JSON string with draft file path
        """
        try:
            # Default save location
            if not save_to:
                save_to = VAULT_PATH / "Pending_Approval" / "Email"

            save_path = Path(save_to)
            save_path.mkdir(parents=True, exist_ok=True)

            # Create draft filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            safe_subject = subject.replace(' ', '_')[:50]
            draft_filename = f"{timestamp}_draft_{safe_subject}.md"
            draft_path = save_path / draft_filename

            # Create draft content
            draft_content = f"""---
type: email_draft
status: pending_approval
from: {SMTP_FROM}
to: {to}
subject: {subject}
created: {datetime.now().isoformat()}
priority: normal
---

# Email Draft: {subject}

## To
{to}

## Subject
{subject}

## Body
{body}

## Attachments
None

---
*Drafted by Email Sender*
*Awaits your approval before sending*
"""

            # Write draft file
            with open(draft_path, 'w', encoding='utf-8') as f:
                f.write(draft_content)

            logger.info(f"Created email draft: {draft_filename}")

            return json.dumps({
                'success': True,
                'draft_file': str(draft_path),
                'timestamp': datetime.now().isoformat()
            })

        except Exception as e:
            logger.error(f"Error creating draft: {e}")
            return json.dumps({
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })

    async def check_queue(self) -> str:
        """
        Check Ready_To_Send/Email/ folder and send all approved emails.

        Returns:
            JSON string with results
        """
        try:
            results = {
                'success': True,
                'checked': datetime.now().isoformat(),
                'sent': [],
                'failed': []
            }

            # Check if folder exists
            if not READY_TO_SEND_PATH.exists():
                return json.dumps(results)

            # Get all email files in Ready_To_Send/
            email_files = list(READY_TO_SEND_PATH.glob("*.md"))

            if not email_files:
                return json.dumps(results)

            logger.info(f"Found {len(email_files)} emails to send")

            # Process each email
            for email_file in email_files:
                try:
                    # Read email file
                    content = email_file.read_text(encoding='utf-8')

                    # Extract metadata
                    metadata = self._parse_email_metadata(content)
                    to = metadata.get('to', '')
                    subject = metadata.get('subject', '')
                    body = self._extract_email_body(content)

                    # Send email
                    result = json.loads(await self.send_email(to, subject, body))

                    if result.get('success'):
                        # Move to Done/
                        done_filename = f"{datetime.now().strftime('%Y-%m-%d')}_sent_{email_file.name}"
                        done_path = DONE_PATH / done_filename
                        email_file.rename(done_path)

                        results['sent'].append({
                            'original': str(email_file.name),
                            'done_file': str(done_filename),
                            'message_id': result.get('message_id')
                        })
                        logger.info(f"Sent and archived: {email_file.name}")
                    else:
                        results['failed'].append({
                            'file': str(email_file.name),
                            'error': result.get('error')
                        })

                except Exception as e:
                    logger.error(f"Error processing {email_file.name}: {e}")
                    results['failed'].append({
                        'file': str(email_file.name),
                        'error': str(e)
                    })

            return json.dumps(results)

        except Exception as e:
            logger.error(f"Error checking queue: {e}")
            return json.dumps({
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })

    async def _send_via_smtp(self, msg: MIMEMultipart):
        """Send message via SMTP."""
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
                logger.info("Email sent successfully via SMTP")
        except Exception as e:
            logger.error(f"SMTP error: {e}")
            raise

    def _markdown_to_html(self, markdown: str) -> str:
        """Convert simple markdown to HTML."""
        html = markdown
        # Simple conversions
        html = html.replace('**', '<strong>').replace('*', '<strong>')
        html = html.replace('\n\n', '</p><p>')
        html = html.replace('\n', '<br>')
        return f"<p>{html}</p>"

    def _add_attachment(self, msg: MIMEMultipart, file_path: str):
        """Add attachment to message."""
        with open(file_path, 'rb') as f:
            part = MIMEApplication(f.read(), Name=Path(file_path).name)
            part['Content-Disposition'] = f'attachment; filename="{Path(file_path).name}"'
            msg.attach(part)

    def _generate_message_id(self) -> str:
        """Generate unique message ID."""
        import uuid
        return f"{uuid.uuid4()}@ai-employee"

    def _log_sent_email(self, to: str, subject: str, message_id: str):
        """Log sent email to Done/ folder."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        log_filename = f"{timestamp}_sent_email.md"
        log_path = DONE_PATH / log_filename

        log_content = f"""---
type: sent_email
sent: {datetime.now().isoformat()}
message_id: {message_id}
status: sent
---

# Email Sent: {subject}

## Details
- **To:** {to}
- **From:** {SMTP_FROM}
- **Subject:** {subject}
- **Sent:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Message ID:** {message_id}

---
*Sent via Email Sender MCP*
*SMTP: {SMTP_SERVER}:{SMTP_PORT}*
"""

        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(log_content)

    def _parse_email_metadata(self, content: str) -> dict:
        """Parse YAML frontmatter from email file."""
        metadata = {}
        in_frontmatter = False
        frontmatter_lines = []

        for line in content.split('\n'):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    break
            if in_frontmatter:
                frontmatter_lines.append(line)

        for line in frontmatter_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

        return metadata

    def _extract_email_body(self, content: str) -> str:
        """Extract email body from markdown file."""
        # Find content after first ---
        parts = content.split('---', 2)
        if len(parts) > 2:
            return parts[2].strip()
        return content


async def main():
    """Main entry point for Email Sender MCP server."""
    logger.info("="*60)
    logger.info("AI Employee - Email Sender MCP Server")
    logger.info("="*60)

    # Check configuration
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        logger.error("SMTP credentials not configured!")
        logger.error("Please set SMTP_USERNAME and SMTP_PASSWORD in .env file")
        return

    # Create server
    server = EmailSenderServer()

    # Check queue on startup
    logger.info("Checking for emails in Ready_To_Send/...")
    queue_result = await server.check_queue()
    logger.info(f"Queue check result: {queue_result}")

    # Run server
    logger.info("Starting Email Sender MCP server on stdio...")
    logger.info("Listening for MCP requests...")

    async with server.server.stdio_server() as streams:
        await streams[0].drain()


if __name__ == "__main__":
    asyncio.run(main())
