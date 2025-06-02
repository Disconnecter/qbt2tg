#!/bin/bash

set -e

echo "== qbt2tg setup script =="

# 1. Find or install python3 via brew
if ! which python3 > /dev/null; then
    echo "python3 not found, installing via Homebrew..."
    brew install python
fi

PYTHON_BIN="$(which python3)"

echo "Using python: $PYTHON_BIN"
echo

# 2. Create virtualenv
if [ ! -d "venv" ]; then
    echo "Creating virtualenv in ./venv"
    $PYTHON_BIN -m venv venv
fi

# 3. Activate virtualenv and install dependencies
echo "Activating virtualenv and installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install python-telegram-bot qbittorrent-api apscheduler

deactivate

# 4. Get absolute path for project dir and user
PROJECT_DIR="$(cd "$(dirname "$0")"; pwd)"
PYTHON_VENV="$PROJECT_DIR/venv/bin/python"
USER_NAME=$(whoami)
PLIST_NAME="com.${USER_NAME}.qbt2tg.plist"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME"

echo "Project directory: $PROJECT_DIR"
echo "Virtualenv python: $PYTHON_VENV"
echo "Plist will be generated as: $PLIST_PATH"
echo

# 5. Generate launchd plist
cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.${USER_NAME}.qbt2tg</string>

    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_VENV}</string>
        <string>${PROJECT_DIR}/bot.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>${PROJECT_DIR}</string>

    <key>StandardOutPath</key>
    <string>${PROJECT_DIR}/bot.out.log</string>
    <key>StandardErrorPath</key>
    <string>${PROJECT_DIR}/bot.err.log</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PYTHONUNBUFFERED</key>
        <string>1</string>
    </dict>

    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
EOF

echo "launchd plist created at $PLIST_PATH"
plutil "$PLIST_PATH"

# 6. Load the service
echo "Unloading any old service..."
launchctl unload "$PLIST_PATH" || true

echo "Loading bot as service..."
launchctl load "$PLIST_PATH"

echo "Bot should now run as a service. To check logs:"
echo "  tail -f $PROJECT_DIR/bot.out.log"
echo "  tail -f $PROJECT_DIR/bot.err.log"

echo "To restart: launchctl unload $PLIST_PATH && launchctl load $PLIST_PATH"

echo "Done!"