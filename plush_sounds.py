import pygame
from pygame.mixer import Sound

global_mute = True   # for silence on start-up

# Mixer channels
DENDRITE_1_BUTTON_CHANNEL = 0
DENDRITE_1_WEIGHT_CHANNEL = 1
DENDRITE_2_BUTTON_CHANNEL = 2
DENDRITE_2_WEIGHT_CHANNEL = 3
DENDRITE_3_BUTTON_CHANNEL = 4
DENDRITE_3_WEIGHT_CHANNEL = 5
THRESHOLD_WEIGHT_CHANNEL  = 6
ACTIVATION_FIRE_CHANNEL   = 7

channel_ids = [
    DENDRITE_1_BUTTON_CHANNEL,
    DENDRITE_1_WEIGHT_CHANNEL,
    DENDRITE_2_BUTTON_CHANNEL,
    DENDRITE_2_WEIGHT_CHANNEL,
    DENDRITE_3_BUTTON_CHANNEL,
    DENDRITE_3_WEIGHT_CHANNEL,
    THRESHOLD_WEIGHT_CHANNEL,
    ACTIVATION_FIRE_CHANNEL
]

pygame.mixer.init()
pygame.mixer.music.set_volume(0.9) #volume at 90%
channels = [pygame.mixer.Channel(i) for i in channel_ids]

sound_queues = [list() for c in channels]

class PlushSound(Sound):
    def __init__(self, filename):
        super().__init__(filename)
        self.filename = filename


DENDRITE_1_WEIGHT_SOUNDS = {
    0 : PlushSound("sounds/dendrite1/clarinet_C4.mp3"),   #  0
    1 : PlushSound("sounds/dendrite1/clarinet_E4.mp3"),   # +1
    2 : PlushSound("sounds/dendrite1/clarinet_G4.mp3"),   # +2
    3 : PlushSound("sounds/dendrite1/clarinet_C5.mp3"),   # +3
    4 : PlushSound("sounds/dendrite1/clarinet_E5.mp3"),   # +4
    # 5 is not used
    6 : PlushSound("sounds/dendrite1/clarinet_B2.mp3"),   # -4
    7 : PlushSound("sounds/dendrite1/clarinet_D#3.mp3"),  # -3
    8 : PlushSound("sounds/dendrite1/clarinet_F#3.mp3"),  # -2
    9 : PlushSound("sounds/dendrite1/clarinet_A3.mp3")    # -1
}


# Tones for dendrite weights:
# -4  -3  -2 -1  0  1  2  3  4
# B2 D#3 F#3 A3 C4 E4 G4 C5 E5

# index is the starting value of the rotary switch before increase
DENDRITE_1_WEIGHT_INCREASE_SOUNDS = {
    0 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_C4-E4.mp3"),
    1 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_E4-G4.mp3"),
    2 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_G4-C5.mp3"),
    3 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_C5-E5.mp3"),
    # 4 is not used
    # 5 is not used
    6 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_B2-D#3.mp3"),
    7 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_D#3-F#3.mp3"),
    8 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_F#3-A3.mp3"),
    9 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_A3-C4.mp3")
}

# index is the starting value of the rotary switch before decrease
DENDRITE_1_WEIGHT_DECREASE_SOUNDS = {
    0 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_C4-A3.mp3"),
    1 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_E4-C4.mp3"),
    2 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_G4-E4.mp3"),
    3 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_C5-G4.mp3"),
    4 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_E5-C5.mp3"),
    # 5 is not used
    # 6 is not used
    7 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_D#3-B2.mp3"),
    8 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_F#3-D#3.mp3"),
    9 : PlushSound("sounds/dendrite1/weight-transitions/clarinet_A3-F#3.mp3")
}

DENDRITE_2_WEIGHT_SOUNDS = {
    0 : PlushSound("sounds/dendrite2/oud_C4.mp3"),   #  0
    1 : PlushSound("sounds/dendrite2/oud_E4.mp3"),   # +1
    2 : PlushSound("sounds/dendrite2/oud_G4.mp3"),   # +2
    3 : PlushSound("sounds/dendrite2/oud_C5.mp3"),   # +3
    4 : PlushSound("sounds/dendrite2/oud_E5.mp3"),   # +4
    # 5 is not used
    6 : PlushSound("sounds/dendrite2/oud_B2.mp3"),   # -4
    7 : PlushSound("sounds/dendrite2/oud_D#3.mp3"),  # -3
    8 : PlushSound("sounds/dendrite2/oud_F#3.mp3"),  # -2
    9 : PlushSound("sounds/dendrite2/oud_A3.mp3")    # -1
}

