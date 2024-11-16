import pygame
from pygame.mixer import Sound

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
    0 : Sound("sounds/organ_C4.ogg"),   # 0
    1 : Sound("sounds/organ_E4.ogg"),   # +1
    2 : Sound("sounds/organ_G4.ogg"),   # +2
    3 : Sound("sounds/organ_C5.ogg"),   # +3
    4 : Sound("sounds/organ_E5.ogg"),   # +4
    6 : Sound("sounds/organ_B2.ogg"),   # -4
    7 : Sound("sounds/organ_D#3.ogg"),  # -3
    8 : Sound("sounds/organ_F#3.ogg"),  # -2
    9 : Sound("sounds/organ_A3.ogg")   # -1
}


# Tones for dendrite weights:
# -4  -3  -2 -1  0  1  2  3  4
# B2 D#3 F#3 A3 C4 E4 G4 C5 E5

# index is the starting value of the rotary switch before increase
DENDRITE_1_WEIGHT_INCREASE_SOUNDS = {
    0 : Sound("sounds/Transitions/C4-E4.ogg"),
    1 : Sound("sounds/Transitions/E4-G4.ogg"),
    2 : Sound("sounds/Transitions/G4-C5.ogg"),
    3 : Sound("sounds/Transitions/C5-E5.ogg"),
    4 : Sound("sounds/organ_B2.ogg"),  # shouldn't need this
    # 5 is not used
    6 : Sound("sounds/Transitions/B2-D#3.ogg"),
    7 : Sound("sounds/Transitions/D#3-F#3.ogg"),
    8 : Sound("sounds/Transitions/F#3-A3.ogg"),
    9 : Sound("sounds/Transitions/A3-C4.ogg")
}

# index is the starting value of the rotary switch before decrease
DENDRITE_1_WEIGHT_DECREASE_SOUNDS = {
    0 : Sound("sounds/Transitions/C4-A3.ogg"),
    1 : Sound("sounds/Transitions/E4-C4.ogg"),
    2 : Sound("sounds/Transitions/G4-E4.ogg"),
    3 : Sound("sounds/Transitions/C5-G4.ogg"),
    4 : Sound("sounds/Transitions/E5-C5.ogg"),
    # 5 is not used
    6 : Sound("sounds/organ_E5.ogg"), # shouldn't need this
    7 : Sound("sounds/Transitions/D#3-B2.ogg"),
    8 : Sound("sounds/Transitions/F#3-D#3.ogg"),
    9 : Sound("sounds/Transitions/A3-F#3.ogg")
}

DENDRITE_2_WEIGHT_SOUNDS = DENDRITE_1_WEIGHT_SOUNDS
DENDRITE_2_WEIGHT_INCREASE_SOUNDS = DENDRITE_1_WEIGHT_INCREASE_SOUNDS
DENDRITE_2_WEIGHT_DECREASE_SOUNDS = DENDRITE_1_WEIGHT_DECREASE_SOUNDS 

DENDRITE_3_WEIGHT_SOUNDS = DENDRITE_1_WEIGHT_SOUNDS
DENDRITE_3_WEIGHT_INCREASE_SOUNDS = DENDRITE_1_WEIGHT_INCREASE_SOUNDS
DENDRITE_3_WEIGHT_DECREASE_SOUNDS = DENDRITE_1_WEIGHT_DECREASE_SOUNDS 

# Temporary hacks
DENDRITE_1_BUTTON_SOUND = Sound("sounds/organ_C4.ogg")
DENDRITE_2_BUTTON_SOUND = Sound("sounds/organ_E4.ogg")
DENDRITE_3_BUTTON_SOUND = Sound("sounds/organ_G4.ogg")

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


DENDRITE_BUTTON_SOUNDS = [
    DENDRITE_1_BUTTON_SOUND,
    DENDRITE_2_BUTTON_SOUND,
    DENDRITE_3_BUTTON_SOUND
]

# Tones for dendrite weights:
# -4  -3  -2 -1  0  1  2  3  4
# B2 D#3 F#3 A3 C4 E4 G4 C5 E5


# Tones for threshold weights:
# -3.5  -3.0  -2.5  -2.0  -1.5  -1.0  -0.5  0.0  0.5  1.0  1.5  2.0  2.5  3.0  3.5
#  C3    D3    E3    F3    G3    A3    B3   C4   D4   E4   F4   G4   A#4  C5   D5

THRESHOLD_INCREASE_SOUNDS = {}

THRESHOLD_DECREASE_SOUNDS = {}

def queue_sound(sound, channel_id):
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
