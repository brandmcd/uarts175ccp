#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

echo "Starting image download service on Monitor 1..."
python download_images.py &

echo "Displaying images on Monitor 1..."
env DISPLAY=:0 python display.py &

echo "Starting slideshow on Monitor 2..."
env DISPLAY=:0.1 python slideshow.py &

echo "Project is running!"

