import digitalio
import board
import time
from led_display import init_leds, display_pattern, DENDRITE_1_LED_START_INDEX, NUM_PIXELS_WEIGHT

# Configure dendrite input (D24)
dendrite = digitalio.DigitalInOut(board.D24)
dendrite.direction = digitalio.Direction.INPUT
dendrite.pull = digitalio.Pull.UP  # Normally HIGH (inactive)

# Initialize LEDs
init_leds()

# Light up the CENTER LED (4th position) of dendrite1 in bright blue
LED_PATTERN = [0] * NUM_PIXELS_WEIGHT  # Create blank pattern
LED_PATTERN[3] = 3  # Set 4th LED to blue (index 3)
LED_OFF = [0] * NUM_PIXELS_WEIGHT  # All LEDs off

print("DENDRITE RECEIVER TEST - VISUAL SIGNAL DETECTION")
print(f"Will light dendrite1 LED4 (position {DENDRITE_1_LED_START_INDEX+3}) blue on signal")

try:
    while True:
        if not dendrite.value:  # Active LOW detected
            print("SIGNAL DETECTED - LIGHTING LED")
            display_pattern(tuple(LED_PATTERN), DENDRITE_1_LED_START_INDEX)
            time.sleep(0.5)  # Keep lit for visible period
            
            display_pattern(tuple(LED_OFF), DENDRITE_1_LED_START_INDEX)
            time.sleep(0.1)  # Brief pause after signal
            
        time.sleep(0.05)  # Main loop delay
        
except KeyboardInterrupt:
    display_pattern(tuple(LED_OFF), DENDRITE_1_LED_START_INDEX)
    print("\nReceiver stopped")