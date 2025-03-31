import pyautogui
import time
import subprocess
import sys
import os
import signal

# List to keep track of subprocess PIDs and processes
subprocess_list = []

# Timeout handler for download.py
def timeout_handler(signum, frame):
    print("download.py reached 135-second timeout for current script. Terminating subprocesses and exiting...")
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
    # Use os.setsid to create a new process group (Unix-specific)
    process = subprocess.Popen(['python3', script_name], preexec_fn=os.setsid)
    subprocess_list.append(process)
    start_time = time.time()
    
    while process.poll() is None:  # While the process is still running
        elapsed = time.time() - start_time
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

# Function to run a Python script without a local timeout
def run_script_no_timeout(script_name):
    # Use os.setsid to create a new process group (Unix-specific)
    process = subprocess.Popen(['python3', script_name], preexec_fn=os.setsid)
    subprocess_list.append(process)
    
    # Wait for the process to complete without enforcing a timeout
    returncode = process.wait()
    if returncode != 0:
        print(f"{script_name} failed with return code {returncode} (possibly due to its own timeout or subprocess failure).")
        return returncode
    subprocess_list.remove(process)  # Remove completed process
    return 0

try:
    # Initial setup doesnt need a timeout yet
    time.sleep(2)

    try:
        tab_button_location = pyautogui.locateCenterOnScreen('tab_button.png', confidence=0.8)
        if tab_button_location is not None:
            print("Tab button detected, clicking at (1342, 125)...")
            pyautogui.click(1342, 175)
            time.sleep(2)
        else:
            print("Tab button not detected, proceeding to Step 1...")
    except Exception as e:
        print(f"Error detecting tab button: {e}")
        print("Proceeding to Step 1...")

    time.sleep(2)

    pyautogui.click(471, 82)
    time.sleep(0.7)

    url = "https://deepnote.com/workspace/dow-7e0bb950-9742-4324-881c-e398a457cefd/project/upload-00594aac-181a-49dd-a9b2-01942ee547d5?utm_content=00594aac-181a-49dd-a9b2-01942ee547d5"
    pyautogui.write(url)
    time.sleep(1)

    pyautogui.press('enter')
    time.sleep(5)

    # Reset timeout before each script with timeout enforcement
    reset_timeout()
    if run_script('bypass.py') != 0:
        raise Exception("bypass.py failed or timed out")
    time.sleep(1.5)

    reset_timeout()
    if run_script('start.py') != 0:
        raise Exception("start.py failed or timed out")
    time.sleep(2)

    reset_timeout()
    if run_script('terminal.py') != 0:
        raise Exception("terminal.py failed or timed out")
    time.sleep(2)

    reset_timeout()
    if run_script('pip.py') != 0:
        raise Exception("pip.py failed or timed out")
    time.sleep(2)

    pyautogui.click(29, 371)
    time.sleep(1)
    for _ in range(10):
        pyautogui.press('up')
        time.sleep(0.2)
    time.sleep(1)
    pyautogui.click(81, 254)
    time.sleep(5)

    reset_timeout()
    if run_script('run.py') != 0:
        raise Exception("run.py failed or timed out")
    time.sleep(4)

    pyautogui.hotkey('ctrl', 't')
    time.sleep(1)

    url2 = "https://deepnote.com/workspace/dow-7e0bb950-9742-4324-881c-e398a457cefd/project/download-4f68e2cf-7140-471d-977f-a86380d0e026?utm_content=4f68e2cf-7140-471d-977f-a86380d0e026"
    pyautogui.write(url2)
    time.sleep(0.5)

    pyautogui.press('enter')
    time.sleep(4)

    reset_timeout()
    if run_script('bypass.py') != 0:
        raise Exception("bypass.py failed or timed out")
    time.sleep(1)

    # Cancel any existing timeout alarm before running upload.py
    signal.alarm(0)  # Disable the global 135-second alarm
    print("Running upload.py without timeout enforcement...")
    if run_script_no_timeout('upload.py') != 0:
        raise Exception("upload.py failed or timed out internally")
    time.sleep(1)

    pyautogui.click(1324, 12)
    time.sleep(0.3)
    pyautogui.click(1324, 12)
    time.sleep(0.3)

    signal.alarm(0)  # Cancel any remaining alarm (redundant here but safe)
    print("download.py completed successfully.")
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
    print(f"Error in download.py: {e}")
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
