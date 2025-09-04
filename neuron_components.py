import datetime
from enum import Enum
from math import floor

from state_machine import StateMachine, now_msecs
from led_display import display_pattern, DENDRITE_ROTARY_COLORS, DENDRITE_ROTARY_BLANK, \
    THRESHOLD_ROTARY_COLORS, ACTIVATION_COLORS, AXON_BLANK_PATTERN, \
    AXON_FIRING_PATTERNS, NUM_AXON_STRIPS, NUM_PIXELS_AXON_STRIP
from plush_sounds import queue_sound, WEIGHT_SOUNDS, WEIGHT_INCREASE_SOUNDS, WEIGHT_DECREASE_SOUNDS, \
    THRESHOLD_INCREASE_SOUNDS, THRESHOLD_DECREASE_SOUNDS, AXON_FIRE_SOUND
import plush_sounds

"""
**** TREAT ZERO VALUE DIFFERENTLY FOR ROTARY SWITCHES ****
"""

class Debouncer():
    BUTTON_PERSISTENCE_TIME = 20 # msecs
    ROTARY_PERSISTENCE_TIME = 50 # msecs
    MAX_PERSISTENCE_TIME = max(BUTTON_PERSISTENCE_TIME, ROTARY_PERSISTENCE_TIME)

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

################ Rotary Switches ################

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
        # midpoint will be 5 for a 10-position switch
        self.midpoint = floor(0.6 + max(self.dendrite.WEIGHT_VALUES.keys())/2)

    def update(self):
        new_value = self.debouncer.debounce(self.decode_switch())
        if (0 <= self.current_value < new_value < self.midpoint) or \
           (self.midpoint < self.current_value < new_value) or \
           (new_value < self.midpoint < self.current_value):
            self.current_value = new_value
            self.dendrite.increase_weight()
        elif (0 <= new_value < self.current_value < self.midpoint) or \
             (self.midpoint < new_value < self.current_value) or \
             (self.current_value < self.midpoint < new_value):
            self.current_value = new_value
            self.dendrite.decrease_weight()
        else:
            pass  # ignored switch position

        
class ThresholdRotarySwitch(RotarySwitch):
    def __init__(self, soma, gpio_pins):
        super().__init__('threshold switch', gpio_pins)
        self.soma = soma
        # midpoint will be 8 for a 16-position switch
        self.midpoint = floor(0.6 + max(self.soma.THRESHOLD_VALUES.keys())/2)

    def update(self):
        new_value = self.debouncer.debounce(self.decode_switch())
        # Logic is slightly different than for WeightRotarySwitch
        # because we're allowing midpoint as a valid switch value.
        if (0 <= self.current_value < new_value <= self.midpoint) or \
           (self.midpoint < self.current_value < new_value) or \
           (new_value <= self.midpoint < self.current_value):
            self.current_value = new_value
            self.soma.increase_threshold()
        elif (0 <= new_value < self.current_value <= self.midpoint) or \
             (self.midpoint < new_value < self.current_value) or \
             (self.current_value <= self.midpoint < new_value):
            self.current_value = new_value
            self.soma.decrease_threshold()
        else:
            pass  # ignored switch position


################ Buttons and Barrel Connectors ################

