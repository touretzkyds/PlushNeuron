import datetime

NUM_DENDRITES = 3
NUM_ROTARIES = 4

start_time = datetime.datetime.now()

def now_msecs():
    diff = datetime.datetime.now() - start_time
    result = diff.seconds*1000 + diff.microseconds/1000
    return result

"""
**** TREAT ZERO DIFFERENTLY FOR ROTARY SWITCHES ****
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

BUTTON_PERSISTENCE = 100 # msecs
ROTARY_PERSISTENCE = 50 # msecs

button_debouncers = [Debouncer(BUTTON_PERSISTENCE) for i in range(NUM_DENDRITES)]
rotary_debouncers = [Debouncer(ROTARY_PERSISTENCE) for i in range(NUM_DENDRITES + 1)]

