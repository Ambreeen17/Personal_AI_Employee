#!/usr/bin/env python3
"""
File System Watcher for AI Employee
Monitors the Inbox folder and creates action files for new items.
"""
import time
import logging
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
INBOX_PATH = VAULT_PATH / "Inbox"
NEEDS_ACTION_PATH = VAULT_PATH / "Needs_Action"
DONE_PATH = VAULT_PATH / "Done"
IN_PROGRESS_PATH = VAULT_PATH / "In_Progress"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VAULT_PATH / 'watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('FileSystemWatcher')


class FileSystemWatcher(FileSystemEventHandler):
    """Watches for new files in Inbox and creates action items."""

    def __init__(self):
        super().__init__()
        self.processed_files = set()
        # Load previously processed files
        self._load_state()

    def _load_state(self):
        """Load state from previous runs."""
        state_file = VAULT_PATH / "watcher_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    state = json.load(f)
                    self.processed_files = set(state.get('processed_files', []))
                logger.info(f"Loaded state: {len(self.processed_files)} previously processed files")
            except Exception as e:
                logger.error(f"Error loading state: {e}")

    def _save_state(self):
        """Save current state."""
        state_file = VAULT_PATH / "watcher_state.json"
        try:
            with open(state_file, 'w') as f:
                json.dump({'processed_files': list(self.processed_files)}, f)
        except Exception as e:
            logger.error(f"Error saving state: {e}")

    def on_created(self, event):
        """Handle new file creation."""
        if event.is_directory:
            return

        file_path = Path(event.src_path)

        # Skip if already processed
        if str(file_path) in self.processed_files:
            return

        # Wait a moment for file to be fully written
        time.sleep(0.5)

        if not file_path.exists():
            return

        logger.info(f"New file detected: {file_path.name}")
        self._process_file(file_path)

    def _process_file(self, file_path: Path):
        """Process a new file and create an action item."""
        try:
            # Get file info
            stat = file_path.stat()
            file_size = stat.st_size
            file_ext = file_path.suffix.lower()

            # Determine priority based on file name
            priority = "Normal"
            if "urgent" in file_path.name.lower():
                priority = "High"
            elif "important" in file_path.name.lower():
                priority = "High"
            elif "critical" in file_path.name.lower():
                priority = "Critical"

            # Create action file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            action_filename = f"{timestamp}_inbox_{file_path.stem}.md"
            action_path = NEEDS_ACTION_PATH / action_filename

            # Read file content if it's text-based
            content_preview = ""
            text_extensions = ['.txt', '.md', '.py', '.js', '.json', '.csv', '.html', '.css']
            if file_ext in text_extensions and file_size < 100000:  # < 100KB
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        content_preview = ''.join(lines[:10])  # First 10 lines
                        if len(lines) > 10:
                            content_preview += f"\n... ({len(lines) - 10} more lines)"
                except Exception as e:
                    content_preview = f"[Error reading file: {e}]"

            # Create action file content
            action_content = f"""---
type: file_inbox
source: filesystem
priority: {priority}
status: pending
created: {datetime.now().isoformat()}
original_file: {str(file_path)}
file_size: {file_size} bytes
file_type: {file_ext}
---

# New File in Inbox: {file_path.name}

## File Information
- **Path:** `{file_path}`
- **Size:** {file_size} bytes
- **Type:** {file_ext or 'Unknown'}
- **Created:** {datetime.fromtimestamp(stat.st_ctime).isoformat()}

## Content Preview
```
{content_preview or "[Binary or large file - cannot preview]"}
```

## Suggested Actions
- [ ] Review file content
- [ ] Categorize and process
- [ ] Move to appropriate folder
- [ ] Update Dashboard

---

*Created by FileSystemWatcher at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""

            # Write action file
            action_path.parent.mkdir(parents=True, exist_ok=True)
            with open(action_path, 'w', encoding='utf-8') as f:
                f.write(action_content)

            logger.info(f"Created action file: {action_filename}")

            # Mark as processed
            self.processed_files.add(str(file_path))
            self._save_state()

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")


def ensure_directories():
    """Ensure all required directories exist."""
    for path in [INBOX_PATH, NEEDS_ACTION_PATH, DONE_PATH, IN_PROGRESS_PATH]:
        path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured directory exists: {path}")


def scan_existing_files():
    """Scan Inbox for existing files on startup."""
    logger.info("Scanning Inbox for existing files...")

    if not INBOX_PATH.exists():
        logger.warning(f"Inbox path does not exist: {INBOX_PATH}")
        return

    files = list(INBOX_PATH.glob("*"))
    files = [f for f in files if f.is_file()]

    logger.info(f"Found {len(files)} existing files in Inbox")

    for file_path in files:
        logger.info(f"Processing existing file: {file_path.name}")
        # Process will be handled by the watcher's on_created
        # But we need to manually trigger it for existing files
        handler = FileSystemWatcher()
        handler._process_file(file_path)


def main():
    """Main entry point for the file system watcher."""
    logger.info("="*60)
    logger.info("AI Employee - File System Watcher")
    logger.info("="*60)

    # Ensure directories exist
    ensure_directories()

    # Create the watcher
    event_handler = FileSystemWatcher()
    observer = Observer()

    # Watch the Inbox directory
    if INBOX_PATH.exists():
        observer.schedule(event_handler, str(INBOX_PATH), recursive=False)
        logger.info(f"Watching: {INBOX_PATH}")
    else:
        logger.error(f"Inbox directory does not exist: {INBOX_PATH}")
        logger.info("Creating Inbox directory...")
        INBOX_PATH.mkdir(parents=True, exist_ok=True)
        observer.schedule(event_handler, str(INBOX_PATH), recursive=False)

    # Start the observer
    observer.start()
    logger.info("File System Watcher is now running...")
    logger.info(f"Monitoring: {INBOX_PATH}")
    logger.info(f"Actions will be created in: {NEEDS_ACTION_PATH}")
    logger.info("Press Ctrl+C to stop")

    # Scan existing files on startup
    scan_existing_files()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down File System Watcher...")
        observer.stop()

    observer.join()
    logger.info("File System Watcher stopped")


if __name__ == "__main__":
    main()
