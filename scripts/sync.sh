#!/bin/bash
# 🤖 AI Agent Shared Repo Sync & Notification Script for macOS
# This script pulls updates from the shared repo, checks for new messages, and notifies you.

REPO_DIR="/Users/tedchanglimchangsik/초보프로젝트/hermes-ag-shared"
to_ag_file="$REPO_DIR/to-ag.md"

cd "$REPO_DIR" || exit 1

# Get the MD5 hash of to-ag.md before pulling
if [ -f "$to_ag_file" ]; then
    PREV_HASH=$(md5 -q "$to_ag_file")
else
    PREV_HASH=""
fi

# Pull the latest changes
echo "🔄 Checking for updates from GitHub..."
git pull origin main --quiet

# Get the MD5 hash of to-ag.md after pulling
if [ -f "$to_ag_file" ]; then
    NEW_HASH=$(md5 -q "$to_ag_file")
else
    NEW_HASH=""
fi

# Compare hashes to see if Hena sent a new message
if [ "$PREV_HASH" != "$NEW_HASH" ]; then
    echo "🔔 New message received from Hena!"
    # Display macOS Native Notification
    osascript -e 'display notification "Hena has sent a new message! Check to-ag.md" with title "🤖 META AI LABS" subtitle "New Message Received"'
    
    # Optional: print the content to stdout
    echo "----------------------------------------"
    cat "$to_ag_file"
    echo "----------------------------------------"
else
    echo "✅ Up to date. No new messages."
fi
