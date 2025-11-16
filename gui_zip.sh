#!/bin/bash

# Ask user
zenity --question --title="ClipBot Zipper" --text="Create clipbot.zip?" 
if [ $? != 0 ]; then
    exit 0
fi

# Run Python
OUTPUT=$(python3 zip_clipbot.py 2>&1)
STATUS=$?

# Success
if [ $STATUS -eq 0 ]; then
    zenity --info --title="Success!" --text="clipbot.zip created successfully!"
else
    zenity --error --title="Error" --text="Something went wrong:\n\n$OUTPUT"
fi
