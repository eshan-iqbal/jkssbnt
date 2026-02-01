#!/bin/bash

# Setup Local Cron Job for JKSSB Monitor
# Runs twice daily at 9 AM and 9 PM

echo "⏰ Setting up Cron Job for JKSSB Monitor"
echo "========================================"
echo ""

# Get absolute path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python"
MONITOR_SCRIPT="$SCRIPT_DIR/monitor.py"
LOG_FILE="$SCRIPT_DIR/logs/cron.log"

echo "📂 Script directory: $SCRIPT_DIR"
echo "🐍 Python path: $PYTHON_PATH"
echo "📝 Monitor script: $MONITOR_SCRIPT"
echo "📋 Log file: $LOG_FILE"
echo ""

# Create cron job entry
CRON_JOB="0 9,21 * * * cd $SCRIPT_DIR && $PYTHON_PATH $MONITOR_SCRIPT >> $LOG_FILE 2>&1"

echo "📅 Cron schedule: Twice daily at 9 AM and 9 PM"
echo ""
echo "Cron job to be added:"
echo "$CRON_JOB"
echo ""

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "jkssb-monitor"; then
    echo "⚠️  Cron job already exists. Updating..."
    # Remove old entry
    crontab -l | grep -v "jkssb-monitor" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "# JKSSB Monitor - Runs at 9 AM and 9 PM daily"; echo "$CRON_JOB") | crontab -

echo "✅ Cron job added successfully!"
echo ""
echo "📊 Current crontab:"
crontab -l | grep -A1 "JKSSB"
echo ""
echo "========================================"
echo "✅ Setup Complete!"
echo "========================================"
echo ""
echo "Your monitor will now run automatically:"
echo "  • 9:00 AM daily"
echo "  • 9:00 PM daily"
echo ""
echo "📝 View logs:"
echo "  tail -f $LOG_FILE"
echo ""
echo "🔍 List cron jobs:"
echo "  crontab -l"
echo ""
echo "❌ Remove cron job:"
echo "  crontab -e  # Then delete the JKSSB Monitor lines"
echo ""
echo "🎉 You're all set!"
echo ""
