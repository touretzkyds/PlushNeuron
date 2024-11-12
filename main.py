import time
import datetime
import pygame
import pygame.mixer
#import RPi.GPIO as GPIO

import led_display
import plush_sounds
import gpio_pins
import state_machine

led_display.init_leds()
plush_sounds.init_sound()
gpio_pins.init_gpio()

dendrtie1 = Dendrite("dendrite1", 0,
                     gpio_pins.DENDRITE_1_ROTARY_PINS,
                     led_display.DENDRITE_1_LED_START_INDEX,
                     plush_sounds.DENDRITE_1_WEIGHT_CHANNEL,
                     plush_sounds.DENDRITE_1_BUTTON_CHANNEL)
