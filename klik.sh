#!/bin/bash

# Check if xdotool is installed
if ! command -v xdotool &> /dev/null; then
    echo "xdotool not found. Installing..."
    sudo apt update && sudo apt install -y xdotool
fi

# Wait for 2 seconds
sleep 2

# Click at (20, 627)
xdotool mousemove 20 627 click 1

# Wait for 1 second
sleep 1

# Click at (84, 443)
xdotool mousemove 84 443 click 1

# Wait for 1 second
sleep 1

# Click at (243, 442)
xdotool mousemove 243 442 click 1

# Wait for 1.5 seconds
sleep 1.5
