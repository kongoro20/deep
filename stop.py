import pyautogui
import sys
import time

# Define image path and confidence level
image_path = "stop_button.png"
confidence_level = 0.8

# Wait a moment to allow screen rendering
time.sleep(1)

# Try to locate the stop button
button_location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence_level, grayscale=True)

if button_location:
    print("Stop button found at:", button_location)
    sys.exit(0)  # Success, continue execution of verif.sh
else:
    print("Stop button not found.")
    sys.exit(1)  # Failure, trigger restart in verif.sh
