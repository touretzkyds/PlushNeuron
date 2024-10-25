import digitalio
import board
import time
import datetime
import adafruit_dotstar as dotstar
import pygame
import pygame.mixer
import RPi.GPIO as GPIO

start_time = datetime.datetime.now()

def now_msecs():
    diff = datetime.datetime.now() - start_time
    value = diff.seconds*1000 + diff.microseconds/1000
    return value

# Initialize pygame for sound
#pygame.mixer.pre_init(buffer=44100)
pygame.mixer.init(4096, -16, 1, 1024)
pygame.mixer.music.set_volume(0.9) #volume at 90%

# Load the sound file
sound_file = "/home/csoska/Desktop/Neuron/zap4096.ogg"
#sound_file2 = "/home/csoska/Desktop/Neuron/zap-e.wav"
#sound_file3 = "/home/csoska/Desktop/Neuron/zap-g.wav"
pygame.mixer.music.load(sound_file)

GPIO.setmode(GPIO.BCM) #forcing to headphone out

# Button input with pull-down resistor (looking for HIGH on press)
pin1 = digitalio.DigitalInOut(board.D27) #expects button press on D27
pin1.direction = digitalio.Direction.INPUT #sets D27 as input
pin1.pull = digitalio.Pull.UP #pull-up enabled

pin2 = digitalio.DigitalInOut(board.D23) #expects button press on D23
pin2.direction = digitalio.Direction.INPUT #sets D23 as input
pin2.pull = digitalio.Pull.UP #pull-up enabled

pin3 = digitalio.DigitalInOut(board.D26) #expects button press on D26
pin3.direction = digitalio.Direction.INPUT #sets D26 as input
pin3.pull = digitalio.Pull.UP #pull-up enabled


dendrite1_pins = [digitalio.DigitalInOut(board.D2), digitalio.DigitalInOut(board.D3),
		digitalio.DigitalInOut(board.D4), digitalio.DigitalInOut(board.D17)]

dendrite2_pins = [digitalio.DigitalInOut(board.D7), digitalio.DigitalInOut(board.D8),
		digitalio.DigitalInOut(board.D25), digitalio.DigitalInOut(board.D24)]

dendrite3_pins = [digitalio.DigitalInOut(board.D5), digitalio.DigitalInOut(board.D6),
		digitalio.DigitalInOut(board.D13), digitalio.DigitalInOut(board.D19)]

for pins in [dendrite1_pins, dendrite2_pins, dendrite3_pins]:
    for pin in pins:
        pin.direction = digitalio.Direction.INPUT
        pin.pull = digitalio.Pull.UP

dots = dotstar.DotStar(board.SCK, board.MOSI, 21, brightness=0.25)

color_red = (255, 0, 0)
color_green = (0, 255, 0)
color_blue = (0, 0, 255)
color_black = (0, 0, 0)

rotary_color = (
    (color_black, color_black, color_black, color_blue, color_black, color_black, color_black), #pos 0
    
    (color_black, color_black, color_green, color_black, color_black, color_black, color_black), 
    (color_black,color_green, color_green, color_black,  color_black, color_black, color_black),
    (color_green, color_green, color_green, color_black,color_black, color_black, color_black),
    
    (color_black, color_black, color_black, color_black, color_black, color_black, color_black), #pos 4
    (color_black, color_black, color_black, color_black, color_black, color_black, color_black),#pos 5
    (color_black, color_black, color_black, color_black, color_black, color_black, color_black), #pos 6
    
    (color_black, color_black, color_black, color_black, color_red, color_red, color_red),#pos 7
    (color_black, color_black, color_black, color_black, color_red, color_red, color_black),#pos 8
    (color_black, color_black, color_black, color_black, color_red, color_black, color_black),#pos 9 end of 10-pos switch
    
    (color_black, color_black, color_black, color_black, color_red, color_black, color_black),#pos 10
    (color_black, color_black, color_black, color_black, color_black, color_black, color_black),#pos 11

    (color_black, color_black, color_black, color_black, color_black, color_black, color_black), #pos 12
    (color_black, color_black, color_black, color_black, color_red, color_red, color_red), #pos 13
    (color_black, color_black, color_black, color_black, color_red, color_red, color_black), #pos 7 (14); 3 red led
    (color_black, color_black, color_black, color_black, color_red, color_black, color_black), #pos 9; 1 red led
)


def decode_switch(pins):
    value = 0
    for i in range(len(pins)):
        if pins[i].value == False:
          value += 2**i
    return value

def display_weight(dendrite, value):
    pattern = rotary_color[value]
    index = (dendrite-1) * 7
    for i in range(len(pattern)):
        dots[index+i] = pattern[i]

while True:

    dendrite1_pos = decode_switch(dendrite1_pins)
    dendrite2_pos = decode_switch(dendrite2_pins)
    dendrite3_pos = decode_switch(dendrite3_pins)
        
    print ("Dendrite1:", dendrite1_pos, "Dendrite2:", dendrite2_pos, "Dendrite3:", dendrite3_pos)
    
    #print ("Dendrite2 weight:", dendrite2_pos)

    if pin1.value == False: # Button press detected pulls GPIO pin LOW
        print ("Button 1 Pressed")
        time.sleep(.1)
        pygame.mixer.music.play()
        time.sleep(0.4)

    if pin2.value == False: # Button press detected pulls GPIO pin LOW
        print ("Button 2 Pressed")
        pygame.mixer.music.play()
        time.sleep(0.4)

    if pin3.value == False: # Button press detected pulls GPIO pinLOW
        print ("Button 3 Pressed")
        
        pygame.mixer.music.play()
        time.sleep(0.4)     

    display_weight(1, dendrite1_pos)
    display_weight(2, dendrite2_pos)
    display_weight(3, dendrite3_pos)

    dots.show()

   # time.sleep(0.1)
