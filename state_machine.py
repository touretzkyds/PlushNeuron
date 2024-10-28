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
    def __init__(self, persistence_time):
        self.persistence_time = persistence_time
        self.current_value = None
        self.new_value = None
        self.new_time = -1

    def debounce(self,value):
        if self.current_value == value:
            self.new_value = None
        elif self.current_value == None:
            self.current_value = value
        else:
            t = now_msecs()
            if value == self.new_value:
                if (t - self.new_time) > self.persistence_time:
                    self.current_value = value
            else:
                self.new_value = value
                self.new_time = t
        return self.current_value

BUTTON_PERSISTENCE_TIME = 100 # msecs
ROTARY_PERSISTENCE_TIME = 50 # msecs

button_debouncers = [Debouncer(BUTTON_PERSISTENCE) for i in range(NUM_DENDRITES)]
rotary_debouncers = [Debouncer(ROTARY_PERSISTENCE) for i in range(NUM_DENDRITES + 1)]

class StateMachine():
    def __init__(self,name,index=0,states=()):
        self.name = name
        self.states = states
        self.current_state = states[0]
        self.state_entry_time = 0
        self.state_duration = 0

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

class DendriteRotarySwitchMachine(StateMachine):
    def __init__(self, pins, name, index):
        super().__init__(name, index)
        self.pins = pins
        self.debouncer = Debouncer(ROTARY_PERSISTENCE_TIME)

    def update(self):
        super().update()
        new_value = self.debouncer(decode_pins(self.pins))
        if self.current_value != new_value:
            # play sound
            # LEDs will update themselves
