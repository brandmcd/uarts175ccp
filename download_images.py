import os
import io
import random
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import board
import neopixel

# Google Drive API Setup
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'
FOLDER_ID = '1j6tBoQwV8kwOonj7ZIzlM4vVGo1toJxmcy19ZDc6R5OUCR7wDwMrukglvU3LharGgOAn2gt1'

# WS2812B LED Setup
LED_PIN = board.D18
NUM_LEDS = 30
BRIGHTNESS = 0.5
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

# Authenticate with Google Drive
def authenticate_drive():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

# List Images in the Specific Folder
def list_images(drive_service):
    query = f"'{FOLDER_ID}' in parents and mimeType contains 'image/'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

# Download Image
def download_image(drive_service, file_id, file_name, path):
    request = drive_service.files().get_media(fileId=file_id)
    file_path = os.path.join(path, file_name)
    with open(file_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

# LED Control
def clear_leds():
    pixels.fill((0, 0, 0))
    pixels.show()

def light_up_leds(color=(0, 255, 0), duration=1):
    pixels.fill(color)
    pixels.show()
    time.sleep(duration)
    clear_leds()

def chase_sequence(color=(255, 0, 0), duration=0.1):
    """Create a chase effect with the LEDs."""
    for i in range(NUM_LEDS):
        # Light up one LED at a time
        pixels[i] = color
        pixels.show()
        time.sleep(duration)
        # Turn off the LED after the delay
        pixels[i] = (0, 0, 0)
    # Ensure all LEDs are turned off after the chase
    clear_leds()

# Handle Images
def handle_images():
    drive_service = authenticate_drive()
    images = list_images(drive_service)

    for image in images:
        file_id = image['id']
        file_name = image['name']

        # Check if the image is not in Monitor 1 or "forgotten"
        monitor1_path = './images/monitor1'
        monitor2_path = './images/monitor2'
        forgotten_path = './images/forgotten'
        monitor1_files = os.listdir(monitor1_path)
        forgotten_files = os.listdir(forgotten_path)

        if file_name not in monitor1_files and file_name not in forgotten_files:
            #this is the first time this image has been seen
            #take the current image on monitor 1 and 50/50 chance to move it to forgotten or monitor 2
            if monitor1_files:
                # take the first file in monitor1 to move
                random_file = random.choice(monitor1_files)
                if random.random() < 0.5:
                    # Move to forgotten
                    os.rename(os.path.join(monitor1_path, random_file), os.path.join(forgotten_path, random_file))
                    print(f"Moved {random_file} to Forgotten")
                else:
                    # Move to Monitor 2
                    os.rename(os.path.join(monitor1_path, random_file), os.path.join(monitor2_path, random_file))
                    print(f"Moved {random_file} to Monitor 2")
                    #light up LEDs in a chase sequence to indicate a move to monitor 2
                    chase_sequence(color=(0, 0, 255))
            # Download the new image to monitor 1
            download_image(drive_service, file_id, file_name, monitor1_path)
            print(f"Downloaded {file_name} to Monitor 1")
            

if __name__ == "__main__":
    while True:
        handle_images()
        print("Checking for new images in 5 minutes...")
        time.sleep(300)
