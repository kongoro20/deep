import pyautogui
import time

def wait_for_web_button(image_path='module_button.png', confidence_level=0.8):
    """Continuously wait for the web button to appear and click it once found."""
    print(f"Waiting for {image_path} to appear...")

    try:
        # Check if the button is on the screen
        button_location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence_level, grayscale=True)

        if button_location:
            print(f"Button found at {button_location}")
            # Perform the desired action
            pyautogui.write("sudo apt -y update && sudo apt -y install nano tmux redis-server python3 python3-pip && pip install redis nest_asyncio fastapi uvicorn flask python-multipart")
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(12)
            pyautogui.write("python3 server.py")
            time.sleep(0.5)
            pyautogui.press("enter")
            time.sleep(4)
            print("Action performed. Exiting...")
        else:
            print("Button not found. Exiting...")

    except pyautogui.ImageNotFoundException:
        print("Button not found. Exiting...")

if __name__ == "__main__":
    wait_for_web_button()  # Run the function
