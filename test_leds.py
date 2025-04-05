import time
import board
import neopixel

# LED setup
LED_PIN = board.D18         # GPIO 18
NUM_LEDS = 60                # Change to match your strip length
BRIGHTNESS = 0.5             # 0.0 to 1.0
DELAY = 0.1                  # Time between LED updates

# Initialize LED strip
pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_LEDS,
    brightness=BRIGHTNESS,
    auto_write=False
)

def color_chase(color, wait):
    """Light one LED at a time in a chase pattern."""
    for i in range(NUM_LEDS):
        pixels[i] = color
        pixels.show()
        time.sleep(wait)
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    pixels.show()

def rainbow_cycle(wait):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS + j) & 255
            pixels[i] = wheel(rc_index)
        pixels.show()
        time.sleep(wait)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

if __name__ == "__main__":
    print("Running LED test...")

    try:
        while True:
            color_chase((255, 0, 0), DELAY)  # Red
            color_chase((0, 255, 0), DELAY)  # Green
            color_chase((0, 0, 255), DELAY)  # Blue
            rainbow_cycle(0.01)

    except KeyboardInterrupt:
        pixels.fill((0, 0, 0))
        pixels.show()
        print("\nLED test ended.")
