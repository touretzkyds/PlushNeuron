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

DENDRITE_1_WEIGHT_SOUNDS = {
    0 : Sound("sounds/dendrite1/organ_C4.ogg"),   #  0
    1 : Sound("sounds/dendrite1/organ_E4.ogg"),   # +1
    2 : Sound("sounds/dendrite1/organ_G4.ogg"),   # +2
    3 : Sound("sounds/dendrite1/organ_C5.ogg"),   # +3
    4 : Sound("sounds/dendrite1/organ_E5.ogg"),   # +4
    # 5 is not used
    6 : Sound("sounds/dendrite1/organ_B2.ogg"),   # -4
    7 : Sound("sounds/dendrite1/organ_D#3.ogg"),  # -3
    8 : Sound("sounds/dendrite1/organ_F#3.ogg"),  # -2
    9 : Sound("sounds/dendrite1/organ_A3.ogg")    # -1
}


# Tones for dendrite weights:
# -4  -3  -2 -1  0  1  2  3  4
# B2 D#3 F#3 A3 C4 E4 G4 C5 E5

# index is the starting value of the rotary switch before increase
DENDRITE_1_WEIGHT_INCREASE_SOUNDS = {
    0 : Sound("sounds/dendrite1/weight-transitions/organ_C4-E4.ogg"),
    1 : Sound("sounds/dendrite1/weight-transitions/organ_E4-G4.ogg"),
    2 : Sound("sounds/dendrite1/weight-transitions/organ_G4-C5.ogg"),
    3 : Sound("sounds/dendrite1/weight-transitions/organ_C5-E5.ogg"),
    # 4 is not used
    # 5 is not used
    6 : Sound("sounds/dendrite1/weight-transitions/organ_B2-D#3.ogg"),
    7 : Sound("sounds/dendrite1/weight-transitions/organ_D#3-F#3.ogg"),
    8 : Sound("sounds/dendrite1/weight-transitions/organ_F#3-A3.ogg"),
    9 : Sound("sounds/dendrite1/weight-transitions/organ_A3-C4.ogg")
}

# index is the starting value of the rotary switch before decrease
DENDRITE_1_WEIGHT_DECREASE_SOUNDS = {
    0 : Sound("sounds/dendrite1/weight-transitions/organ_C4-A3.ogg"),
    1 : Sound("sounds/dendrite1/weight-transitions/organ_E4-C4.ogg"),
    2 : Sound("sounds/dendrite1/weight-transitions/organ_G4-E4.ogg"),
    3 : Sound("sounds/dendrite1/weight-transitions/organ_C5-G4.ogg"),
    4 : Sound("sounds/dendrite1/weight-transitions/organ_E5-C5.ogg"),
    # 5 is not used
    # 6 is not used
    7 : Sound("sounds/dendrite1/weight-transitions/organ_D#3-B2.ogg"),
    8 : Sound("sounds/dendrite1/weight-transitions/organ_F#3-D#3.ogg"),
    9 : Sound("sounds/dendrite1/weight-transitions/organ_A3-F#3.ogg")
}

DENDRITE_2_WEIGHT_SOUNDS = {
    0 : Sound("sounds/dendrite2/clarinet_C4.ogg"),   #  0
    1 : Sound("sounds/dendrite2/clarinet_E4.ogg"),   # +1
    2 : Sound("sounds/dendrite2/clarinet_G4.ogg"),   # +2
    3 : Sound("sounds/dendrite2/clarinet_C5.ogg"),   # +3
    4 : Sound("sounds/dendrite2/clarinet_E5.ogg"),   # +4
    # 5 is not used
    6 : Sound("sounds/dendrite2/clarinet_B2.ogg"),   # -4
    7 : Sound("sounds/dendrite2/clarinet_D#3.ogg"),  # -3
    8 : Sound("sounds/dendrite2/clarinet_F#3.ogg"),  # -2
    9 : Sound("sounds/dendrite2/clarinet_A3.ogg")    # -1
}

