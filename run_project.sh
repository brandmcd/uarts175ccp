#!/bin/bash

echo "Starting..."

# Ensure the correct Google Drive folder ID is set
export GOOGLE_DRIVE_FOLDER_ID=1j6tBoQwV8kwOonj7ZIzlM4vVGo1toJxmcy19ZDc6R5OUCR7wDwMrukglvU3LharGgOAn2gt1

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Ensure X server is running
echo "Checking if X server is running..."
if ! pgrep -x "Xorg" > /dev/null && ! pgrep -x "Xwayland" > /dev/null; then
  echo "X server is not running. Starting LightDM..."
  sudo systemctl start lightdm
  sleep 5
else
  echo "X server is already running."
fi

# Set the correct DISPLAY variable for each monitor
echo "Setting display variables..."
export DISPLAY=:0
xrandr --output XWAYLAND0 --auto
xrandr --output XWAYLAND1 --auto

# Allow access to the display
echo "Granting access to X server..."
xhost + > /dev/null 2>&1

# Confirm Google Drive Folder ID
if [ -z "$GOOGLE_DRIVE_FOLDER_ID" ]; then
  echo "Error: GOOGLE_DRIVE_FOLDER_ID is not set. Exiting..."
  exit 1
else
  echo "Using Google Drive Folder ID: $GOOGLE_DRIVE_FOLDER_ID"
fi

# Start the image download service
echo "Starting image download service..."
sudo ./venv/bin/python3 download_images.py &

# Start Monitor 1 display
echo "Starting display on Monitor 1..."
env DISPLAY=:0 python3 display.py &

# Start Monitor 2 slideshow
echo "Starting slideshow on Monitor 2..."
env DISPLAY=:0 python3 slideshow.py &

echo "Project is running. Press Ctrl+C to stop."

# Keep the script alive to catch any errors
wait
