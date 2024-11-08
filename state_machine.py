import datetime

NUM_DENDRITES = 3
NUM_ROTARIES = 4

start_time = datetime.datetime.now()

def now_msecs():
    diff = datetime.datetime.now() - start_time
    result = diff.seconds*1000 + diff.microseconds/1000
    return result

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
    def __init__(self, name, index, gpio_pins):
        super().__init__(name, index)
        self.gpio_pins = gpio_pins
        self.debouncer = Debouncer(Debouncer.ROTARY_PERSISTENCE_TIME)

    def decode_switch(pins):
        value = 0
        for i in range(len(gpio_pins)):
            if self.gpio_pins[i].value == False:
                value += (1 << i)
        return value


class DendriteRotarySwitch(RotarySwitch):
    def update(self):
        new_value = self.debouncer(decode_pins(self.pins))
        if (self.current_value < new_value or new_value == 0) and self.dendrite.WEIGHT_VALUES.get(new_value):
            self.dendrite.increase_weight()
        elif (self.current_value > new_value or self.current_value == 0) and self.dendrite.WEIGHT_VALUES.get(new_value):
            self.dendrite.decrease_weight()
        else:
            pass  # ignored switch position

        
class BodyRotarySwitch(RotarySwitch):
    pass


class Dendrite():
    WEIGHT_VALUES = { # 10 position switch
        0 : 0,
        1 : 1,
        2 : 2,
        3 : 3,
        4 : 4,
        5 : None,
        6 : -4,
        7 : -3,
        8 : -2,
        9 : -1
    }

    def __init__(self, name, dendrite_index, gpio_pins, led_start_index,
                 switch_audio_channel, button_audio_channel):
        self.name = name
        self.dendrite_index = dendrite_index
        self.rotary_switch = DendriteRotarySwitch(name, gpio_pins)
        self.rotary_switch.dendrite = self
        self.led_start_index = led_start_index
        self.switch_audio_channel = switch_audio_channel
        self.button_audio_channel = button_audio_channel
        self.weight_index = 0

    def increase_weight(self):
        sound = WEIGHT_INCREASE_SOUNDS[self.dendrite_index][self.weight_index]
        queue_sound(sound, self.switch_audio_channel)
        self.weight_index += 1
        if self.weight_index not in WEIGHT_VALUES:  # wrap around
            self.weight_index = 0
        display_pattern(DENDRITE_ROTARY_COLORS, self.led_start_index, self.weight_index)

    def decrease_weight(self):
        sound = WEIGHT_DECREASE_SOUNDS[self.dendrite_index][self.weight_index]
        queue_sound(sound, self.switch_audio_channel)
        self.weight_index -= 1
        if self.weight_index not in WEIGHT_VALUES:  # wrap around
            self.weight_index = max(WEIGHT_VALUES.keys())
        display_pattern(DENDRITE_ROTARY_COLORS, self.led_start_index, self.weight_index)


class StateMachine():
    def __init__(self,name,index=None,states=()):
        self.name = name
        self.states = states
        self.current_state = states[0]
        self.state_entry_time = -1
        self.state_duration = -1

    def update():
        now = now_msecs()
        self.state_duration = now - self.state_entry_time

    def transition(new_state):
        if new_state in self.states:
            self.current_state = new_state
            sef.state_entry_time = now_msecs()
            self.state_duration = 0
        else:
            print(f"{self.name} transition to invalid state '{new_state}'")

