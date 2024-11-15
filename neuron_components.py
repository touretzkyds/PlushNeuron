import datetime
from enum import Enum

from state_machine import StateMachine, now_msecs
from led_display import display_pattern, DENDRITE_ROTARY_COLORS, DENDRITE_ROTARY_BLANK, THRESHOLD_ROTARY_COLORS
from plush_sounds import queue_sound, WEIGHT_SOUNDS, WEIGHT_INCREASE_SOUNDS, WEIGHT_DECREASE_SOUNDS

"""
**** TREAT ZERO VALUE DIFFERENTLY FOR ROTARY SWITCHES ****
"""

class Debouncer():
    BUTTON_PERSISTENCE_TIME = 100 # msecs
    ROTARY_PERSISTENCE_TIME = 50 # msecs

    def __init__(self, persistence_time):
        self.persistence_time = persistence_time
        self.current_value = None
        self.new_value = None
        self.new_time = -1

    def debounce(self,value):
        if self.current_value == None:  # initializing
            self.current_value = value
        elif self.current_value == value: # value persists
            self.new_value = None
        else:  # value is changing
            t = now_msecs()
            if value == self.new_value:  # change is consistent
                if (t - self.new_time) > self.persistence_time:   # and persisted long enough
                    self.current_value = value  # make the change
            else:  # change is new: start timer
                self.new_value = value
                self.new_time = t
        return self.current_value



class RotarySwitch():
    def __init__(self, name, gpio_pins):
        self.gpio_pins = gpio_pins
        self.debouncer = Debouncer(Debouncer.ROTARY_PERSISTENCE_TIME)
        self.current_value = 0

    def decode_switch(self):
        value = 0
        for i in range(len(self.gpio_pins)):
            if self.gpio_pins[i].value == False:
                value += (1 << i)
        return value

    def update(self): pass


class DendriteRotarySwitch(RotarySwitch):
    def __init__(self, dendrite, name, gpio_pins):
        super().__init__(name, gpio_pins)
        self.dendrite = dendrite

    def update(self):
        new_value = self.debouncer.debounce(self.decode_switch())
        if (new_value > self.current_value or (new_value == 0 and self.current_value > 5)) and \
                new_value in self.dendrite.WEIGHT_VALUES:
            print(f"dendrite rotary update: cur={self.current_value} new={new_value}")
            self.current_value = new_value
            self.dendrite.increase_weight()
        elif (new_value < self.current_value or (self.current_value == 0 and new_value > 5)) and \
                new_value in self.dendrite.WEIGHT_VALUES:
            self.current_value = new_value
            self.dendrite.decrease_weight()
        else:
            pass  # ignored switch position

        
class BodyRotarySwitch(RotarySwitch):
    # fill this in later
    pass


class Button(StateMachine):
    states = Enum('ButtonStates', [('BUTTON_OFF', 1), ('BUTTON_ON', 2)])
    def __init__(self, dendrite, button_gpio_pin, barrel_gpio_pin):
        super().__init__(f"Button {dendrite.dendrite_index}", self.states)
        self.dendrite = dendrite
        self.button_gpio_pin = button_gpio_pin
        self.barrel_gpio_pin = barrel_gpio_pin
        self.debouncer = Debouncer(Debouncer.BUTTON_PERSISTENCE_TIME)
        self.current_value = 0

    def update(self):
        super().update()
        # not handling the barrel connector for now, just the button
        new_value = self.debouncer.debounce(self.button_gpio_pin.value + 0)
        if new_value < self.current_value:
            self.button_pressed()
        elif new_value > self.current_value:
            self.button_released()
        self.current_value = new_value

    def button_pressed(self):
        # play sound
        self.dendrite.weight_display.transition(WeightDisplay.states.FLASH_OFF)
        self.transition(self.states.BUTTON_ON)

    def button_released(self):
        # play sound
        self.dendrite.weight_display.transition(WeightDisplay.states.FLASH_ON)
        self.transition(self.states.BUTTON_OFF)



class LEDDisplay(StateMachine):
    def __init__(self, name, states, led_start_index):
        super().__init__(name, states)
        self.led_start_index = led_start_index


class WeightDisplay(LEDDisplay):
    FLASH_ON_TIME = 200
    FLASH_OFF_TIME = 100
    states = Enum('WeightDisplayStates', [('IDLE', 1), ('FLASH_OFF', 2), ('FLASH_ON', 3), ('SHOW_WEIGHT', 4)])

    def __init__(self, dendrite, led_start_index):
        super().__init__(f"WeightDisplay {dendrite.dendrite_index}", self.states, led_start_index)
        self.dendrite = dendrite

    def update(self):
        super().update()
        if self.current_state == self.states.FLASH_ON and self.state_duration >= self.FLASH_ON_TIME:
            display_pattern(DENDRITE_ROTARY_BLANK, self.led_start_index)
            self.transition(self.states.FLASH_OFF)
        elif self.current_state == self.states.FLASH_OFF and self.state_duration >= self.FLASH_OFF_TIME:
            weight_index = self.dendrite.weight_index
            display_pattern(DENDRITE_ROTARY_COLORS[self.dendrite.weight_index], self.led_start_index)
            self.transition(self.states.FLASH_ON)
        elif self.current_state == self.states.SHOW_WEIGHT:
            weight_index = self.dendrite.weight_index
            display_pattern(DENDRITE_ROTARY_COLORS[self.dendrite.weight_index], self.led_start_index)
            self.transition(self.states.IDLE)
        else:
            pass


class Dendrite():
    WEIGHT_VALUES = { # 10 position switch
        0 : 0,
        1 : 1,
        2 : 2,
        3 : 3,
        4 : 4,
        # no entry for 5
        6 : -4,
        7 : -3,
        8 : -2,
        9 : -1
    }

    def __init__(self, name, dendrite_index, rotary_gpio_pins, button_gpio_pin, barrel_gpio_pin,
                 led_start_index, rotary_audio_channel, button_audio_channel):
        self.name = name
        self.dendrite_index = dendrite_index
        self.rotary_switch = DendriteRotarySwitch(self, name, rotary_gpio_pins)
        self.button = Button(self, button_gpio_pin, barrel_gpio_pin)
        self.weight_display = WeightDisplay(self, led_start_index)
        self.rotary_audio_channel = rotary_audio_channel
        self.button_audio_channel = button_audio_channel
        self.weight_index = 0

    def update(self):
        self.rotary_switch.update()
        self.button.update()
        self.weight_display.update()

    def increase_weight(self):
        sound = WEIGHT_INCREASE_SOUNDS[self.dendrite_index][self.weight_index]
        queue_sound(sound, self.rotary_audio_channel)
        self.weight_index = self.rotary_switch.current_value
        print(f"increase weight: weight_index now {self.weight_index}")
        self.weight_display.transition(WeightDisplay.states.SHOW_WEIGHT)

    def decrease_weight(self):
        sound = WEIGHT_DECREASE_SOUNDS[self.dendrite_index][self.weight_index]
        queue_sound(sound, self.rotary_audio_channel)
        self.weight_index = self.rotary_switch.current_value
        self.weight_display.transition(WeightDisplay.states.SHOW_WEIGHT)



