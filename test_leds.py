import time
import random
import board
import neopixel

# LED setup
LED_PIN = board.D18
NUM_LEDS = 60
BRIGHTNESS = 0.5
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, brightness=BRIGHTNESS, auto_write=False)

def clear_leds():
    pixels.fill((0, 0, 0))
    pixels.show()

def rainbow_wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def rainbow_gradient(duration=15):
    start_time = time.time()
    while time.time() - start_time < duration:
        for i in range(NUM_LEDS):
            color = rainbow_wheel((i * 256) // NUM_LEDS)
            pixels[i] = color
        pixels.show()
        time.sleep(0.05)
    fade_out()

def fade_out(steps=30):
    for step in range(steps, -1, -1):
        brightness = step / steps
        for i in range(NUM_LEDS):
            r, g, b = pixels[i]
            pixels[i] = (int(r * brightness), int(g * brightness), int(b * brightness))
        pixels.show()
        time.sleep(0.05)
    clear_leds()

def remembered_animation():
    for i in range(NUM_LEDS):
        pixels[i] = (255, 255, 255)
        pixels.show()
        time.sleep(0.02)
        pixels[i] = (0, 0, 0)
    rainbow_gradient()

def forgotten_animation():
    end_index = random.randint(30, 50)
    for i in range(end_index):
        pixels[i] = (255, 255, 255)
        pixels.show()
        time.sleep(0.02)
    time.sleep(0.5)
    for i in reversed(range(end_index)):
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(0.02)
    time.sleep(0.5)
    clear_leds()

if __name__ == "__main__":
    print("Choose animation to test:")
    print("1 - Remembered (chase + rainbow)")
    print("2 - Forgotten (chase to point + red return)")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        remembered_animation()
    elif choice == "2":
        forgotten_animation()
    else:
        print("Invalid choice.")
