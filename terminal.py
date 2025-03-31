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
    print("terminal.py reached 135-second timeout. Terminating subprocesses and exiting...")
    for proc in subprocesses:
        try:
            os.killpg(proc.pid, signal.SIGKILL)  # Kill process group
            print(f"Terminated process group PID {proc.pid}")
        except AttributeError:
            os.kill(proc.pid, signal.SIGKILL)
            print(f"Terminated subprocess PID {proc.pid}")
        except OSError:
            pass
    os._exit(1)  # Force immediate exit

# Set up the timeout alarm
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(135)

def detect_web_button(script_name):
    """Run an external script to detect the web button with up to 20 attempts."""
    global subprocesses
    attempt = 0
    max_attempts = 20

    while attempt < max_attempts:
        elapsed = time.time() - start_time
        if elapsed >= 135:
            print("terminal.py reached 135-second timeout. Exiting...")
            for proc in subprocesses:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                    print(f"Terminated process group PID {proc.pid}")
                except OSError:
                    pass
            os._exit(1)

        print(f"Detection attempt {attempt + 1}/{max_attempts}...")
        process = subprocess.Popen(['python3', script_name], preexec_fn=os.setsid)
        subprocesses.append(process)
        try:
            process.wait()
        except KeyboardInterrupt:
            os.killpg(process.pid, signal.SIGKILL)
            raise

        if process.returncode == 0:
            print("Web button detected successfully.")
            subprocesses.remove(process)
            return True
        else:
            print("Web button not detected. Retrying...")
            subprocesses.remove(process)
            attempt += 1
            time.sleep(2)

    print("Max detection attempts reached. Proceeding with fallback action...")
    return False

def perform_additional_tasks():
    """Define tasks to perform after the web button is detected."""
    elapsed = time.time() - start_time
    if elapsed >= 135:
        print("terminal.py reached 135-second timeout. Exiting...")
        for proc in subprocesses:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
                print(f"Terminated process group PID {proc.pid}")
            except OSError:
                pass
        os._exit(1)
    print("Performing additional tasks...")
    time.sleep(2)
    pyautogui.click(999, 438)
    time.sleep(1)
    pyautogui.write("sudo apt -y update && sudo apt -y install nano tmux redis-server python3 python3-pip && pip install redis nest_asyncio fastapi uvicorn flask python-multipart")
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(2)

if __name__ == "__main__":
    try:
        # Total cycles of detection and fallback
        max_cycles = 4
        cycle = 0

        while cycle < max_cycles:
            elapsed = time.time() - start_time
            if elapsed >= 135:
                print("terminal.py reached 135-second timeout. Exiting...")
                for proc in subprocesses:
                    try:
                        os.killpg(proc.pid, signal.SIGKILL)
                        print(f"Terminated process group PID {proc.pid}")
                    except OSError:
                        pass
                os._exit(1)

            print(f"Starting detection cycle {cycle + 1}/{max_cycles}...")

            # Step 1: Detect the web button
            button_detected = detect_web_button('detector2.py')

            if button_detected:
                # If the button is detected, perform additional tasks and exit
                print(f"Button detected during cycle {cycle + 1}. Proceeding to additional tasks.")
                perform_additional_tasks()
                break
            else:
                # Perform fallback click if the button is not detected
                print(f"Button not detected during cycle {cycle + 1}. Performing fallback click.")
                time.sleep(0.7)
                pyautogui.click(89, 84)
                time.sleep(2)
                # Launch clikterminal.py in a new process group
                process = subprocess.Popen(['python3', 'clikterminal.py'], preexec_fn=os.setsid)
                subprocesses.append(process)
                try:
                    process.wait()
                except KeyboardInterrupt:
                    os.killpg(process.pid, signal.SIGKILL)
                    raise
                if process.returncode != 0:
                    raise Exception("clikterminal.py failed or timed out")
                subprocesses.remove(process)

            # Increment the cycle counter
            cycle += 1

        # If the script finishes all cycles without detecting the button
        if cycle == max_cycles:
            print(f"All {max_cycles} cycles completed without detecting the button.")

        signal.alarm(0)
        for proc in subprocesses:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
                print(f"Terminated process group PID {proc.pid}")
            except OSError:
                pass
        sys.exit(0)

    except Exception as e:
        print(f"Error in terminal.py: {e}")
        for proc in subprocesses:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
                print(f"Terminated process group PID {proc.pid}")
            except OSError:
                pass
        signal.alarm(0)
        os._exit(1)
