import pyautogui
import time
import subprocess
import sys
import os
import signal

# List to keep track of subprocess PIDs and processes
subprocess_list = []

# Start time tracking for overall timeout
start_time = time.time()

# Timeout handler for pip1.py
def timeout_handler(signum, frame):
    print("pip1.py reached 135-second timeout for current script. Terminating subprocesses and exiting...")
    for process in subprocess_list:
        try:
            os.killpg(process.pid, signal.SIGKILL)  # Kill entire process group
            print(f"Terminated process group PID {process.pid}")
        except AttributeError:
            os.kill(process.pid, signal.SIGKILL)
            print(f"Terminated subprocess PID {process.pid}")
        except OSError:
            pass
    sys.exit(1)

# Function to reset the timeout alarm
def reset_timeout():
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(135)  # Reset to 135 seconds

# Function to run a Python script with timeout monitoring
def run_script(script_name, timeout=135):
    process = subprocess.Popen(['python3', script_name], preexec_fn=os.setsid)
    subprocess_list.append(process)
    script_start_time = time.time()
    
    while process.poll() is None:  # While the process is still running
        elapsed = time.time() - script_start_time
        if elapsed >= timeout:
            print(f"{script_name} exceeded {timeout}-second timeout. Terminating...")
            try:
                os.killpg(process.pid, signal.SIGKILL)
                print(f"Terminated process group PID {process.pid}")
            except AttributeError:
                os.kill(process.pid, signal.SIGKILL)
                print(f"Terminated subprocess PID {process.pid}")
            except OSError:
                pass
            return 1
        time.sleep(0.1)
    
    returncode = process.returncode
    if returncode != 0:
        print(f"{script_name} failed with return code {returncode}.")
        return returncode
    subprocess_list.remove(process)  # Remove completed process
    return 0

def detect_web_button(script_name):
    """Run an external script to detect the web button and keep trying until successful."""
    global subprocess_list
    while True:
        elapsed = time.time() - start_time
        if elapsed >= 135:
            print("pip1.py reached 135-second timeout. Exiting...")
            for process in subprocess_list:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                    print(f"Terminated process group PID {process.pid}")
                except OSError:
                    pass
            sys.exit(1)

        reset_timeout()  # Reset timeout for each attempt
        process = subprocess.Popen(['python3', script_name], preexec_fn=os.setsid)
        subprocess_list.append(process)
        try:
            process.wait()
        except KeyboardInterrupt:
            os.killpg(process.pid, signal.SIGKILL)
            raise

        if process.returncode == 0:
            print(f"Web button detected and clicked by {script_name}. Proceeding with tasks...")
            subprocess_list.remove(process)
            return
        else:
            print(f"Web button not detected by {script_name}. Retrying...")
            subprocess_list.remove(process)
            time.sleep(2)

def perform_additional_tasks():
    """Define tasks to perform after the web button is detected."""
    elapsed = time.time() - start_time
    if elapsed >= 135:
        print("pip1.py reached 135-second timeout. Exiting...")
        for process in subprocess_list:
            try:
                os.killpg(process.pid, signal.SIGKILL)
                print(f"Terminated process group PID {process.pid}")
            except OSError:
                pass
        sys.exit(1)
    
    print("Performing additional tasks...")
    time.sleep(2)
    pyautogui.click(1038, 524)
    time.sleep(0.5)
    pyautogui.write("tmux")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(1.5)

    # Start Redis server
    pyautogui.write("redis-server")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(4)

    # Exit tmux session with Ctrl+B then D
    pyautogui.hotkey("ctrl", "b")
    pyautogui.press("d")
    time.sleep(1)
    pyautogui.write("tmux")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(1.5)

    # Start upload.py
    pyautogui.write("python3 upload.py")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(4)

    # Run module1.py with timeout
    reset_timeout()
    if run_script("module1.py") != 0:
        raise Exception("module1.py failed or timed out")
    time.sleep(1)

    pyautogui.click(980, 531)
    time.sleep(0.5)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(1)
    pyautogui.click(980, 531)
    time.sleep(0.5)
    # Exit tmux session with Ctrl+B then D
    pyautogui.hotkey("ctrl", "b")
    pyautogui.press("d")
    time.sleep(1)
    print("All tasks completed.")

if __name__ == "__main__":
    try:
        # Step 1: Detect the web button via the detection script
        detect_web_button('detector3.py')

        # Step 2: Perform additional tasks after the web button is detected
        perform_additional_tasks()

        signal.alarm(0)  # Cancel the alarm on success
        for process in subprocess_list:
            try:
                os.killpg(process.pid, signal.SIGKILL)
                print(f"Terminated process group PID {process.pid}")
            except AttributeError:
                os.kill(process.pid, signal.SIGKILL)
                print(f"Terminated subprocess PID {process.pid}")
            except OSError:
                pass
        sys.exit(0)

    except Exception as e:
        print(f"Error in pip1.py: {e}")
        signal.alarm(0)
        for process in subprocess_list:
            try:
                os.killpg(process.pid, signal.SIGKILL)
                print(f"Terminated process group PID {process.pid}")
            except AttributeError:
                os.kill(process.pid, signal.SIGKILL)
                print(f"Terminated subprocess PID {process.pid}")
            except OSError:
                pass
        sys.exit(1)
