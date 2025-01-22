import argparse
import time
import pygame
from pygame.mixer import Sound

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str)

args = parser.parse_args()

pygame.mixer.init()
pygame.init()
pygame.mixer.music.set_volume(0.9) #volume at 90%

channel = pygame.mixer.Channel(0)

#filename = "sounds/dendrite3/weight-transitions/trombone_E4-G4.ogg"
filename = args.filename

print("Playing", filename)

channel.play(Sound(filename))

while channel.get_busy():
    time.sleep(0.1)

