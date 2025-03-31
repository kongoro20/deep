import pyautogui
import time
import os
import sys

# Global start time
START_TIME = time.time()

# Paths to the images of the verification buttons
verif_button_image = 'terminal_button.png'
verif1_button_image = 'croix_button.png'

# Maximum number of detection attempts
max_attempts = 1000

def check_timeout():
    """Check if 135 seconds have elapsed and exit if so."""
    elapsed = time.time() - START_TIME
    if elapsed >= 135:
        print(f"croix-found.py reached 135-second timeout (elapsed: {elapsed:.1f}s). Exiting...")
        sys.exit(1)
    return elapsed

if __name__ == "__main__":
    try:
        # Step 1: Sleep for 4 seconds before starting
        print(f"Starting croix-found.py at {check_timeout():.1f}s")
        time.sleep(4)
        check_timeout()

        # Check if both image files exist
        if not os.path.isfile(verif_button_image):
            print(f"Error: The image file '{verif_button_image}' does not exist.")
            sys.exit(1)
        if not os.path.isfile(verif1_button_image):
            print(f"Error: The image file '{verif1_button_image}' does not exist.")
            sys.exit(1)

        # Loop for a maximum number of attempts
        for attempt in range(max_attempts):
            elapsed = check_timeout()
            print(f"Attempt {attempt + 1} of {max_attempts}: Attempting to detect verification buttons at {elapsed:.1f}s")

            # Sleep for 2 seconds before each detection attempt
            time.sleep(2)
            check_timeout()

            # Try to detect the first verification button: verif_button.png
            button_location = None
            try:
                print(f"Trying to detect: {verif_button_image}")
                button_location = pyautogui.locateOnScreen(verif_button_image, confidence=0.8)
            except Exception as e:
                print(f"Error while detecting '{verif_button_image}': {e}")

            # If the first button is detected, click it
            if button_location:
                print(f"'{verif_button_image}' detected at {button_location}, clicking...")
                time.sleep(1)
                check_timeout()
                pyautogui.click(7, 408)
                time.sleep(0.7)
                check_timeout()
                pyautogui.click(6, 368)
                time.sleep(0.7)
                check_timeout()
                for _ in range(10):
                    pyautogui.press('down')
                    time.sleep(0.2)
                    check_timeout()
                time.sleep(1)
                check_timeout()
                pyautogui.click(button_location)
                print(f"'{verif_button_image}' clicked!")
                time.sleep(4)
                check_timeout()
                break

            # Try to detect the second button: verif1_button.png
            try:
                print(f"Trying to detect: {verif1_button_image}")
                button_location = pyautogui.locateOnScreen(verif1_button_image, confidence=0.95)
            except Exception as e:
                print(f"Error while detecting '{verif1_button_image}': {e}")

            # If the second button is detected, click it
            if button_location:
                print(f"'{verif1_button_image}' detected at {button_location}, clicking...")
                time.sleep(1)
                check_timeout()
                pyautogui.click(button_location)
                pyautogui.click(7, 408)
                time.sleep(0.7)
                check_timeout()
                pyautogui.click(6, 368)
                time.sleep(0.7)
                check_timeout()
                for _ in range(10):
                    pyautogui.press('down')
                    time.sleep(0.2)
                    check_timeout()
                time.sleep(1)
                check_timeout()
                print(f"'{verif1_button_image}' clicked!")
                break

            print(f"Neither '{verif_button_image}' nor '{verif1_button_image}' detected. Pressing Down Arrow key...")

        else:
            print("Maximum detection attempts reached. Exiting...")
            sys.exit(1)

        print(f"croix-found.py completed successfully at {check_timeout():.1f}s")
        sys.exit(0)

    except Exception as e:
        print(f"Error in croix-found.py: {e}")
        sys.exit(1)
