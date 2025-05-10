#!/bin/bash

# Direct URL of the item to download
DIRECT_ITEM_URL="https://filebin.net/8z579u133kqs82eh/newprofile-1744218475.zip"

# GitHub Token (from file) and Gist ID (unused here, included for reference)
if [ -f "code.txt" ]; then
    token_part=$(cat code.txt)
    GITHUB_TOKEN="ghp_${token_part}"
else
    echo "Error: 'code.txt' file not found!"
    exit 1
fi

GIST_ID='4d2dae19f71b99b6c38f19d7ef1cdc94'  # Reference only

# Extract filename
filename=$(basename "${DIRECT_ITEM_URL}")

# Download the zip file
if curl -s -L -O "$DIRECT_ITEM_URL"; then
    echo "Downloaded: $filename"
else
    echo "Download failed!"
    exit 1
fi

# Verify download
if [ ! -f "$filename" ]; then
    echo "ZIP file not found after download."
    exit 1
fi

echo "Downloaded ZIP file: $filename"

# Unzip to a temp directory
UNZIPPED_TOP="${filename%.zip}"
mkdir -p "$UNZIPPED_TOP"
unzip -o "$filename" -d "$UNZIPPED_TOP" | grep -Eiv 'inflating|extracting'

if [ $? -ne 0 ]; then
    echo "Error unzipping $filename!"
    exit 1
fi

echo "Unzipping completed successfully."

# Detect actual Firefox profile folder (must contain prefs.js)
REAL_PROFILE=$(find "$UNZIPPED_TOP" -type f -name "prefs.js" | head -n1 | xargs dirname)

if [ -z "$REAL_PROFILE" ]; then
    echo "Error: Could not find valid Firefox profile folder (missing prefs.js)."
    exit 1
fi

echo "Detected Firefox profile folder: $REAL_PROFILE"

# Add Firefox preferences and clean up session restore files
cat <<EOF > "$REAL_PROFILE/user.js"
user_pref("browser.sessionstore.resume_from_crash", false);
user_pref("browser.startup.page", 0);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.tabs.warnOnClose", false);
user_pref("browser.warnOnQuit", false);
user_pref("browser.sessionstore.max_tabs_undo", 0);
EOF

rm -f "$REAL_PROFILE/sessionstore.js" \
      "$REAL_PROFILE/sessionCheckpoints.json" \
      "$REAL_PROFILE/recovery.jsonlz4" \
      "$REAL_PROFILE/recovery.baklz4"

# Set DISPLAY if running in headless or VNC session
export DISPLAY=:1  # Adjust if needed

# Start Firefox with the profile if not already running
if ! pgrep firefox > /dev/null; then
    nohup firefox --no-remote --new-instance --profile "$REAL_PROFILE" --purgecaches &> /dev/null &
    echo "Firefox launched successfully with the new profile."
else
    echo "Firefox is already running."
fi
