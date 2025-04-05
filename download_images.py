import os
import io
import time
import random
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import board
import neopixel

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'
FOLDER_ID = '1j6tBoQwV8kwOonj7ZIzlM4vVGo1toJxmcy19ZDc6R5OUCR7wDwMrukglvU3LharGgOAn2gt1'

# LED setup
LED_PIN = board.D18
NUM_LEDS = 60
BRIGHTNESS_SCALE = 0.3  # Adjustable scale for actual brightness control
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, auto_write=False)

def apply_brightness(color, scale):
    return tuple(int(c * scale) for c in color)

def clear_leds():
    pixels.fill((0, 0, 0))
    pixels.show()

def safe_filename(name):
    return re.sub(r'[^\w\s\.-]', '_', name).strip()

def authenticate_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def list_images(drive_service):
    query = f"'{FOLDER_ID}' in parents and mimeType contains 'image/'"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def download_image(service, file_id, file_name, path):
    request = service.files().get_media(fileId=file_id)
    file_path = os.path.join(path, file_name)
    with open(file_path, 'wb') as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

def rainbow_wheel(pos, scale=1.0):
    if pos < 85:
        color = (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        color = (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        color = (pos * 3, 0, 255 - pos * 3)
    return apply_brightness(color, scale)

def rainbow_gradient(duration=15):
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(NUM_LEDS):
            color = rainbow_wheel((i * 256) // NUM_LEDS, BRIGHTNESS_SCALE)
            pixels[i] = color
        pixels.show()
        time.sleep(0.05)
    fade_out()

def fade_out(steps=60):
    for step in range(steps, -1, -1):
        brightness = step / steps
        for i in range(NUM_LEDS):
            r, g, b = pixels[i]
            pixels[i] = (int(r * brightness), int(g * brightness), int(b * brightness))
        pixels.show()
        time.sleep(0.05)
    clear_leds()

def remembered_animation():
    white = apply_brightness((255, 255, 255), BRIGHTNESS_SCALE)
    for i in range(NUM_LEDS):
        pixels[i] = white
        pixels.show()
        time.sleep(0.05)
    rainbow_gradient()

def forgotten_animation():
    white = apply_brightness((255, 255, 255), BRIGHTNESS_SCALE)
    red = apply_brightness((255, 0, 0), BRIGHTNESS_SCALE)
    end_index = random.randint(30, 50)
    for i in range(end_index):
        pixels[i] = white
        pixels.show()
        time.sleep(0.05)
    time.sleep(0.5)
    for i in reversed(range(end_index)):
        pixels[i] = red
        pixels.show()
        time.sleep(0.05)
    time.sleep(0.5)
    clear_leds()

monitor1_path = './images/monitor1'
monitor2_path = './images/monitor2'
forgotten_path = './images/forgotten'

def handle_images():
    service = authenticate_drive()
    images = list_images(service)

    for image in images:
        file_id = image['id']
        file_name = image['name']

        # Skip if image already seen
        seen_files = os.listdir(monitor1_path) + os.listdir(monitor2_path) + os.listdir(forgotten_path)
        if file_name in seen_files:
            continue

        # If monitor1 has an image, move it to monitor2 or forgotten
        monitor1_files = os.listdir(monitor1_path)
        if monitor1_files:
            prev_file = monitor1_files[0]
            src = os.path.join(monitor1_path, prev_file)
            if random.random() < 0.5:
                dst = os.path.join(forgotten_path, prev_file)
                print(f"Moved {prev_file} to Forgotten")
                forgotten_animation()
            else:
                dst = os.path.join(monitor2_path, prev_file)
                print(f"Moved {prev_file} to Monitor 2")
                remembered_animation()
            os.rename(src, dst)

        # Download new image to monitor1
        download_image(service, file_id, file_name, monitor1_path)
        print(f"Downloaded {file_name} to Monitor 1")
        break  # Only handle one new image per cycle

if __name__ == "__main__":
    print(f"Starting download_images.py with BRIGHTNESS_SCALE = {BRIGHTNESS_SCALE}")
    while True:
        handle_images()
        print("Checking for new images in 30 seconds...")
        time.sleep(30)
