#!/bin/bash
# Gmail Watcher Startup Script for Unix/Linux/macOS

echo "===================================="
echo "AI Employee - Gmail Watcher"
echo "===================================="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet

# Check if credentials exist
if [ ! -f "credentials.json" ]; then
    echo
    echo "========================================"
    echo "Gmail Setup Required"
    echo "========================================"
    echo
    echo "Please follow these steps to set up Gmail API:"
    echo
    echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
    echo "2. Create a new project or select existing"
    echo "3. Enable Gmail API"
    echo "4. Create OAuth 2.0 credentials (Desktop app)"
    echo "5. Download credentials.json and place in this directory"
    echo
    echo "See: .claude/skills/gmail-watcher/SKILL.md for detailed instructions"
    echo
    read -p "Press Enter when credentials.json is in place..."
fi

# Start the watcher
echo
echo "Starting Gmail Watcher..."
echo "Monitoring for unread emails..."
echo "Press Ctrl+C to stop"
echo
python gmail_watcher.py