# index is the starting value of the rotary switch before increase
DENDRITE_2_WEIGHT_INCREASE_SOUNDS = {
    0 : Sound("sounds/dendrite2/weight-transitions/clarinet_C4-E4.ogg"),
    1 : Sound("sounds/dendrite2/weight-transitions/clarinet_E4-G4.ogg"),
    2 : Sound("sounds/dendrite2/weight-transitions/clarinet_G4-C5.ogg"),
    3 : Sound("sounds/dendrite2/weight-transitions/clarinet_C5-E5.ogg"),
    # 4 is not used
    # 5 is not used
    6 : Sound("sounds/dendrite2/weight-transitions/clarinet_B2-D#3.ogg"),
    7 : Sound("sounds/dendrite2/weight-transitions/clarinet_D#3-F#3.ogg"),
    8 : Sound("sounds/dendrite2/weight-transitions/clarinet_F#3-A3.ogg"),
    9 : Sound("sounds/dendrite2/weight-transitions/clarinet_A3-C4.ogg")
}

# index is the starting value of the rotary switch before decrease
DENDRITE_2_WEIGHT_DECREASE_SOUNDS = {
    0 : Sound("sounds/dendrite2/weight-transitions/clarinet_C4-A3.ogg"),
    1 : Sound("sounds/dendrite2/weight-transitions/clarinet_E4-C4.ogg"),
    2 : Sound("sounds/dendrite2/weight-transitions/clarinet_G4-E4.ogg"),
    3 : Sound("sounds/dendrite2/weight-transitions/clarinet_C5-G4.ogg"),
    4 : Sound("sounds/dendrite2/weight-transitions/clarinet_E5-C5.ogg"),
    # 5 is not used
    # 6 is not used
    7 : Sound("sounds/dendrite2/weight-transitions/clarinet_D#3-B2.ogg"),
    8 : Sound("sounds/dendrite2/weight-transitions/clarinet_F#3-D#3.ogg"),
    9 : Sound("sounds/dendrite2/weight-transitions/clarinet_A3-F#3.ogg")
}

DENDRITE_3_WEIGHT_SOUNDS = {
    0 : Sound("sounds/dendrite3/trombone_C4.ogg"),   #  0
    1 : Sound("sounds/dendrite3/trombone_E4.ogg"),   # +1
    2 : Sound("sounds/dendrite3/trombone_G4.ogg"),   # +2
    3 : Sound("sounds/dendrite3/trombone_C5.ogg"),   # +3
    4 : Sound("sounds/dendrite3/trombone_E5.ogg"),   # +4
    # 5 is not used
    6 : Sound("sounds/dendrite3/trombone_B2.ogg"),   # -4
    7 : Sound("sounds/dendrite3/trombone_D#3.ogg"),  # -3
    8 : Sound("sounds/dendrite3/trombone_F#3.ogg"),  # -2
    9 : Sound("sounds/dendrite3/trombone_A3.ogg")    # -1
}

# index is the starting value of the rotary switch before increase
DENDRITE_3_WEIGHT_INCREASE_SOUNDS = {
    0 : Sound("sounds/dendrite3/weight-transitions/trombone_C4-E4.ogg"),
    1 : Sound("sounds/dendrite3/weight-transitions/trombone_E4-G4.ogg"),
    2 : Sound("sounds/dendrite3/weight-transitions/trombone_G4-C5.ogg"),
    3 : Sound("sounds/dendrite3/weight-transitions/trombone_C5-E5.ogg"),
    # 4 is not used
    # 5 is not used
    6 : Sound("sounds/dendrite3/weight-transitions/trombone_B2-D#3.ogg"),
    7 : Sound("sounds/dendrite3/weight-transitions/trombone_D#3-F#3.ogg"),
    8 : Sound("sounds/dendrite3/weight-transitions/trombone_F#3-A3.ogg"),
    9 : Sound("sounds/dendrite3/weight-transitions/trombone_A3-C4.ogg")
}

