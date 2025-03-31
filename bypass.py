import pyautogui
import time
import subprocess
import sys
import signal

# Start time tracking
start_time = time.time()

# Timeout handler for bypass.py
def timeout_handler(signum, frame):
    print("bypass.py reached 135-second timeout. Exiting with failure...")
    sys.exit(1)  # Exit with failure to signal download.py

# Set up the timeout alarm
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(135)  # Set alarm for 135 seconds

def detect_web_button(script_name):
    """Run an external script to detect the web button with up to 10 attempts."""
    attempt = 0
    max_attempts = 10

    while attempt < max_attempts:
        elapsed = time.time() - start_time
        if elapsed >= 135:  # Double-check in case signal fails
            print("bypass.py reached 135-second timeout. Exiting...")
            sys.exit(1)

        print(f"Detection attempt {attempt + 1}/{max_attempts}...")
        process = subprocess.Popen(['python3', script_name])
        process.wait()  # Wait for the detection script to finish

        if process.returncode == 0:  # Success code indicates the button was found
            print("Web button detected successfully.")
            return True  # Exit the loop and return success
        else:
            print("Web button not detected. Retrying...")
            attempt += 1
            time.sleep(1)  # Wait before the next attempt

    print("Max detection attempts reached. Proceeding with fallback action...")
    return False  # Return failure after all attempts

def perform_additional_tasks():
    """Define tasks to perform after the web button is detected."""
    elapsed = time.time() - start_time
    if elapsed >= 135:
        print("bypass.py reached 135-second timeout. Exiting...")
        sys.exit(1)
    print("Performing additional tasks...")
    time.sleep(4)

if __name__ == "__main__":
    try:
        # Total cycles of detection and fallback
        max_cycles = 2
        cycle = 0

        while cycle < max_cycles:
            elapsed = time.time() - start_time
            if elapsed >= 135:
                print("bypass.py reached 135-second timeout. Exiting...")
                sys.exit(1)

            print(f"Starting detection cycle {cycle + 1}/{max_cycles}...")

            # Step 1: Detect the web button
            button_detected = detect_web_button('stop_detection_button.py')

            if button_detected:
                # If the button is detected, perform additional tasks and exit
                print(f"Button detected during cycle {cycle + 1}. Proceeding to additional tasks.")
                time.sleep(1)
                perform_additional_tasks()
                break  # Exit the while loop if button is detected
            else:
                # Perform fallback click if the button is not detected
                print(f"Button not detected during cycle {cycle + 1}. Performing fallback click.")
                time.sleep(1.5)

            # Increment the cycle counter
            cycle += 1

        # If the script finishes all cycles without detecting the button
        if cycle == max_cycles:
            print(f"All {max_cycles} cycles completed without detecting the button.")
        
        signal.alarm(0)  # Cancel the alarm on success
        sys.exit(0)  # Normal exit

    except Exception as e:
        print(f"Error in bypass.py: {e}")
        signal.alarm(0)  # Cancel the alarm
        sys.exit(1)  # Exit with failure on exception
