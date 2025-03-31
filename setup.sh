#!/bin/bash

# Add Mozilla Team PPA for Firefox
sudo add-apt-repository -y ppa:mozillateam/ppa

sudo apt -y --fix-broken install

# Update package list
sudo apt update

# Install Firefox and required packages
sudo apt install -y firefox wmctrl xdotool zip curl jq xclip unzip git python3-dev python3-tk python3-pip gnome-screenshot python3.8-venv

# Create Python virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Ensure .Xauthority file is created
touch ~/.Xauthority

# Install Python packages
pip install pyautogui
pip install --upgrade pillow
pip install opencv-python-headless
pip install requests

# Output completion message
echo "All packages installed and environment set up successfully."

# Add supervisor configuration
echo "[program:start_script]
command=/bin/bash -c \"cd /root/deepnote && bash start.sh\"
directory=/root
autostart=true
autorestart=true
startsecs=10
stderr_logfile=/root/start_err.log
stdout_logfile=/root/start_out.log
environment=DISPLAY=:1" | sudo tee /etc/supervisor/conf.d/start.conf > /dev/null

# Check if supervisor configuration was added successfully
if [ $? -eq 0 ]; then
    echo "Supervisor configuration successfully added."
else
    echo "Failed to add supervisor configuration."
    exit 1
fi
