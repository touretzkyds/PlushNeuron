import time
import datetime
#import RPi.GPIO as GPIO

import led_display
import plush_sounds
import gpio_pins
from neuron_components import Dendrite

dendrite1 = Dendrite("dendrite1", 0, \
                     gpio_pins.DENDRITE_1_ROTARY_PINS, \
                     gpio_pins.DENDRITE_1_BUTTON_PIN, \
                     gpio_pins.DENDRITE_1_BARREL_PIN, \
                     led_display.DENDRITE_1_LED_START_INDEX, \
                     plush_sounds.DENDRITE_1_WEIGHT_CHANNEL, \
                     plush_sounds.DENDRITE_1_BUTTON_CHANNEL, \
)

dendrite2 = Dendrite("dendrite2", 1,\
                     gpio_pins.DENDRITE_2_ROTARY_PINS, \
                     gpio_pins.DENDRITE_2_BUTTON_PIN, \
                     gpio_pins.DENDRITE_2_BARREL_PIN, \
                     led_display.DENDRITE_2_LED_START_INDEX, \
                     plush_sounds.DENDRITE_2_WEIGHT_CHANNEL, \
                     plush_sounds.DENDRITE_2_BUTTON_CHANNEL)

dendrite3 = Dendrite("dendrite3", 2,\
                     gpio_pins.DENDRITE_3_ROTARY_PINS, \
                     gpio_pins.DENDRITE_3_BUTTON_PIN, \
                     gpio_pins.DENDRITE_3_BARREL_PIN, \
                     led_display.DENDRITE_3_LED_START_INDEX, \
                     plush_sounds.DENDRITE_3_WEIGHT_CHANNEL, \
                     plush_sounds.DENDRITE_3_BUTTON_CHANNEL)

dendrites = [dendrite1, dendrite2, dendrite3]

gpio_pins.init_gpio()
led_display.init_leds()

while True:
    for d in dendrites:
        d.update()
    # update cell body
    # update axon
    plush_sounds.udpate_all_channels()
    time.sleep(0.01)
