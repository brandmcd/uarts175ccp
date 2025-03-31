#!/bin/bash

# Activate the virtual environment
source venv/bin/activate

echo "Starting image download service on Monitor 1..."
python download_images.py &

# Set Monitor 1 for displaying images
echo "Displaying images on Monitor 1..."
python display.py &

# Set Monitor 2 for the slideshow
echo "Starting slideshow on Monitor 2..."
python slideshow.py &

echo "Project is running!"