class Button(StateMachine):
    states = Enum('ButtonStates', [('BUTTON_OFF', 1), ('BUTTON_ON', 2)])
    
    def __init__(self, dendrite, button_gpio_pin, barrel_gpio_pin, button_audio_channel):
        super().__init__(f"Button {dendrite.dendrite_index}", self.states)
        self.dendrite = dendrite
        self.button_gpio_pin = button_gpio_pin
        self.barrel_gpio_pin = barrel_gpio_pin
        self.button_audio_channel = button_audio_channel
        self.debouncer = Debouncer(Debouncer.BUTTON_PERSISTENCE_TIME)
        self.current_value = True  # pin is high when button not pressed
        self.transmitted_value = 0

    def update(self):
        super().update()
        new_button_value = self.debouncer.debounce(self.button_gpio_pin.value)
        new_barrel_value = self.barrel_gpio_pin.value
        # button is pressed when pin pulled down to 0
        new_value = min(new_button_value, new_barrel_value)
        if new_value < self.current_value:
            self.current_value = new_value
            self.button_pressed()
        elif new_value > self.current_value:
            self.current_value = new_value
            self.button_released()
        else:
            pass # state unchanged

    def button_pressed(self):
        #print(f"Button pressed: {self} {self.dendrite}")
        self.transmitted_value = 1
        sound = WEIGHT_SOUNDS[self.dendrite.dendrite_index][self.dendrite.weight_index]
        queue_sound(sound, self.button_audio_channel)
        self.dendrite.weight_display.transition(WeightDisplay.states.START_FLASH)
        self.transition(self.states.BUTTON_ON)

    def button_released(self):
        #print(f"Button released: {self} {self.dendrite}")
        self.transmitted_value = 0
        self.dendrite.weight_display.finish_flash()
        self.transition(self.states.BUTTON_OFF)


################ LED Displays ################

class LEDDisplay(StateMachine):
    def __init__(self, name, states, led_start_index):
        super().__init__(name, states)
        self.led_start_index = led_start_index


class WeightDisplay(LEDDisplay):
    FLASH_ON_DURATION = 200
    FLASH_OFF_DURATION = 100
    FLASH_MINIMUM_TIME = 2000
    
    states = Enum('WeightDisplayStates', [ ('SHOW_WEIGHT', 1), ('IDLE', 2),
                                           ('START_FLASH', 3), ('FLASH_OFF', 4),
                                           ('FLASH_ON', 5) ])

    def __init__(self, dendrite, led_start_index):
        super().__init__(f"WeightDisplay {dendrite.dendrite_index}", self.states, led_start_index)
        self.dendrite = dendrite
        self.flash_start_time = -1
        self.flash_finish_requested = False

    def update(self):
        super().update()
        t = now_msecs()
        if self.current_state == self.states.START_FLASH:
            self.flash_start_time = t
            self.flash_finish_requested = False
        elif self.flash_finish_requested and (t - self.flash_start_time) > self.FLASH_MINIMUM_TIME:
            self.transition(self.states.SHOW_WEIGHT)
        elif self.current_state == self.states.START_FLASH or \
           (self.current_state == self.states.FLASH_ON and self.state_duration >= self.FLASH_ON_DURATION):
            display_pattern(DENDRITE_ROTARY_BLANK, self.led_start_index)
            self.transition(self.states.FLASH_OFF)
        elif self.current_state == self.states.FLASH_OFF and self.state_duration >= self.FLASH_OFF_DURATION:
            display_pattern(DENDRITE_ROTARY_COLORS[self.dendrite.weight_index], self.led_start_index)
            self.transition(self.states.FLASH_ON)
        elif self.current_state == self.states.SHOW_WEIGHT:
            display_pattern(DENDRITE_ROTARY_COLORS[self.dendrite.weight_index], self.led_start_index)
            self.transition(self.states.IDLE)
        else:
            pass

    def finish_flash(self):
        self.flash_finish_requested = True


class ThresholdDisplay(LEDDisplay):
    states = Enum('ThresholdDisplayStates', [ ('SHOW_THRESHOLD', 1), ('IDLE', 2)])

    def __init__(self, soma, led_start_index):
        super().__init__('ThresholdDisplay', self.states, led_start_index)
        self.soma = soma

    def update(self):
        super().update()
        if self.current_state == self.states.SHOW_THRESHOLD:
            display_pattern(THRESHOLD_ROTARY_COLORS[self.soma.threshold_index], self.led_start_index)
            self.transition(self.states.IDLE)


class ActivationDisplay(LEDDisplay):
    states = Enum('ActivationDisplayStates', [('IDLE', 1)])

    def __init__(self, soma, led_start_index):
        super().__init__('ActivationDisplay', self.states, led_start_index)
        self.soma = soma
        self.current_value = None

    def update(self):
        super().update()
        activation = self.soma.current_activation
        if self.current_value != activation:
            self.current_value = activation
            display_pattern(ACTIVATION_COLORS[activation], self.led_start_index)


