import digitalio
import board

# Dendrite 1
dendrite1_rotary_pins = [digitalio.DigitalInOut(board.D2), digitalio.DigitalInOut(board.D3),
		         digitalio.DigitalInOut(board.D4), digitalio.DigitalInOut(board.D17)]
dendrite1_button_pin = digitalio.DigitalInOut(board.D27)
dendrite1_audio_jack_pin = None # fix this later

# Dendrite 2
dendrite2_rotary_pins = [digitalio.DigitalInOut(board.D7), digitalio.DigitalInOut(board.D8),
		         digitalio.DigitalInOut(board.D25), digitalio.DigitalInOut(board.D24)]
dendrite2_button_pin = digitalio.DigitalInOut(board.D23)
dendrite2_audio_jack_pin = None # fix this later

# Dendrite 3
dendrite3_rotary_pins = [digitalio.DigitalInOut(board.D5), digitalio.DigitalInOut(board.D6),
		         digitalio.DigitalInOut(board.D13), digitalio.DigitalInOut(board.D19)]
dendrite3_button_pin = digitalio.DigitalInOut(board.D26)
dendrite3_audio_jack_pin = None # fix this later

# Initialize all pins

input_pins = dendrite1_rotary_pins + dendrite2_rotary_pins + dendrite3_rotary_pins +
    [dendrite1_button_pin, dendrite2_button_pin, dendrite3_button_pin] +
    [dendrite1_audio_jack_pin + dendrite2_audio_jack_pin + dendrite3_audio_jack_pin]

def init_gpio():
    for pin in input_pins:
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP
    # init output pin for axon barrel connector
