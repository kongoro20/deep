#!/usr/bin/env python3
import requests
import time
import sys
import os

# Server addresses to check
servers = [
    "https://17e0d0b6-2d21-4b7f-b999-1e3861403867.deepnoteproject.com/",
    "https://4fd7ef24-8595-435c-862c-c76faa2281a9.deepnoteproject.com/"
]

def check_server(server, attempts=5, delay=1):
    for attempt in range(attempts):
        try:
            # Send GET request to the server
            response = requests.get(server, timeout=5)
            # Check the response content
            if response.text.strip() == '{"detail":"Not Found"}':
                print(f"Server {server} returned valid response 'Not Found' on attempt {attempt + 1}")
                return True
            else:
                print(f"Server {server} returned unexpected response '{response.text.strip()}' on attempt {attempt + 1}")
        except requests.RequestException as e:
            # Handle connection errors (e.g., "Nothing is running on port 8080")
            print(f"Failed to reach {server} on attempt {attempt + 1}: {e}")
        
        # Wait before the next attempt if its not the last one
        if attempt < attempts - 1:
            time.sleep(delay)
    
    # If all attempts fail
    print(f"Server {server} failed after {attempts} attempts")
    return False

def check_servers():
    for server in servers:
        if not check_server(server):
            return False
    return True

if __name__ == "__main__":
    # Check if running in continuous mode
    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        while True:
            if not check_servers():
                # Create a failure flag file to signal start.sh
                open("/tmp/request_failure", "w").close()
                exit(1)  # Exit with failure
            time.sleep(2)  # Check every 2 seconds in continuous mode
    else:
        # Normal one-time check
        if check_servers():
            print("All servers responded successfully after checks.")
            exit(0)  # Return success (0) to start.sh
        else:
            exit(1)  # Return failure (1) to start.sh