class AxonDisplay(LEDDisplay):
    FLASH_ON_DURATION = 5
    NUM_CYCLES = 1

    states = Enum('AxonStates', [('IDLE', 1),
                                 ('START_FLASH', 2), ('FLASH_ON', 3),
                                 ('SHUTDOWN', 4)])

    def __init__(self, axon, led_start_index):
        super().__init__('AxonDisplay', self.states, led_start_index)
        self.axon = axon

    def update(self):
        super().update()
        t = now_msecs()
        if self.current_state == self.states.START_FLASH:
            self.cycle_count = 0
            self.pattern_index = 0
            self.transition(self.states.FLASH_ON)
        elif self.current_state == self.states.FLASH_ON and \
             self.state_duration >= self.FLASH_ON_DURATION:
            n = NUM_PIXELS_AXON_STRIP
            for i in range(NUM_AXON_STRIPS):
                p = AXON_FIRING_PATTERNS[self.pattern_index]
                rp = list(p).copy()
                rp.reverse()
                if i%2 == 1:
                    display_pattern(p, self.led_start_index + i*n)
                else:
                    display_pattern(rp, self.led_start_index + i*n)
            self.pattern_index += 1
            if self.pattern_index not in AXON_FIRING_PATTERNS:
                self.pattern_index = 0
                self.cycle_count += 1
                if self.cycle_count >= self.NUM_CYCLES:
                    self.transition(self.states.SHUTDOWN)
                    return
            self.transition(self.states.FLASH_ON)
        elif self.current_state == self.states.SHUTDOWN:
            display_pattern(AXON_BLANK_PATTERN, self.led_start_index)
            self.transition(self.states.IDLE)
        else: # idle
            pass


################ Neuron Components ################

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
        self.rotary_switch = DendriteRotarySwitch(self, f"{name} switch", rotary_gpio_pins)
        self.button = Button(self, button_gpio_pin, barrel_gpio_pin, button_audio_channel)
        self.weight_display = WeightDisplay(self, led_start_index)
        self.rotary_audio_channel = rotary_audio_channel
        self.weight_index = 0
        self.transmitted_value = 0

    def update(self):
        self.rotary_switch.update()
        self.button.update()
        self.weight_display.update()
        if self.button.current_value == 0:
            self.transmitted_value = self.WEIGHT_VALUES[self.weight_index]
        else:
            self.transmitted_value = 0

    def increase_weight(self):
        #print(f"increase: dendrite {self.dendrite_index} weight index {self.weight_index} will become {self.rotary_switch.current_value}")
        sound = WEIGHT_INCREASE_SOUNDS[self.dendrite_index][self.weight_index]
        queue_sound(sound, self.rotary_audio_channel)
        self.weight_index = self.rotary_switch.current_value
        self.weight_display.transition(WeightDisplay.states.SHOW_WEIGHT)

    def decrease_weight(self):
        #print(f"decrease: dendrite {self.dendrite_index} weight index {self.weight_index} will become {self.rotary_switch.current_value}")
        sound = WEIGHT_DECREASE_SOUNDS[self.dendrite_index][self.weight_index]
        queue_sound(sound, self.rotary_audio_channel)
        self.weight_index = self.rotary_switch.current_value
        self.weight_display.transition(WeightDisplay.states.SHOW_WEIGHT)



