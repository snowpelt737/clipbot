#!/bin/bash

BASE_DIR="$(dirname "$0")"
SETTINGS="$BASE_DIR/settings.json"
CODE="$BASE_DIR/code"
LOGFILE="$BASE_DIR/clipbot.log"

# Read settings
AUTO_LOGS=$(jq -r '.auto_logs' "$SETTINGS")
CHECK_UPDATES=$(jq -r '.check_updates' "$SETTINGS")
STARTUP_SUPER=$(jq -r '.startup_superfriendly' "$SETTINGS")

# Auto-logs
if [ "$AUTO_LOGS" = "true" ]; then
    echo "[$(date)] Launcher opened" >> "$LOGFILE"
fi

# Menu
choice=$(zenity --list \
    --title="ClipBot Launcher" \
    --column="Action" \
    "Run ClipBot" \
    "Zip ClipBot Folder" \
    "Settings" \
    "Check for Updates" \
    "Exit")

case "$choice" in

    "Run ClipBot")
        if [ "$STARTUP_SUPER" = "true" ]; then
            python3 "$CODE/main.py" --superfriendly
        else
            python3 "$CODE/main.py"
        fi
        ;;

    "Zip ClipBot Folder")
        bash "$BASE_DIR/gui_zip.sh"
        ;;

    "Settings")
        bash "$BASE_DIR/edit_settings.sh"
        ;;

    "Check for Updates")
        if [ "$CHECK_UPDATES" = "true" ]; then
            bash "$BASE_DIR/check_updates.sh"
        else
            zenity --info --text="Update checking is disabled in settings."
        fi
        ;;

    "Exit")
        exit 0
        ;;
esac
