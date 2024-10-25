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
THRESHOLD_VALUE   = 6
ACTIVATION_FIRE   = 7

channel_ids = [
    DENDRITE_1_BUTTON,
    DENDRITE_1_WEIGHT,
    DENDRITE_2_BUTTON,
    DENDRITE_2_WEIGHT,
    DENDRITE_3_BUTTON,
    DENDRITE_3_WEIGHT,
    THRESHOLD_VALUE,
    ACTIVATION_FIRE
]

channels = [pygame.mixer.Channel(i) for i in channel_ids]
sound_queues = [list() for c in channels]

DENDRITE_1_BUTTON_SOUND = Sound("sounds/organ_C4.ogg")
DENDRITE_2_BUTTON_SOUND = Sound("sounds/organ_E4.ogg")

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
        
