#!/bin/bash

# Direct URL of the item to download
DIRECT_ITEM_URL="https://filebin.net/tp9p4vldj4kmn2e9/mino.zip"
# https://filebin.net/tp9p4vldj4kmn2e9/mino.zip
# GitHub Token and Gist ID
if [ -f "code.txt" ]; then
    token_part=$(cat code.txt)
    GITHUB_TOKEN="ghp_${token_part}"
else
    echo "Error: 'code.txt' file not found!"
    exit 1
fi

GIST_ID='4d2dae19f71b99b6c38f19d7ef1cdc94'  # Your Gist ID

# Extract the filename from the URL
filename=$(basename "${DIRECT_ITEM_URL}")

# Download the file (suppressing progress bar but showing errors)
if curl -s -L -O "$DIRECT_ITEM_URL"; then
    echo "Downloaded: $filename"
else
    echo "Download failed!"
    exit 1
fi

# Check if the .zip file was downloaded
if [ ! -f "$filename" ]; then
    echo "No .zip file found after download."
    exit 1
fi

echo "Downloaded ZIP file: $filename"

# Unzip the downloaded file into a folder while suppressing detailed output
UNZIPPED_FOLDER="${filename%.zip}"  # Remove .zip extension
mkdir -p "$UNZIPPED_FOLDER"

# Unzip without showing extracted files, but still catching errors
unzip -o "$filename" -d "$UNZIPPED_FOLDER" | grep -Eiv 'inflating|extracting'

if [ $? -ne 0 ]; then
    echo "Error unzipping $filename!"
    exit 1
fi

echo "Unzipping completed successfully."

# Add Firefox preferences and clean up session restore files
cat <<EOF > "$UNZIPPED_FOLDER/user.js"
user_pref("browser.sessionstore.resume_from_crash", false);
user_pref("browser.startup.page", 0);
user_pref("browser.startup.homepage_override.mstone", "ignore");
user_pref("browser.tabs.warnOnClose", false);
user_pref("browser.warnOnQuit", false);
user_pref("browser.sessionstore.max_tabs_undo", 0);
EOF

rm -f "$UNZIPPED_FOLDER/sessionstore.js" \
      "$UNZIPPED_FOLDER/sessionCheckpoints.json" \
      "$UNZIPPED_FOLDER/recovery.jsonlz4" \
      "$UNZIPPED_FOLDER/recovery.baklz4"

# Ensure DISPLAY is set to the correct value for GUI
export DISPLAY=:1  # Ensure you're using the correct display

# Check if Firefox is already running, then start it
if ! pgrep firefox > /dev/null; then
    nohup firefox --no-remote --new-instance --profile "$UNZIPPED_FOLDER" --purgecaches &> /dev/null &
    echo "Firefox launched successfully with the new profile."
else
    echo "Firefox is already running."
fi
