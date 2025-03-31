import pyautogui
import time
import subprocess
import sys
import signal
import os

# Start time tracking
start_time = time.time()

# List to track subprocesses
subprocesses = []

# Timeout handler
def timeout_handler(signum, frame):
    print("croix.py reached 135-second timeout. Terminating subprocesses and exiting...")
    for proc in subprocesses:
        try:
            os.kill(proc.pid, signal.SIGKILL)
            print(f"Terminated subprocess PID {proc.pid}")
        except OSError:
            pass
    sys.exit(1)

# Set up the timeout alarm
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(135)

def detect_web_button(script_name):
    """Run an external script to detect the web button and keep trying until successful."""
    global subprocesses
    while True:
        elapsed = time.time() - start_time
        if elapsed >= 135:
            print("croix.py reached 135-second timeout. Exiting...")
            for proc in subprocesses:
                try:
                    os.kill(proc.pid, signal.SIGKILL)
                    print(f"Terminated subprocess PID {proc.pid}")
                except OSError:
                    pass
            sys.exit(1)

        # Start the external detection script
        process = subprocess.Popen(['python3', script_name])
        subprocesses.append(process)
        try:
            process.wait()
        except KeyboardInterrupt:
            os.kill(process.pid, signal.SIGKILL)
            raise

        if process.returncode == 0:
            print(f"Web button detected and clicked by {script_name}. Proceeding with tasks...")
            subprocesses.remove(process)  # Remove completed process
            return
        else:
            print(f"Web button not detected by {script_name}. Retrying...")
            subprocesses.remove(process)  # Remove failed process
            time.sleep(2)

def perform_additional_tasks():
    elapsed = time.time() - start_time
    if elapsed >= 135:
        print("croix.py reached 135-second timeout. Exiting...")
        for proc in subprocesses:
            try:
                os.kill(proc.pid, signal.SIGKILL)
                print(f"Terminated subprocess PID {proc.pid}")
            except OSError:
                pass
        sys.exit(1)
    print("Performing additional tasks...")
    time.sleep(1.5)
    print("All tasks completed.")

if __name__ == "__main__":
    try:
        detect_web_button('croix-found.py')
        perform_additional_tasks()
        signal.alarm(0)
        sys.exit(0)
    except Exception as e:
        print(f"Error in croix.py: {e}")
        for proc in subprocesses:
            try:
                os.kill(proc.pid, signal.SIGKILL)
                print(f"Terminated subprocess PID {proc.pid}")
            except OSError:
                pass
        signal.alarm(0)
        sys.exit(1)
