import pyautogui
import time
import os
import sys

# Step 1: Sleep before starting
time.sleep(4)

# Paths to the images of the verification buttons
verif_button_image = 'run_button.png'
verif1_button_image = 'play_button.png'

# Maximum number of detection attempts
max_attempts = 5

# Check if both image files exist
if not os.path.isfile(verif_button_image):
    print(f"Error: The image file '{verif_button_image}' does not exist.")
if not os.path.isfile(verif1_button_image):
    print(f"Error: The image file '{verif1_button_image}' does not exist.")

# Loop for a maximum number of attempts
for attempt in range(max_attempts):
    print(f"Attempt {attempt + 1} of {max_attempts}: Attempting to detect verification buttons...")

    # Sleep before each detection attempt
    time.sleep(2)

    # Try to detect the first verification button
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
        print(f"'{verif_button_image}' continue remaining steps")
        sys.exit(1)  # Exit successfully

    # Try to detect the second verification button
    try:
        print(f"Trying to detect: {verif1_button_image}")
        button_location = pyautogui.locateOnScreen(verif1_button_image, confidence=0.95)
    except Exception as e:
        print(f"Error while detecting '{verif1_button_image}': {e}")

    # If the second button is detected, click it
    if button_location:
        print(f"'{verif1_button_image}' detected at {button_location}, clicking...")
        time.sleep(1)
        print(f"'{verif1_button_image}' continue remaining steps")
        sys.exit(1)  # Exit successfully

    # If neither button is found, press the Down Arrow key and try again
    print(f"Neither '{verif_button_image}' nor '{verif1_button_image}' detected. Pressing Down Arrow key...")

# If maximum attempts are reached without success, exit with failure
print("Maximum detection attempts reached. Exiting with failure...")
sys.exit(0)
