#!/usr/bin/env python3
"""
Silver Tier Validation Script
Tests all Silver Tier components to verify they're working correctly.
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
VAULT_PATH = Path(__file__).parent.parent / "AI_Employee_Vault"
WATCHERS_PATH = Path(__file__).parent
MCP_SERVERS_PATH = Path(__file__).parent.parent / "mcp_servers"

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

    @classmethod
    def ok(cls, msg):
        print(f"{cls.GREEN}✓{cls.ENDC} {msg}")

    @classmethod
    def fail(cls, msg):
        print(f"{cls.RED}✗{cls.ENDC} {msg}")

    @classmethod
    def warn(cls, msg):
        print(f"{cls.YELLOW}⚠{cls.ENDC} {msg}")

    @classmethod
    def info(cls, msg):
        print(f"{cls.BLUE}ℹ{cls.ENDC}  {msg}")


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        Colors.ok(f"Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        Colors.fail(f"Python version: {version.major}.{version.minor}.{version.micro} (need 3.10+)")
        return False


def check_folder_structure():
    """Check vault folder structure."""
    print("\n" + "="*60)
    print("Checking Folder Structure...")
    print("="*60)

    required_folders = [
        'Inbox',
        'Needs_Action',
        'Done',
        'Plans',
        'Pending_Approval',
        'Pending_Approval/Email',
        'Pending_Approval/LinkedIn',
        'Ready_To_Send/Email',
        'Ready_To_Post/LinkedIn',
        'Rejected/Email',
        'Rejected/LinkedIn',
    ]

    all_exist = True
    for folder in required_folders:
        folder_path = VAULT_PATH / folder
        if folder_path.exists():
            Colors.ok(f"{folder}/")
        else:
            Colors.fail(f"{folder}/ (missing)")
            all_exist = False

    return all_exist


def check_watcher_scripts():
    """Check if watcher scripts exist."""
    print("\n" + "="*60)
    print("Checking Watcher Scripts...")
    print("="*60)

    scripts = [
        ('File System Watcher', 'file_system_watcher.py'),
        ('Gmail Watcher', 'gmail_watcher.py'),
        ('Task Scheduler', 'scheduler.py'),
        ('LinkedIn Poster', 'linkedin_poster.py'),
    ]

    all_exist = True
    for name, script in scripts:
        script_path = WATCHERS_PATH / script
        if script_path.exists():
            Colors.ok(f"{name} - {script}")
        else:
            Colors.fail(f"{name} - {script} (missing)")
            all_exist = False

    return all_exist


def check_dependencies():
    """Check if required packages are installed."""
    print("\n" + "="*60)
    print("Checking Python Dependencies...")
    print("="*60)

    required_packages = [
        'watchdog',
        'google',
        'yaml',
        'playwright',
    ]

    missing = []
    for package in required_packages:
        try:
            __import__(package)
            Colors.ok(f"{package}")
        except ImportError:
            Colors.fail(f"{package} (not installed)")
            missing.append(package)

    return len(missing) == 0


def check_gmail_setup():
    """Check Gmail credentials setup."""
    print("\n" + "="*60)
    print("Checking Gmail Setup...")
    print("="*60)

    credentials_file = WATCHERS_PATH / 'credentials.json'
    token_file = WATCHERS_PATH / 'token.json'

    if credentials_file.exists():
        Colors.ok("credentials.json found")
        credentials_ok = True
    else:
        Colors.warn("credentials.json not found (run: python gmail_watcher.py --auth)")
        credentials_ok = False

    if token_file.exists():
        Colors.ok("token.json found")
        token_ok = True
    else:
        Colors.warn("token.json not found (run: python gmail_watcher.py --auth)")
        token_ok = False

    return credentials_ok and token_ok


def check_email_sender_config():
    """Check Email Sender MCP configuration."""
    print("\n" + "="*60)
    print("Checking Email Sender Configuration...")
    print("="*60)

    env_file = MCP_SERVERS_PATH / 'email_sender' / '.env'

    if env_file.exists():
        Colors.ok(".env file exists")
        # Check if it has actual configuration
        with open(env_file, 'r') as f:
            content = f.read()
            if 'SMTP_PASSWORD=' in content and 'your_' not in content:
                Colors.ok("SMTP appears configured")
                return True
            else:
                Colors.warn("SMTP needs configuration (edit .env)")
                return False
    else:
        Colors.fail(".env file not found (copy .env.template to .env)")
        return False


def check_schedule_config():
    """Check schedule configuration."""
    print("\n" + "="*60)
    print("Checking Scheduler Configuration...")
    print("="*60)

    schedule_file = WATCHERS_PATH / 'schedule.yaml'

    if schedule_file.exists():
        Colors.ok("schedule.yaml found")
        return True
    else:
        Colors.fail("schedule.yaml not found")
        return False


def create_test_file():
    """Create a test file to verify watcher works."""
    print("\n" + "="*60)
    print("Creating Test File...")
    print("="*60)

    inbox_path = VAULT_PATH / 'Inbox'
    test_file = inbox_path / f"validation_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    try:
        test_file.write_text("This is a validation test file for Silver Tier.")
        Colors.ok(f"Test file created: {test_file.name}")
        return True
    except Exception as e:
        Colors.fail(f"Failed to create test file: {e}")
        return False


def run_tests():
    """Run all validation tests."""
    print("\n" + "="*60)
    print(f"SILVER TIER VALIDATION")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

    results = {
        'Python Version': check_python_version(),
        'Folder Structure': check_folder_structure(),
        'Watcher Scripts': check_watcher_scripts(),
        'Dependencies': check_dependencies(),
        'Gmail Setup': check_gmail_setup(),
        'Email Config': check_email_sender_config(),
        'Schedule Config': check_schedule_config(),
        'Test File': create_test_file(),
    }

    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test, result in results.items():
        if result:
            Colors.ok(f"{test}")
        else:
            Colors.fail(f"{test}")

    print(f"\n{Colors.GREEN if passed == total else Colors.YELLOW}Passed: {passed}/{total}{Colors.ENDC}")

    if passed == total:
        print("\n🎉 All validation checks passed!")
        print("\nSilver Tier is ready for configuration.")
        print("\nNext steps:")
        print("1. Read: SILVER_TIER_SETUP.md")
        print("2. Set up Google Cloud Console & Gmail OAuth")
        print("3. Configure SMTP in .env")
        print("4. Install cron/Task Scheduler jobs")
        print("5. Test end-to-end workflow")
        return True
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
