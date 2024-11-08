import digitalio
import board
import time
import datetime
import adafruit_dotstar as dotstar
import pygame
import pygame.mixer
import RPi.GPIO as GPIO

import plush_sounds
import state_machine

# Initialize pygame for sound
#pygame.mixer.pre_init(buffer=44100)
pygame.mixer.init(4096, -16, 1, 1024)
pygame.mixer.music.set_volume(0.9) #volume at 90%

GPIO.setmode(GPIO.BCM) # enable audio jack output

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

for pin in input_pins:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.UP

################ DotStar LEDs ################

dots = dotstar.DotStar(board.SCK, board.MOSI, 21, brightness=0.25)

color_black = (0, 0, 0)
color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)

RGB_COLORS = (
    (  0,   0,   0),  # 0 - black
    (255,   0,   0),  # 1 - red
    (  0, 255,   0),  # 2 - green
    (  0,   0, 255)   # 3 - blue
)

DENDRITE_ROTARY_COLORS = (
    (0, 0, 0, 3, 0, 0, 0), # 0 = blue
    (0, 0, 2, 0, 0, 0, 0), # 1 = green
    (0, 2, 2, 0, 0, 0, 0), # 2 = green green
    (2, 2, 2, 0, 0, 0, 0), # 3 = green green green
    (2, 2, 2, 2, 0, 0, 0), # 4 = green green green green
    (0, 0, 0, 0, 0, 0, 0), # 5 = nothing
    (0, 0, 0, 1, 1, 1, 1), # 6 = red red red red
    (0, 0, 0, 0, 1, 1, 1), # 7 = red red red
    (0, 0, 0, 0, 1, 1, 0), # 8 = red red
    (0, 0, 0, 0, 1, 0, 0)  # 9 = red
)

def display_pattern(patterns, led_start_index, value):
    pattern = patterns[value]
    for i in range(len(pattern)):
        dots[led_start_index+i] = RGB_COLORS[pattern[i]]
    dots.show()
