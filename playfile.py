import pygame
from pygame.mixer import Sound

pygame.mixer.init()
pygame.init()
pygame.mixer.music.set_volume(0.9) #volume at 90%

channel = pygame.mixer.Channel(0)

filename = "sounds/dendrite3/weight-transitions/trombone_E4-G4.ogg"

print("Playing", filename)

channel.play(Sound(filename))

