#!/bin/bash

LOCAL_VERSION=$(cat "$(dirname "$0")/version.txt")
REMOTE_VERSION=$(curl -s https://raw.githubusercontent.com/snowpelt737/clipbot/main/version.txt)

if [ "$LOCAL_VERSION" != "$REMOTE_VERSION" ]; then
    zenity --info --title="Update Available" \
        --text="A new ClipBot version is available!\nLocal: $LOCAL_VERSION\nRemote: $REMOTE_VERSION"
else
    zenity --info --title="Up To Date" \
        --text="You're using the latest version of ClipBot!"
fi
