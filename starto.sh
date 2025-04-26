#!/bin/bash

# New Step: Keep running request.py every 5 seconds until it fails
echo "Starting initial server check loop (request.py every 5 seconds)..."
while true; do
    echo "Running request.py..."
    python3 request.py
    if [ $? -ne 0 ]; then
        echo "request.py failed. Proceeding to main execution..."
        break
    fi
    sleep 5
done

# Start Xvfb if it's not already running
if ! pgrep -x "Xvfb" > /dev/null; then
    echo "Starting Xvfb..."
    Xvfb :1 -screen 0 1366x641x16 &
    sleep 2
fi

# Activate the environment and set necessary variables
sleep 1
source /root/deep/myenv/bin/activate  # Explicit path to myenv
export DISPLAY=:1  # Ensures Firefox uses the correct display

# Wait for Xvfb to initialize
sleep 2

# Cleanup function to close Firefox windows and terminate Python scripts from /root/deepnote
cleanup_and_restart() {
    echo "Failure detected. Closing Firefox windows and restarting..."
    sleep 2
    while wmctrl -l | grep -i "Mozilla Firefox" >/dev/null; do
        wmctrl -c "Mozilla Firefox"
        sleep 0.5
    done

    echo "Current Python processes before cleanup:"
    ps aux | grep "[p]ython3" || echo "No python3 processes found"

    echo "Terminating Python scripts from current directory and their children..."
    # List of all Python scripts in current directory (/root/deepnote)
    scripts="bypass.py clikterminal.py croix-found.py croix.py detector1.py detector2.py detector3.py detector4.py download.py found.py klik.py module.py module1.py pip.py pip1.py play.py request.py run.py start.py stop.py stop_detection_button.py terminal.py upload.py"

    # Target each script by name, filtering out system paths
    for script in $scripts; do
        # Find PIDs first, excluding system paths, then kill them
        pids=$(ps aux | grep "[p]ython3.*${script}" | grep -v "/usr/bin/\|/usr/local/" | awk '{print $2}')
        if [ -n "$pids" ]; then
            for pid in $pids; do
                echo "Killing process tree for ${script} (PID $pid)..."
                kill -9 $pid 2>/dev/null      # Kill parent
                pkill -9 -P $pid 2>/dev/null  # Kill children
            done
        fi
    done

    echo "Remaining Python processes after cleanup:"
    ps aux | grep "[p]ython3" || echo "No python3 processes found"

    sleep 2
    echo "Exiting and restarting start.sh..."
    exec bash "$0"
}

# Function to terminate request.py if running
terminate_request_py() {
    if [ -n "$REQUEST_PID" ] && ps -p $REQUEST_PID > /dev/null; then
        echo "Terminating request.py (PID $REQUEST_PID)..."
        kill $REQUEST_PID 2>/dev/null
        sleep 0.1
        if ps -p $REQUEST_PID > /dev/null; then
            kill -9 $REQUEST_PID 2>/dev/null
            echo "request.py (PID $REQUEST_PID) force-killed"
        else
            echo "request.py (PID $REQUEST_PID) killed"
        fi
    fi
}

while true; do
    echo "Running gofile.sh..."
    bash gofile1.sh

    # Wait for 8 seconds
    sleep 8

    # Run download.py
    echo "Running download.py..."
    python3 download.py
    if [ $? -ne 0 ]; then
        echo "download.py failed or timed out."
        terminate_request_py
        cleanup_and_restart
    fi

    # Wait for 2 seconds
    sleep 2

    # Unlimited iteration loop
    echo "Starting refresh.sh loop (unlimited)..."
    while true; do
        echo "Running refresh.sh..."
        bash refresh.sh
        sleep 3
        echo "Running verif.sh..."
        bash verif.sh
        if [ $? -ne 0 ]; then
            echo "verif.sh failed."
            terminate_request_py
            cleanup_and_restart
        fi

        # Run request.py synchronously first
        echo "Running request.py to verify servers..."
        python3 request.py
        if [ $? -ne 0 ]; then
            echo "request.py failed."
            terminate_request_py
            cleanup_and_restart
        fi

        echo "Iteration completed successfully!"
        echo "Starting request.py in background for 300 seconds..."
        rm -f /tmp/request_failure
        python3 request.py continuous &
        REQUEST_PID=$!
        echo "request.py PID: $REQUEST_PID"

        # Sleep for 300 seconds, checking for failure signal
        for ((i=0; i<150; i++)); do
            sleep 1
            if [ -f /tmp/request_failure ]; then
                kill $REQUEST_PID 2>/dev/null
                sleep 0.1
                if ps -p $REQUEST_PID > /dev/null; then
                    kill -9 $REQUEST_PID 2>/dev/null
                fi
                rm -f /tmp/request_failure
                echo "request.py (PID $REQUEST_PID) killed due to failure"
                cleanup_and_restart
            fi
        done

        # Kill the background request.py process if still running
        if ps -p $REQUEST_PID > /dev/null; then
            kill $REQUEST_PID 2>/dev/null
            sleep 0.1
            if ps -p $REQUEST_PID > /dev/null; then
                kill -9 $REQUEST_PID 2>/dev/null
                echo "request.py (PID $REQUEST_PID) force-killed after 300 seconds"
            else
                echo "request.py (PID $REQUEST_PID) killed after 300 seconds"
            fi
        else
            echo "request.py (PID $REQUEST_PID) already finished or killed"
        fi
        REQUEST_PID=""
    done
done
