#!/bin/bash

SETTINGS_FILE="$(dirname "$0")/settings.json"

# Load current settings
AUTO_LOGS=$(jq -r '.auto_logs' "$SETTINGS_FILE")
CHECK_UPDATES=$(jq -r '.check_updates' "$SETTINGS_FILE")
STARTUP_SUPER=$(jq -r '.startup_superfriendly' "$SETTINGS_FILE")

CHOICE=$(zenity --list \
    --title="ClipBot Settings" \
    --checklist \
    --column="Enabled" --column="Setting" \
    $( [ "$AUTO_LOGS" = "true" ] && echo TRUE || echo FALSE ) "Auto Logs" \
    $( [ "$CHECK_UPDATES" = "true" ] && echo TRUE || echo FALSE ) "Check for Updates" \
    $( [ "$STARTUP_SUPER" = "true" ] && echo TRUE || echo FALSE ) "Start in Super Friendly Mode" \
)

# Update JSON
echo "$CHOICE" | grep -q "Auto Logs"
AUTO=$?
echo "$CHOICE" | grep -q "Check for Updates"
UPD=$?
echo "$CHOICE" | grep -q "Start in Super Friendly Mode"
SUPER=$?

cat <<EOF > "$SETTINGS_FILE"
{
  "auto_logs": $( [ $AUTO -eq 0 ] && echo true || echo false ),
  "check_updates": $( [ $UPD -eq 0 ] && echo true || echo false ),
  "startup_superfriendly": $( [ $SUPER -eq 0 ] && echo true || echo false )
}
EOF
