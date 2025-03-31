import pyautogui
import time
import subprocess
import sys
import signal

# Start time tracking
start_time = time.time()

# Timeout handler
def timeout_handler(signum, frame):
    print("start.py reached 135-second timeout. Exiting with failure...")
    sys.exit(1)

# Set up the timeout alarm
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(135)  # Set alarm for 135 seconds

def detect_web_button(script_name):
    """Run an external script to detect the web button and keep trying until successful."""
    while True:
        elapsed = time.time() - start_time
        if elapsed >= 135:
            print("start.py reached 135-second timeout. Exiting...")
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
        print("start.py reached 135-second timeout. Exiting...")
        sys.exit(1)
    print("Performing additional tasks...")
    time.sleep(2)
    pyautogui.click(12, 342)
    print("Clicked at (82, 360).")  # Note: Message says (82, 360) but click is at (12, 342)
    time.sleep(1)
    for _ in range(10):
        pyautogui.press('down')
        time.sleep(0.2)
    time.sleep(1)
    process = subprocess.Popen(["python3", "croix.py"])
    process.wait()  # Wait for croix.py to finish
    if process.returncode != 0:
        raise Exception("croix.py failed")
    time.sleep(2)
    pyautogui.click(95, 83)
    time.sleep(3)
    process = subprocess.Popen(["python3", "croix.py"])
    process.wait()  # Wait for croix.py to finish
    if process.returncode != 0:
        raise Exception("croix.py failed")
    print("All tasks completed.")

if __name__ == "__main__":
    try:
        # Step 1: Detect the web button via the detection script
        detect_web_button('detector1.py')

        # Step 2: Perform additional tasks after the web button is detected
        perform_additional_tasks()

        signal.alarm(0)  # Cancel the alarm on success
        sys.exit(0)

    except Exception as e:
        print(f"Error in start.py: {e}")
        signal.alarm(0)
        sys.exit(1)