class Soma(StateMachine):
    THRESHOLD_VALUES = { # 16 position switch
         0 :  0.0,
         1 :  0.5,
         2 :  1.0,
         3 :  1.5,
         4 :  2.0,
         5 :  2.5,
         6 :  3.0,
         7 :  3.5,
         8 :  4.0,
         9 : -3.5,
        10 : -3.0,
        11 : -2.5,
        12 : -2.0,
        13 : -1.5,
        14 : -1.0,
        15 : -0.5
    }

    states = Enum('SomaStates', [('STARTUP', 1), ('IDLE', 2)])

    def __init__(self, dendrites, axon, threshold_gpio_pins,
                 activation_led_start_index, threshold_led_start_index,
                 rotary_audio_channel, activation_fire_channel):
        super().__init__('SomaMachine', self.states)
        self.dendrites = dendrites
        self.axon = axon
        self.rotary_switch = ThresholdRotarySwitch(self, threshold_gpio_pins)
        self.activation_display = ActivationDisplay(self, activation_led_start_index)
        self.threshold_display = ThresholdDisplay(self, threshold_led_start_index)
        self.rotary_audio_channel = rotary_audio_channel
        self.activation_fire_channel = activation_fire_channel
        self.threshold_index = 0
        self.current_activation = 0

    def update(self):
        super().update()
        self.rotary_switch.update()
        self.threshold_display.update()
        # compute activation
        new_activation = sum([d.transmitted_value for d in self.dendrites])
        # update activation display -- should have an animation here
        self.current_activation = new_activation
        self.activation_display.update()
        if self.current_state == self.states.STARTUP:
            # Give switches and buttons time to initialize their
            # values before unmuting.
            if self.state_duration > Debouncer.MAX_PERSISTENCE_TIME*1.25:
                plush_sounds.global_mute = False
                self.transition(self.states.IDLE)
        else:  # state is IDLE
            threshold = self.THRESHOLD_VALUES[self.rotary_switch.current_value]
            if new_activation > threshold:
                # print(f"activation {new_activation} > threshold {threshold}: FIRE!")
                self.axon.maybe_fire()

    def increase_threshold(self):
        sound = THRESHOLD_INCREASE_SOUNDS[self.threshold_index]
        queue_sound(sound, self.rotary_audio_channel)
        self.threshold_index = self.rotary_switch.current_value
        print(f"increase threshold: threshold_index now {self.threshold_index}")
        self.threshold_display.transition(ThresholdDisplay.states.SHOW_THRESHOLD)

    def decrease_threshold(self):
        sound = THRESHOLD_DECREASE_SOUNDS[self.threshold_index]
        queue_sound(sound, self.rotary_audio_channel)
        self.threshold_index = self.rotary_switch.current_value
        print(f"decrease threshold: threshold_index now {self.threshold_index}")
        self.threshold_display.transition(ThresholdDisplay.states.SHOW_THRESHOLD)


class Axon(StateMachine):
    AXON_FIRING_DURATION = 1200
    DELAY_FIRING_SOUND = 200

    states = Enum('AxonStates', [('IDLE', 1),
                                 ('FIRE', 2),
                                 ('FIRING_FLASH', 3),
                                 ('FIRING_SOUND', 4)])

    def __init__(self, barrel_pin, led_start_index, activation_fire_channel):
        super().__init__('axon', self.states)
        self.activation_fire_channel = activation_fire_channel
        self.barrel_pin = barrel_pin
        self.axon_display = AxonDisplay(self, led_start_index)
        self.firing_start_time = -1

    def maybe_fire(self):
        if self.current_state == self.states.IDLE:
            self.transition(self.states.FIRE)

    def update(self):
        super().update()
        self.axon_display.update()
        t = now_msecs()
        if self.current_state == self.states.FIRE:
            self.firing_start_time = t
            self.barrel_pin.value = True
            self.transition(self.states.FIRING_FLASH)
        elif self.current_state == self.states.FIRING_FLASH and \
             self.state_duration > self.DELAY_FIRING_SOUND:
            self.axon_display.transition(self.axon_display.states.START_FLASH)
            queue_sound(AXON_FIRE_SOUND, self.activation_fire_channel)
            self.transition(self.states.FIRING_SOUND)
        elif self.current_state == self.states.FIRING_SOUND and \
             (t - self.firing_start_time) > self.AXON_FIRING_DURATION:
            self.axon_display.transition(self.axon_display.states.SHUTDOWN)
            self.barrel_pin.value = False
            self.transition(self.states.IDLE)
        else: # idle
            pass