# index is the starting value of the rotary switch before increase
DENDRITE_2_WEIGHT_INCREASE_SOUNDS = {
    0 : PlushSound("sounds/dendrite2/weight-transitions/oud_C4-E4.mp3"),
    1 : PlushSound("sounds/dendrite2/weight-transitions/oud_E4-G4.mp3"),
    2 : PlushSound("sounds/dendrite2/weight-transitions/oud_G4-C5.mp3"),
    3 : PlushSound("sounds/dendrite2/weight-transitions/oud_C5-E5.mp3"),
    # 4 is not used
    # 5 is not used
    6 : PlushSound("sounds/dendrite2/weight-transitions/oud_B2-D#3.mp3"),
    7 : PlushSound("sounds/dendrite2/weight-transitions/oud_D#3-F#3.mp3"),
    8 : PlushSound("sounds/dendrite2/weight-transitions/oud_F#3-A3.mp3"),
    9 : PlushSound("sounds/dendrite2/weight-transitions/oud_A3-C4.mp3")
}

# index is the starting value of the rotary switch before decrease
DENDRITE_2_WEIGHT_DECREASE_SOUNDS = {
    0 : PlushSound("sounds/dendrite2/weight-transitions/oud_C4-A3.mp3"),
    1 : PlushSound("sounds/dendrite2/weight-transitions/oud_E4-C4.mp3"),
    2 : PlushSound("sounds/dendrite2/weight-transitions/oud_G4-E4.mp3"),
    3 : PlushSound("sounds/dendrite2/weight-transitions/oud_C5-G4.mp3"),
    4 : PlushSound("sounds/dendrite2/weight-transitions/oud_E5-C5.mp3"),
    # 5 is not used
    # 6 is not used
    7 : PlushSound("sounds/dendrite2/weight-transitions/oud_D#3-B2.mp3"),
    8 : PlushSound("sounds/dendrite2/weight-transitions/oud_F#3-D#3.mp3"),
    9 : PlushSound("sounds/dendrite2/weight-transitions/oud_A3-F#3.mp3")
}

DENDRITE_3_WEIGHT_SOUNDS = {
    0 : PlushSound("sounds/dendrite3/saxophone_C4.mp3"),   #  0
    1 : PlushSound("sounds/dendrite3/saxophone_E4.mp3"),   # +1
    2 : PlushSound("sounds/dendrite3/saxophone_G4.mp3"),   # +2
    3 : PlushSound("sounds/dendrite3/saxophone_C5.mp3"),   # +3
    4 : PlushSound("sounds/dendrite3/saxophone_E5.mp3"),   # +4
    # 5 is not used
    6 : PlushSound("sounds/dendrite3/saxophone_B2.mp3"),   # -4
    7 : PlushSound("sounds/dendrite3/saxophone_D#3.mp3"),  # -3
    8 : PlushSound("sounds/dendrite3/saxophone_F#3.mp3"),  # -2
    9 : PlushSound("sounds/dendrite3/saxophone_A3.mp3")    # -1
}

# index is the starting value of the rotary switch before increase
DENDRITE_3_WEIGHT_INCREASE_SOUNDS = {
    0 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_C4-E4.mp3"),
    1 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_E4-G4.mp3"),
    2 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_G4-C5.mp3"),
    3 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_C5-E5.mp3"),
    # 4 is not used
    # 5 is not used
    6 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_B2-D#3.mp3"),
    7 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_D#3-F#3.mp3"),
    8 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_F#3-A3.mp3"),
    9 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_A3-C4.mp3")
}

# index is the starting value of the rotary switch before decrease
DENDRITE_3_WEIGHT_DECREASE_SOUNDS = {
    0 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_C4-A3.mp3"),
    1 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_E4-C4.mp3"),
    2 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_G4-E4.mp3"),
    3 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_C5-G4.mp3"),
    4 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_E5-C5.mp3"),
    # 5 is not used
    # 6 is not used
    7 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_D#3-B2.mp3"),
    8 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_F#3-D#3.mp3"),
    9 : PlushSound("sounds/dendrite3/weight-transitions/saxophone_A3-F#3.mp3")
}

WEIGHT_SOUNDS = [
    DENDRITE_1_WEIGHT_SOUNDS,
    DENDRITE_2_WEIGHT_SOUNDS,
    DENDRITE_3_WEIGHT_SOUNDS
]

WEIGHT_INCREASE_SOUNDS = [
    DENDRITE_1_WEIGHT_INCREASE_SOUNDS,
    DENDRITE_2_WEIGHT_INCREASE_SOUNDS,
    DENDRITE_3_WEIGHT_INCREASE_SOUNDS
]

WEIGHT_DECREASE_SOUNDS = [
    DENDRITE_1_WEIGHT_DECREASE_SOUNDS,
    DENDRITE_2_WEIGHT_DECREASE_SOUNDS,
    DENDRITE_3_WEIGHT_DECREASE_SOUNDS
]


# Tones for dendrite weights:
# -4  -3  -2 -1  0  1  2  3  4
# B2 D#3 F#3 A3 C4 E4 G4 C5 E5


