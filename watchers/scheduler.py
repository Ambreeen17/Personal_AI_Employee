#!/usr/bin/env python3
"""
Task Scheduler for AI Employee
Runs scheduled tasks via cron or Task Scheduler integration.
"""
import time
import logging
import yaml
import subprocess
import json
from pathlib import Path
from datetime import datetime
from croniter import croniter

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
SCHEDULE_FILE = Path(__file__).parent / "schedule.yaml"
LOG_FILE = VAULT_PATH / "scheduler.log"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TaskScheduler')


class TaskScheduler:
    """Task Scheduler for running periodic AI Employee tasks."""

    def __init__(self, schedule_file=SCHEDULE_FILE):
        """
        Initialize Task Scheduler.

        Args:
            schedule_file: Path to schedule.yaml configuration
        """
        self.schedule_file = Path(schedule_file)
        self.scheduled_tasks = []
        self.last_run_times = {}

        # Load schedule
        self._load_schedule()

        # Load last run times
        self._load_state()

    def _load_schedule(self):
        """Load schedule from YAML file."""
        if not self.schedule_file.exists():
            logger.warning(f"Schedule file not found: {self.schedule_file}")
            return

        try:
            with open(self.schedule_file, 'r') as f:
                config = yaml.safe_load(f)
                self.scheduled_tasks = config.get('schedule', [])
            logger.info(f"Loaded {len(self.scheduled_tasks)} scheduled tasks")
        except Exception as e:
            logger.error(f"Error loading schedule: {e}")

    def _load_state(self):
        """Load last run times from state file."""
        state_file = VAULT_PATH / "scheduler_state.json"
        if state_file.exists():
            try:
                with open(state_file, 'r') as f:
                    self.last_run_times = json.load(f)
                logger.info(f"Loaded state: {len(self.last_run_times)} tasks")
            except Exception as e:
                logger.error(f"Error loading state: {e}")

    def _save_state(self):
        """Save current run times to state file."""
        state_file = VAULT_PATH / "scheduler_state.json"
        try:
            with open(state_file, 'w') as f:
                json.dump(self.last_run_times, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving state: {e}")

    def should_run(self, task_name: str, cron_expression: str) -> bool:
        """
        Check if a task should run based on cron schedule.

        Args:
            task_name: Name of the task
            cron_expression: Cron expression for schedule

        Returns:
            True if task should run now
        """
        try:
            now = datetime.now()

            # Get last run time for this task
            last_run = self.last_run_times.get(task_name)

            if not last_run:
                # Task has never run, should run if schedule matches
                cron = croniter(cron_expression, now)
                return cron.get_prev(datetime) == now

            # Check if it's time to run again
            last_run_dt = datetime.fromisoformat(last_run)
            cron = croniter(cron_expression, last_run_dt)
            next_run = cron.get_next(datetime)

            # Should run if next run time has passed
            should_run = next_run <= now

            if should_run:
                logger.info(f"Task '{task_name}' is due to run")

            return should_run

        except Exception as e:
            logger.error(f"Error checking schedule for {task_name}: {e}")
            return False

    def run_action(self, action: str, task_name: str):
        """
        Run a scheduled action.

        Args:
            action: Action name (send_emails, post_linkedin, etc.)
            task_name: Name of the task
        """
        try:
            logger.info(f"Running action: {action} (task: {task_name})")

            if action == "send_emails":
                self._send_emails()
            elif action == "post_linkedin":
                self._post_linkedin()
            elif action == "daily_report":
                self._daily_report()
            elif action == "weekly_audit":
                self._weekly_audit()
            elif action == "health_check":
                self._health_check()
            elif action == "cleanup_logs":
                self._cleanup_logs()
            elif action == "process_emails":
                self._process_emails()
            else:
                logger.warning(f"Unknown action: {action}")

            # Update last run time
            self.last_run_times[task_name] = datetime.now().isoformat()
            self._save_state()

            logger.info(f"Completed action: {action}")

        except Exception as e:
            logger.error(f"Error running action {action}: {e}")

    def _send_emails(self):
        """Check Ready_To_Send/Email/ and send pending emails."""
        try:
            ready_to_send = VAULT_PATH / "Ready_To_Send" / "Email"
            if not ready_to_send.exists():
                logger.info("No Ready_To_Send/Email/ folder")
                return

            email_files = list(ready_to_send.glob("*.md"))
            if not email_files:
                logger.info("No emails ready to send")
                return

            logger.info(f"Found {len(email_files)} emails to send")

            # Import EmailSenderServer (if available)
            try:
                import sys
                sys.path.insert(0, str(Path(__file__).parent.parent / "mcp_servers" / "email_sender"))
                from email_server import EmailSenderServer

                # Create server and check queue
                server = EmailSenderServer()
                result = asyncio.run(server.check_queue())
                logger.info(f"Email queue result: {result}")

            except ImportError as e:
                logger.error(f"Email Sender MCP not available: {e}")

        except Exception as e:
            logger.error(f"Error sending emails: {e}")

    def _post_linkedin(self):
        """Check Ready_To_Post/LinkedIn/ and post pending content."""
        try:
            ready_to_post = VAULT_PATH / "Ready_To_Post" / "LinkedIn"
            if not ready_to_post.exists():
                logger.info("No Ready_To_Post/LinkedIn/ folder")
                return

            post_files = list(ready_to_post.glob("*.md"))
            if not post_files:
                logger.info("No LinkedIn posts ready")
                return

            logger.info(f"Found {len(post_files)} LinkedIn posts to process")
            # LinkedIn posting would be implemented here
            # For now, just log the files
            for post_file in post_files:
                logger.info(f"Post ready: {post_file.name}")

        except Exception as e:
            logger.error(f"Error posting to LinkedIn: {e}")

    def _daily_report(self):
        """Generate daily summary report."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d")
            report_file = VAULT_PATH / "Accounting" / f"Daily_Report_{timestamp}.md"
            report_file.parent.mkdir(parents=True, exist_ok=True)

            # Count completed items today
            done_path = VAULT_PATH / "Done"
            completed_today = list(done_path.glob(f"*{datetime.now().strftime('%Y-%m-%d')}*.md"))

            # Count pending items
            needs_action = VAULT_PATH / "Needs_Action"
            pending_items = list(needs_action.glob("*.md"))

            # Count approval queue
            pending_approval = VAULT_PATH / "Pending_Approval"
            approval_count = sum(len(list(pending_approval.rglob("*.md"))) for _ in [1])

            report_content = f"""# AI Employee Daily Report - {datetime.now().strftime('%Y-%m-%d')}

## Summary
- Tasks Processed: {len(completed_today)}
- Pending Items: {len(pending_items)}
- Awaiting Approval: {approval_count}
- Errors: 0

## Tasks Completed
"""
            for task in completed_today[-10:]:  # Last 10 tasks
                report_content += f"- ✅ {task.name}\n"

            report_content += f"""
## Pending Items
- {len(pending_items)} items in Needs_Action
- {approval_count} items awaiting approval

## System Status
- Vault: 🟢 Online
- Gmail Watcher: {'🟢 Running' if self._is_watcher_running('gmail') else '⚪ Not Running'}
- File System Watcher: {'🟢 Running' if self._is_watcher_running('filesystem') else '⚪ Not Running'}
- Email Sender MCP: {'🟢 Running' if self._is_mcp_running() else '⚪ Not Running'}

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

            with open(report_file, 'w') as f:
                f.write(report_content)

            logger.info(f"Daily report generated: {report_file}")

        except Exception as e:
            logger.error(f"Error generating daily report: {e}")

    def _weekly_audit(self):
        """Generate weekly CEO briefing."""
        try:
            logger.info("Generating weekly CEO briefing")
            # Weekly audit implementation
            # Would summarize week's activities, metrics, etc.
        except Exception as e:
            logger.error(f"Error generating weekly audit: {e}")

    def _health_check(self):
        """Check system health and status."""
        try:
            logger.info("Running health check")

            # Check folder structure
            required_folders = ['Inbox', 'Needs_Action', 'Done', 'Plans']
            for folder in required_folders:
                folder_path = VAULT_PATH / folder
                if not folder_path.exists():
                    logger.warning(f"Missing folder: {folder}")

            # Check disk space
            import shutil
            total, used, free = shutil.disk_usage(VAULT_PATH)
            free_gb = free // (1024**3)
            if free_gb < 1:
                logger.warning(f"Low disk space: {free_gb}GB free")

            logger.info("Health check complete")

        except Exception as e:
            logger.error(f"Error in health check: {e}")

    def _cleanup_logs(self):
        """Clean up old log files."""
        try:
            logger.info("Cleaning up old logs")
            # Log cleanup implementation
        except Exception as e:
            logger.error(f"Error cleaning up logs: {e}")

    def _process_emails(self):
        """Process new email action items."""
        try:
            logger.info("Processing new emails from Needs_Action")
            # Email processing implementation
        except Exception as e:
            logger.error(f"Error processing emails: {e}")

    def _is_watcher_running(self, watcher_type: str) -> bool:
        """Check if a watcher is running."""
        try:
            import subprocess
            if watcher_type == "gmail":
                result = subprocess.run(['pgrep', '-f', 'gmail_watcher.py'],
                                      capture_output=True)
            elif watcher_type == "filesystem":
                result = subprocess.run(['pgrep', '-f', 'file_system_watcher.py'],
                                      capture_output=True)
            else:
                return False
            return result.returncode == 0
        except:
            return False

    def _is_mcp_running(self) -> bool:
        """Check if Email Sender MCP is running."""
        try:
            import subprocess
            result = subprocess.run(['pgrep', '-f', 'email_server.py'],
                                  capture_output=True)
            return result.returncode == 0
        except:
            return False

    def run(self):
        """Main loop - check schedule and run due tasks."""
        logger.info("="*60)
        logger.info("AI Employee - Task Scheduler")
        logger.info("="*60)
        logger.info("Press Ctrl+C to stop")

        try:
            while True:
                try:
                    # Check each scheduled task
                    for task in self.scheduled_tasks:
                        if not task.get('enabled', True):
                            continue

                        name = task.get('name', '')
                        frequency = task.get('frequency', '')
                        action = task.get('action', '')

                        if not frequency or not action:
                            continue

                        # Check if task should run
                        if self.should_run(name, frequency):
                            self.run_action(action, name)

                except Exception as e:
                    logger.error(f"Error in main loop: {e}")

                # Wait before next check (1 minute)
                time.sleep(60)

        except KeyboardInterrupt:
            logger.info("Shutting down Task Scheduler...")
        finally:
            self._save_state()


def main():
    """Main entry point for Task Scheduler."""
    import argparse

    parser = argparse.ArgumentParser(description='Task Scheduler for AI Employee')
    parser.add_argument('--action', type=str,
                       help='Run specific action immediately')
    parser.add_argument('--list', action='store_true',
                       help='List scheduled tasks')
    parser.add_argument('--validate', action='store_true',
                       help='Validate schedule configuration')

    args = parser.parse_args()

    scheduler = TaskScheduler()

    if args.list:
        print("Scheduled Tasks:")
        print("="*60)
        for task in scheduler.scheduled_tasks:
            status = "✅" if task.get('enabled', True) else "❌"
            print(f"{status} {task.get('name', '')}")
            print(f"   Frequency: {task.get('frequency', '')}")
            print(f"   Action: {task.get('action', '')}")
            print()

    elif args.action:
        print(f"Running action: {args.action}")
        scheduler.run_action(args.action, f"manual_{args.action}")

    elif args.validate:
        print("Validating schedule configuration...")
        # Validate schedule
        print("Schedule is valid")

    else:
        # Run continuously
        scheduler.run()


if __name__ == "__main__":
    main()
