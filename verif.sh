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

# Run play.py to detect terminal_button.png or croix_button.png
echo "Running play.py..."
python3 play.py
PLAY_STATUS=$?

# If play.py fails, close all Firefox windows and restart start.sh
if [ $PLAY_STATUS -ne 0 ]; then
  echo "play.py failed! Closing all Firefox windows and restarting start.sh..."
  while wmctrl -l | grep -i "Mozilla Firefox" >/dev/null; do
      wmctrl -c "Mozilla Firefox"
      sleep 0.5
  done
  sleep 2
  echo "Restarting start.sh..."
  exit 1
fi

# Run stop.py to detect stop_button.png
echo "Running stop.py..."
python3 stop.py
STOP_STATUS=$?

# If stop.py fails, close all Firefox windows and restart start.sh
if [ $STOP_STATUS -ne 0 ]; then
  echo "stop.py failed! Closing all Firefox windows and restarting start.sh..."
  while wmctrl -l | grep -i "Mozilla Firefox" >/dev/null; do
      wmctrl -c "Mozilla Firefox"
      sleep 0.5
  done
  sleep 2
  echo "Restarting start.sh..."
  exit 1
fi

# If both play.py and stop.py succeed, proceed with remaining steps
echo "Both play.py and stop.py succeeded, proceeding with remaining steps..."

# Minimize Firefox window after finishing navigation
wmctrl -ir "$WINDOW_ID" -b add,hidden
echo "Tab navigation completed and Firefox minimized."
