import datetime
from enum import Enum

debug_all = False

start_time = datetime.datetime.now()

def now_msecs():
    diff = datetime.datetime.now() - start_time
    result = diff.seconds*1000 + diff.microseconds/1000
    return result

class StateMachine():
    def __init__(self, name, states : Enum):
        self.name = name
        self.states = states
        self.current_state = list(self.states)[0]
        self.state_entry_time = -1
        self.state_duration = -1
        self.debug = None

    def __repr__(self):
        return f"<StateMachine {self.name} in state {self.current_state}>"

    def set_debug(self, value=True):
        self.debug = value

    def is_debugging(self):
        if self.debug:
            return True
        elif self.debug is None:
            return debug_all
        else:
            return False

    def update(self):
        now = now_msecs()
        self.state_duration = now - self.state_entry_time

    def transition(self, new_state):
        if self.is_debugging():
            print(f"{self} transitioning from {self.current_state} to {new_state}")
        if isinstance(new_state, self.states):
            self.current_state = new_state
            self.state_entry_time = now_msecs()
            self.state_duration = 0
        else:
            print(f"{self.name} transition to invalid state '{new_state}'")
        self.update()
