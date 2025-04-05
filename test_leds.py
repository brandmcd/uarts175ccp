import time
import random
import board
import neopixel

# LED setup
LED_PIN = board.D18
NUM_LEDS = 60
BRIGHTNESS_SCALE = 0.2  # Adjust this between 0.0 and 1.0 to control actual output brightness
pixels = neopixel.NeoPixel(LED_PIN, NUM_LEDS, auto_write=False)

def apply_brightness(color, scale):
    return tuple(int(c * scale) for c in color)

def clear_leds():
    pixels.fill((0, 0, 0))
    pixels.show()

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
        factor = step / steps
        for i in range(NUM_LEDS):
            r, g, b = pixels[i]
            pixels[i] = (int(r * factor), int(g * factor), int(b * factor))
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

if __name__ == "__main__":
    BRIGHTNESS_SCALE = 0.5
    print("Choose animation to test:")
    print("1 - Remembered (chase + rainbow)")
    print("2 - Forgotten (chase to point + red return)")
    print("3 - Set brightness scale")
    choice = input("Enter 1, 2, or 3: ")

    if choice == "1":
        remembered_animation()
    elif choice == "2":
        forgotten_animation()
    elif choice == "3":
        scale_input = float(input("Enter brightness scale (0.0 to 1.0): "))
        if 0.0 <= scale_input <= 1.0:
            BRIGHTNESS_SCALE = scale_input
            print(f"Brightness scale set to {BRIGHTNESS_SCALE}. Now re-run the animation.")
        else:
            print("Invalid brightness scale. Must be between 0.0 and 1.0.")
    else:
        print("Invalid choice.")
