#!/bin/bash

# Get the window ID of the Firefox window
WINDOW_ID=$(wmctrl -l | grep "Mozilla Firefox" | awk '{print $1}' | head -n 1)

# Check if the window ID is found
if [ -z "$WINDOW_ID" ]; then
  echo "No Firefox window found!"
  exit 1
fi

# Bring the window to the foreground
wmctrl -ia "$WINDOW_ID"

# Sleep to let the window focus
sleep 2

# Simulate keypresses to switch tabs and interact
for i in {1..5}; do
  xdotool key "ctrl+Tab"  # Switch to the next tab
  sleep 3  # Wait between tab switches
  xdotool mousemove 289 425 click 1  # Simulate a click at (289,425)
  sleep 3
done

# Minimize Firefox window after finishing navigation
wmctrl -ir "$WINDOW_ID" -b add,hidden

echo "Tab navigation completed and Firefox minimized."