# Tones for threshold weights:
# -3.5  -3.0  -2.5  -2.0  -1.5  -1.0  -0.5  0.0  0.5  1.0  1.5  2.0  2.5  3.0  3.5  4.0
#  C3    D3    E3    F3    G3    A3    B3   C4   D4   E4   F4   G4   A#4  C5   D5   E5

# index is the starting value of the rotary switch before increase
THRESHOLD_INCREASE_SOUNDS = {
     0 : PlushSound("sounds/threshold-transitions/accordion_C4-D4.mp3"),   #  0.0
     1 : PlushSound("sounds/threshold-transitions/accordion_D4-E4.mp3"),   #  0.5
     2 : PlushSound("sounds/threshold-transitions/accordion_E4-F4.mp3"),   #  1.0
     3 : PlushSound("sounds/threshold-transitions/accordion_F4-G4.mp3"),   #  1.5
     4 : PlushSound("sounds/threshold-transitions/accordion_G4-A#4.mp3"),  #  2.0
     5 : PlushSound("sounds/threshold-transitions/accordion_A#4-C5.mp3"),  #  2.5
     6 : PlushSound("sounds/threshold-transitions/accordion_C5-D5.mp3"),   #  3.0
     7 : PlushSound("sounds/threshold-transitions/accordion_D5-E5.mp3"),   #  3.5
     8 : PlushSound("sounds/threshold-transitions/accordion_E5-C3.mp3"),   #  4,0 wrap
     9 : PlushSound("sounds/threshold-transitions/accordion_C3-D3.mp3"),   # -3.5
    10 : PlushSound("sounds/threshold-transitions/accordion_D3-E3.mp3"),   # -3.0
    11 : PlushSound("sounds/threshold-transitions/accordion_E3-F3.mp3"),   # -2.5
    12 : PlushSound("sounds/threshold-transitions/accordion_F3-G3.mp3"),   # -2.0
    13 : PlushSound("sounds/threshold-transitions/accordion_G3-A3.mp3"),   # -1.5
    14 : PlushSound("sounds/threshold-transitions/accordion_A3-B3.mp3"),   # -1.0
    15 : PlushSound("sounds/threshold-transitions/accordion_B3-C4.mp3")    # -0.5
}

# index is the starting value of the rotary switch before decrease
THRESHOLD_DECREASE_SOUNDS = {
     0 : PlushSound("sounds/threshold-transitions/accordion_C4-B3.mp3"),   #  0.0
     1 : PlushSound("sounds/threshold-transitions/accordion_D4-C4.mp3"),   #  0.5
     2 : PlushSound("sounds/threshold-transitions/accordion_E4-D4.mp3"),   #  1.0
     3 : PlushSound("sounds/threshold-transitions/accordion_F4-E4.mp3"),   #  1.5
     4 : PlushSound("sounds/threshold-transitions/accordion_G4-F4.mp3"),   #  2.0
     5 : PlushSound("sounds/threshold-transitions/accordion_A#4-G4.mp3"),  #  2.5
     6 : PlushSound("sounds/threshold-transitions/accordion_C5-A#4.mp3"),  #  3.0
     7 : PlushSound("sounds/threshold-transitions/accordion_D5-C5.mp3"),   #  3.5
     8 : PlushSound("sounds/threshold-transitions/accordion_E5-D5.mp3"),   #  4.0
     9 : PlushSound("sounds/threshold-transitions/accordion_C3-E5.mp3"),   # -3.5 wrap
    10 : PlushSound("sounds/threshold-transitions/accordion_D3-C3.mp3"),   # -3.0
    11 : PlushSound("sounds/threshold-transitions/accordion_E3-D3.mp3"),   # -2.5
    12 : PlushSound("sounds/threshold-transitions/accordion_F3-E3.mp3"),   # -2.0
    13 : PlushSound("sounds/threshold-transitions/accordion_G3-F3.mp3"),   # -1.5
    14 : PlushSound("sounds/threshold-transitions/accordion_A3-G3.mp3"),   # -1.0
    15 : PlushSound("sounds/threshold-transitions/accordion_B3-A3.mp3")    # -0.5
}

AXON_FIRE_SOUND = PlushSound("sounds/8-bit-laser.ogg")

def queue_sound(sound, channel_id):
    if global_mute:
        return
    # play sound if channel is free, else queue it for later
    if not channels[channel_id].get_busy():
        print(f'playing {sound.filename}')
        channels[channel_id].play(sound)
    else:
        sound_queues[channel_id].append(sound)

def update_all_channels():
    # if any queued sounds have become eligible to play, play them
    for id in channel_ids:
        if sound_queues[id]:
            if not channels[id].get_busy():
                sound = sound_queues[id].pop(0)
                print(f'playing {sound.filename}')
                channels[id].play(sound)

def nothing_to_play():
    for id in channel_ids:
        if sound_queues[id] or channels[id].get_busy():
            return False
    return True
