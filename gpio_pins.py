import digitalio
import board

# Dendrite 1
DENDRITE_1_ROTARY_PINS = [digitalio.DigitalInOut(board.D17),
                          digitalio.DigitalInOut(board.D18),
		          digitalio.DigitalInOut(board.D27),
                          digitalio.DigitalInOut(board.D22)]
DENDRITE_1_BUTTON_PIN = digitalio.DigitalInOut(board.D23)
DENDRITE_1_BARREL_PIN = digitalio.DigitalInOut(board.D24)

# Dendrite 2
DENDRITE_2_ROTARY_PINS = [digitalio.DigitalInOut(board.D9),
                          digitalio.DigitalInOut(board.D25),
		          digitalio.DigitalInOut(board.D8),
                          digitalio.DigitalInOut(board.D7)]
DENDRITE_2_BUTTON_PIN = digitalio.DigitalInOut(board.D5)
DENDRITE_2_BARREL_PIN = digitalio.DigitalInOut(board.D6)

# Dendrite 3
DENDRITE_3_ROTARY_PINS = [digitalio.DigitalInOut(board.D12),
                          digitalio.DigitalInOut(board.D13),
		          digitalio.DigitalInOut(board.D19),
                          digitalio.DigitalInOut(board.D16)]
DENDRITE_3_BUTTON_PIN = digitalio.DigitalInOut(board.D26)
DENDRITE_3_BARREL_PIN = digitalio.DigitalInOut(board.D20)

# Threshold
THRESHOLD_ROTARY_PINS = [digitalio.DigitalInOut(board.D21),
                         digitalio.DigitalInOut(board.D3),
		         digitalio.DigitalInOut(board.D4),
                         digitalio.DigitalInOut(board.D14)]

AXON_BARREL_PIN = digitalio.DigitalInOut(board.D15)

# Initialize all pins

input_pins = DENDRITE_1_ROTARY_PINS + DENDRITE_2_ROTARY_PINS + DENDRITE_3_ROTARY_PINS + \
    [DENDRITE_1_BUTTON_PIN, DENDRITE_2_BUTTON_PIN, DENDRITE_3_BUTTON_PIN] + \
    [DENDRITE_1_BARREL_PIN, DENDRITE_2_BARREL_PIN, DENDRITE_3_BARREL_PIN] + \
    THRESHOLD_ROTARY_PINS

output_pins = [AXON_BARREL_PIN]

def init_gpio():
    for pin in input_pins:
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
    for pin in output_pins:
        pin.direction = digitalio.Direction.OUTPUT
        pin.value = True
