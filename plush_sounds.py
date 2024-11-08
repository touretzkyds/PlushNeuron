import pygame
from pygame.mixer import Sound

pygame.mixer.init()

# Mixer channels
DENDRITE_1_BUTTON = 0
DENDRITE_1_WEIGHT = 1
DENDRITE_2_BUTTON = 2
DENDRITE_2_WEIGHT = 3
DENDRITE_3_BUTTON = 4
DENDRITE_3_WEIGHT = 5
THRESHOLD_WEIGHT   = 6
ACTIVATION_FIRE   = 7

channel_ids = [
    DENDRITE_1_BUTTON,
    DENDRITE_1_WEIGHT,
    DENDRITE_2_BUTTON,
    DENDRITE_2_WEIGHT,
    DENDRITE_3_BUTTON,
    DENDRITE_3_WEIGHT,
    THRESHOLD_WEIGHT,
    ACTIVATION_FIRE
]

channels = [pygame.mixer.Channel(i) for i in channel_ids]
sound_queues = [list() for c in channels]

DENDRITE_1_WEIGHT_SOUNDS = {
    0 : Sound("sounds/organ_C4.ogg"),   # 0
    1 : Sound("sounds/organ_D4.ogg"),   # +1
    2 : Sound("sounds/organ_E4.ogg"),   # +2
    3 : Sound("sounds/organ_F4.ogg"),   # +3
    7 : Sound("sounds/organ_Gb3.ogg"),  # -3
    8 : Sound("sounds/organ_Ab3.ogg"),  # -2
    9 : Sound("sounds/organ_Bb3.ogg")   # -1
}


# index is the starting value of the weight before increase
DENDRITE_1_WEIGHT_INCREASE_SOUNDS = {
    0 : Sound("sounds/Transitions/organ_C-D_fade.ogg"),
    1 : Sound("sounds/Transitions/organ_D-E_fade.ogg"),
    2 : Sound("sounds/Transitions/organ_E-F_fade.ogg"),
 #   7 : Sound("sounds/Transitions/organ_Gb-Ab_fade.ogg"),
 #   8 : Sound("sounds/Transitions/organ_Ab-Bb_fade.ogg"),
 #   9 : Sound("sounds/Transitions/organ_Bb-C_fade.ogg")
}

# index is the starting value of the weight before decrease
DENDRITE_1_WEIGHT_DECREASE_SOUNDS = {
    0 : Sound("sounds/Transitions/organ_C-Bb_fade.ogg"),
 #   1 : Sound("sounds/Transitions/organ_D-C_fade.ogg"),
 #   2 : Sound("sounds/Transitions/organ_E-D_fade.ogg"),
 #   3 : Sound("sounds/Transitions/organ_F-E_fade.ogg"),
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
DENDRITE_3_BUTTON_SOUND = Sound("sounds/organ_F4.ogg")

DENDRITE_WEIGHT_SOUNDS = [
    DENDRITE_1_WEIGHT_SOUNDS,
    DENDRITE_2_WEIGHT_SOUNDS,
    DENDRITE_3_WEIGHT_SOUNDS
]

DENDRITE_WEIGHT_INCREASE_SOUNDS = [
    DENDRITE_1_WEIGHT_INCREASE_SOUNDS,
    DENDRITE_2_WEIGHT_INCREASE_SOUNDS,
    DENDRITE_3_WEIGHT_INCREASE_SOUNDS
]

DENDRITE_WEIGHT_INCREASE_SOUNDS = [
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

def update_sounds():
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

while True:
    update_sounds()
    if nothing_to_play():
        cmd = input("cmd? ")
        for ch in cmd:
            if ch == "a":
                queue_sound(DENDRITE_1_BUTTON_SOUND, DENDRITE_1_BUTTON)
            elif ch == "b":
                queue_sound(DENDRITE_2_BUTTON_SOUND, DENDRITE_2_BUTTON)
            else:
                print(f"Unrecognized: '{ch}'")
        
