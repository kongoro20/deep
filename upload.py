import pyautogui
import time
import subprocess
import sys
import os
import signal

# List to keep track of subprocess PIDs and processes
subprocess_list = []

# Timeout handler for upload.py
def timeout_handler(signum, frame):
    print("upload.py reached 135-second timeout for current script. Terminating subprocesses and exiting...")
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

try:
    # Initial delay (no timeout needed yet)
    time.sleep(5)

    # Run start.py
    reset_timeout()
    if run_script('start.py') != 0:
        raise Exception("start.py failed or timed out")
    time.sleep(2)

    # Run terminal.py
    reset_timeout()
    if run_script('terminal.py') != 0:
        raise Exception("terminal.py failed or timed out")
    time.sleep(2)

    # Run pip1.py (assuming 'pip1.py' is intended, not 'pip.py' as in original)
    reset_timeout()
    if run_script('pip1.py') != 0:
        raise Exception("pip1.py failed or timed out")
    time.sleep(2)

    # Perform GUI actions
    pyautogui.click(29, 371)
    time.sleep(1)
    for _ in range(10):
        pyautogui.press('up')
        time.sleep(0.2)
    time.sleep(1)
    pyautogui.click(81, 254)
    time.sleep(5)

    # Run run.py
    reset_timeout()
    if run_script('run.py') != 0:
        raise Exception("run.py failed or timed out")
    time.sleep(4)

    # Cleanup and exit successfully
    signal.alarm(0)  # Cancel any remaining alarm
    print("upload.py completed successfully.")
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
    print(f"Error in upload.py: {e}")
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