# index is the starting value of the rotary switch before decrease
DENDRITE_3_WEIGHT_DECREASE_SOUNDS = {
    0 : Sound("sounds/dendrite3/weight-transitions/trombone_C4-A3.ogg"),
    1 : Sound("sounds/dendrite3/weight-transitions/trombone_E4-C4.ogg"),
    2 : Sound("sounds/dendrite3/weight-transitions/trombone_G4-E4.ogg"),
    3 : Sound("sounds/dendrite3/weight-transitions/trombone_C5-G4.ogg"),
    4 : Sound("sounds/dendrite3/weight-transitions/trombone_E5-C5.ogg"),
    # 5 is not used
    # 6 is not used
    7 : Sound("sounds/dendrite3/weight-transitions/trombone_D#3-B2.ogg"),
    8 : Sound("sounds/dendrite3/weight-transitions/trombone_F#3-D#3.ogg"),
    9 : Sound("sounds/dendrite3/weight-transitions/trombone_A3-F#3.ogg")
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
# -3.5  -3.0  -2.5  -2.0  -1.5  -1.0  -0.5  0.0  0.5  1.0  1.5  2.0  2.5  3.0  3.5
#  C3    D3    E3    F3    G3    A3    B3   C4   D4   E4   F4   G4   A#4  C5   D5

# index is the starting value of the rotary switch before increase
THRESHOLD_INCREASE_SOUNDS = {
     0 : Sound("sounds/threshold-transitions/C4-D4.ogg"),   #  0.0
     1 : Sound("sounds/threshold-transitions/D4-E4.ogg"),   #  0.5
     2 : Sound("sounds/threshold-transitions/E4-F4.ogg"),   #  1.0
     3 : Sound("sounds/threshold-transitions/F4-G4.ogg"),   #  1.5
     4 : Sound("sounds/threshold-transitions/G4-A#4.ogg"),  #  2.0
     5 : Sound("sounds/threshold-transitions/A#4-C5.ogg"),  #  2.5
     6 : Sound("sounds/threshold-transitions/C5-D5.ogg"),   #  3.0
     # 7 is a valid weight but no increase transition
     7 : Sound("shutter16.wav"),
     # 8 is not used
     8 : Sound("shutter16.wav"),
     9 : Sound("sounds/threshold-transitions/C3-D3.ogg"),   # -3.5
    10 : Sound("sounds/threshold-transitions/D3-E3.ogg"),   # -3.0
    11 : Sound("sounds/threshold-transitions/E3-F3.ogg"),   # -2.5
    12 : Sound("sounds/threshold-transitions/F3-G3.ogg"),   # -2.0
    13 : Sound("sounds/threshold-transitions/G3-A3.ogg"),   # -1.5
    14 : Sound("sounds/threshold-transitions/A3-B3.ogg"),   # -1.0
    15 : Sound("sounds/threshold-transitions/B3-C4.ogg")    # -0.5
}

# index is the starting value of the rotary switch before decrease
THRESHOLD_DECREASE_SOUNDS = {
     0 : Sound("sounds/threshold-transitions/C4-B3.ogg"),   #  0.0
     1 : Sound("sounds/threshold-transitions/D4-C4.ogg"),   #  0.5
     2 : Sound("sounds/threshold-transitions/E4-D4.ogg"),   #  1.0
     3 : Sound("sounds/threshold-transitions/F4-E4.ogg"),   #  1.5
     4 : Sound("sounds/threshold-transitions/G4-F4.ogg"),   #  2.0
     5 : Sound("sounds/threshold-transitions/A#4-G4.ogg"),  #  2.5
     6 : Sound("sounds/threshold-transitions/C5-A#4.ogg"),  #  3.0
     7 : Sound("sounds/threshold-transitions/D5-C5.ogg"),   #  3.5
     # 8 is not used
     8 : Sound("shutter16.wav"),
     # 9 is a valid weight but no decrease transition
     9 : Sound("shutter16.wav"),
    10 : Sound("sounds/threshold-transitions/D3-C3.ogg"),   # -3.0
    11 : Sound("sounds/threshold-transitions/E3-D3.ogg"),   # -2.5
    12 : Sound("sounds/threshold-transitions/F3-E3.ogg"),   # -2.0
    13 : Sound("sounds/threshold-transitions/G3-F3.ogg"),   # -1.5
    14 : Sound("sounds/threshold-transitions/A3-G3.ogg"),   # -1.0
    15 : Sound("sounds/threshold-transitions/B3-A3.ogg")    # -0.5
}

AXON_FIRE_SOUND = Sound("sounds/8-bit-laser.ogg")

def queue_sound(sound, channel_id):
    if global_mute:
        return
    # play sound if channel is free, else queue it for later
    if not channels[channel_id].get_busy():
        channels[channel_id].play(sound)
    else:
        sound_queues[channel_id].append(sound)

def update_all_channels():
    # if any queued sounds have become eligible to play, play them
    for id in channel_ids:
        if sound_queues[id]:
            if not channels[id].get_busy():
                sound = sound_queues[id].pop(0)
                channels[id].play(sound)

def nothing_to_play():
    for id in channel_ids:
        if sound_queues[id] or channels[id].get_busy():
            return False
    return True
