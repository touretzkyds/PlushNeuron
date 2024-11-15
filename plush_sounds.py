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

#pygame.mixer.pre_init(buffer=44100)
pygame.mixer.init()
#pygame.mixer.init(4096, -16, 1, 1024)
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

# index is the starting value of the weight before increase
DENDRITE_1_WEIGHT_INCREASE_SOUNDS = {
    0 : Sound("sounds/Transitions/organ_C-D_fade.ogg"),
    1 : Sound("sounds/Transitions/organ_D-E_fade.ogg"),
    2 : Sound("sounds/Transitions/organ_E-F_fade.ogg"),
    3 : Sound("sounds/Transitions/organ_C-D_fade.ogg"),
    7 : Sound("sounds/Transitions/organ_Ab-Gb_fade.ogg"),
    8 : Sound("sounds/Transitions/organ_Bb-Ab_fade.ogg"),
    9 : Sound("sounds/Transitions/organ_C-Bb_fade.ogg")
}

# index is the starting value of the weight before decrease
DENDRITE_1_WEIGHT_DECREASE_SOUNDS = {
    0 : Sound("sounds/Transitions/organ_C-Bb_fade.ogg"),
    1 : Sound("sounds/Transitions/organ_C-D_fade.ogg"),
    2 : Sound("sounds/Transitions/organ_D-E_fade.ogg"),
    3 : Sound("sounds/Transitions/organ_E-F_fade.ogg"),
    7 : Sound("sounds/Transitions/organ_C-Bb_fade.ogg"),
    8 : Sound("sounds/Transitions/organ_Ab-Gb_fade.ogg"),
    9 : Sound("sounds/Transitions/organ_Bb-Ab_fade.ogg")
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

"""
while True:
    update_all_channels()
    if nothing_to_play():
        cmd = input("cmd? ")
        for ch in cmd:
            if ch == "a":
                queue_sound(DENDRITE_1_BUTTON_SOUND, DENDRITE_1_BUTTON)
            elif ch == "b":
                queue_sound(DENDRITE_2_BUTTON_SOUND, DENDRITE_2_BUTTON)
            else:
                print(f"Unrecognized: '{ch}'")
"""
