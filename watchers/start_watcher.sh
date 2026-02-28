#!/bin/bash
# File System Watcher Startup Script for Unix/Linux/macOS

echo "===================================="
echo "AI Employee - File System Watcher"
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

# Start the watcher
echo
echo "Starting File System Watcher..."
echo "Monitoring: ../AI_Employee_Vault/Inbox"
echo "Press Ctrl+C to stop"
echo
python file_system_watcher.py
