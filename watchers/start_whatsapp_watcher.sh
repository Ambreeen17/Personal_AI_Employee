#!/bin/bash
# WhatsApp Watcher Startup Script (Unix/Linux/macOS)
# This script starts the WhatsApp Watcher to monitor for urgent messages

echo "Starting WhatsApp Watcher..."
echo ""

# Change to the watchers directory
cd "$(dirname "$0")"

# Run the WhatsApp Watcher
python whatsapp_watcher.py ../AI_Employee_Vault
