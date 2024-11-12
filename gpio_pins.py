import digitalio
import board

# Dendrite 1
DENDRITE1__ROTARY_PINS = [digitalio.DigitalInOut(board.D2), digitalio.DigitalInOut(board.D3),
		          digitalio.DigitalInOut(board.D4), digitalio.DigitalInOut(board.D17)]
DENDRITE_1_BUTTON_PIN = digitalio.DigitalInOut(board.D27)
DENDRITE_1_BARREL_PIN = None # fix this later

# Dendrite 2
DENDRITE_2_ROTARY_PINS = [digitalio.DigitalInOut(board.D7), digitalio.DigitalInOut(board.D8),
		         digitalio.DigitalInOut(board.D25), digitalio.DigitalInOut(board.D24)]
DENDRITE_2_BUTTON_PIN = digitalio.DigitalInOut(board.D23)
DENDRITE_2_BARREL_PIN = None # fix this later

# Dendrite 3
DENDRITE_3_ROTARY_PINS = [digitalio.DigitalInOut(board.D5), digitalio.DigitalInOut(board.D6),
		         digitalio.DigitalInOut(board.D13), digitalio.DigitalInOut(board.D19)]
DENDRITE_3_BUTTON_PIN = digitalio.DigitalInOut(board.D26)
DENDRITE_3_BARREL_PIN = None # fix this later

# Initialize all pins

input_pins = DENDRITE_1_ROTARY_PINS + DENDRITE_2_ROTARY_PINS + DENDRITE_3_ROTARY_PINS + \
    [DENDRITE_1_BUTTON_PIN, DENDRITE_2_BUTTON_PIN, DENDRITE_3_BUTTON_PIN] + \
    [DENDRITE_1_BARREK_PIN + DENDRITE_2_BARREL_PIN + DENDRITE_3_BARREL_PIN]

def init_gpio():
    for pin in input_pins:
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
    # init output pin for axon barrel connector
