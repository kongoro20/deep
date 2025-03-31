import pyautogui
import time
import subprocess
import sys
import signal

# Start time tracking
start_time = time.time()

# Timeout handler
def timeout_handler(signum, frame):
    print("run.py reached 135-second timeout. Exiting with failure...")
    sys.exit(1)

# Set up the timeout alarm
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(135)  # Set alarm for 135 seconds

def detect_web_button(script_name):
    """Run an external script to detect the web button and keep trying until successful."""
    while True:
        elapsed = time.time() - start_time
        if elapsed >= 135:
            print("run.py reached 135-second timeout. Exiting...")
            sys.exit(1)

        # Start the external detection script
        process = subprocess.Popen(['python3', script_name])
        process.wait()  # Wait for it to finish

        if process.returncode == 0:  # Success code indicates the button was found
            print(f"Web button detected and clicked by {script_name}. Proceeding with tasks...")
            return  # Exit the loop and proceed to next tasks
        else:
            print(f"Web button not detected by {script_name}. Retrying...")
            time.sleep(2)

def perform_additional_tasks():
    """Define tasks to perform after the web button is detected."""
    elapsed = time.time() - start_time
    if elapsed >= 135:
        print("run.py reached 135-second timeout. Exiting...")
        sys.exit(1)
    print("Performing additional tasks...")
    time.sleep(2)
    print("All tasks completed.")

if __name__ == "__main__":
    try:
        # Step 1: Detect the web button via the detection script
        detect_web_button('detector4.py')

        # Step 2: Perform additional tasks after the web button is detected
        perform_additional_tasks()

        signal.alarm(0)  # Cancel the alarm on success
        sys.exit(0)

    except Exception as e:
        print(f"Error in run.py: {e}")
        signal.alarm(0)
        sys.exit(1)
