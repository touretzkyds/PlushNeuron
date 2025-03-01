import board
import adafruit_dotstar as dotstar

NUM_DENDRITES = 3
NUM_PIXELS_WEIGHT = 7
NUM_PIXELS_ACTIVATION = 9
NUM_PIXELS_THRESHOLD = 9
NUM_AXON_STRIPS = 3
NUM_PIXELS_AXON_STRIP = 15
NUM_PIXELS_AXON = NUM_AXON_STRIPS * NUM_PIXELS_AXON_STRIP
NUM_PIXELS = NUM_DENDRITES * NUM_PIXELS_WEIGHT + \
    NUM_PIXELS_ACTIVATION + NUM_PIXELS_THRESHOLD + \
    NUM_PIXELS_AXON

DENDRITE_1_LED_START_INDEX = 0
DENDRITE_2_LED_START_INDEX = DENDRITE_1_LED_START_INDEX + NUM_PIXELS_WEIGHT
DENDRITE_3_LED_START_INDEX = DENDRITE_2_LED_START_INDEX + NUM_PIXELS_WEIGHT
ACTIVATION_LED_START_INDEX = DENDRITE_3_LED_START_INDEX + NUM_PIXELS_WEIGHT
THRESHOLD_LED_START_INDEX  = ACTIVATION_LED_START_INDEX + NUM_PIXELS_ACTIVATION
AXON_LED_START_INDEX       = THRESHOLD_LED_START_INDEX + NUM_PIXELS_THRESHOLD

def init_leds():
    global dots
    dots = dotstar.DotStar(board.SCK, board.MOSI, NUM_PIXELS, brightness=0.25)
    for i in range(NUM_PIXELS):
        dots[i] = (0, 0, 0)
    dots.show()

RGB_COLORS = (
    (  0,   0,   0),  # 0 - black
    (255,   0,   0),  # 1 - red
    (  0, 255,   0),  # 2 - green
    (  0,   0, 255),  # 3 - blue
    (  4,   2,   2),  # 4 - dim-red
    (  2,   4,   2),  # 5 - dim-green
    (  0,   0,  16),  # 6 - dim-blue (currently unused)
    (127, 127, 127)   # 7 - white
)

DENDRITE_ROTARY_COLORS = (
    (0, 0, 0, 3, 0, 0, 0), # 0 = blue
    (0, 0, 2, 0, 0, 0, 0), # 1 = green
    (0, 2, 2, 0, 0, 0, 0), # 2 = green green
    (2, 2, 2, 0, 0, 0, 0), # 3 = green green green
    (2, 2, 2, 2, 0, 0, 0), # 4 = green green green green
    (0, 0, 0, 0, 0, 0, 0), # 5 = nothing
    (0, 0, 0, 1, 1, 1, 1), # 6 = red red red red
    (0, 0, 0, 0, 1, 1, 1), # 7 = red red red
    (0, 0, 0, 0, 1, 1, 0), # 8 = red red
    (0, 0, 0, 0, 1, 0, 0)  # 9 = red
)

DENDRITE_ROTARY_BLANK = (0,) * len(DENDRITE_ROTARY_COLORS[0])

THRESHOLD_ROTARY_COLORS = (
    (0, 0, 0, 0, 3, 0, 0, 0, 0), #  0 = blue
    (0, 0, 0, 5, 0, 0, 0, 0, 0), #  1 = dim-green
    (0, 0, 0, 2, 0, 0, 0, 0, 0), #  2 = green
    (0, 0, 5, 2, 0, 0, 0, 0, 0), #  3 = green dim-green
    (0, 0, 2, 2, 0, 0, 0, 0, 0), #  4 = green green
    (0, 5, 2, 2, 0, 0, 0, 0, 0), #  5 = green green dim-green
    (0, 2, 2, 2, 0, 0, 0, 0, 0), #  6 = green green green
    (5, 2, 2, 2, 0, 0, 0, 0, 0), #  7 = green green green dim-green
    (2, 2, 2, 2, 0, 0, 0, 0, 0), #  8 = green green green green
    (0, 0, 0, 0, 0, 1, 1, 1, 4), #  9 = red red red dim-red
    (0, 0, 0, 0, 0, 1, 1, 1, 0), # 10 = red red red
    (0, 0, 0, 0, 0, 1, 1, 4, 0), # 11 = red red dim-red
    (0, 0, 0, 0, 0, 1, 1, 0, 0), # 12 = red red
    (0, 0, 0, 0, 0, 1, 4, 0, 0), # 13 = red dim-red
    (0, 0, 0, 0, 0, 1, 0, 0, 0), # 14 = red
    (0, 0, 0, 0, 0, 4, 0, 0, 0), # 15 = dim-red
)

ACTIVATION_COLORS = {
    -9 : (1, 1, 1, 1, 1, 1, 1, 1, 1),
    -8 : (0, 1, 1, 1, 1, 1, 1, 1, 1),
    -7 : (0, 0, 1, 1, 1, 1, 1, 1, 1),
    -6 : (0, 0, 0, 1, 1, 1, 1, 1, 1),
    -5 : (0, 0, 0, 0, 1, 1, 1, 1, 1),
    -4 : (0, 0, 0, 0, 0, 1, 1, 1, 1),
    -3 : (0, 0, 0, 0, 0, 1, 1, 1, 0),
    -2 : (0, 0, 0, 0, 0, 1, 1, 0, 0),
    -1 : (0, 0, 0, 0, 0, 1, 0, 0, 0),
     0 : (0, 0, 0, 0, 3, 0, 0, 0, 0),
     1 : (0, 0, 0, 2, 0, 0, 0, 0, 0),
     2 : (0, 0, 2, 2, 0, 0, 0, 0, 0),
     3 : (0, 2, 2, 2, 0, 0, 0, 0, 0),
     4 : (2, 2, 2, 2, 0, 0, 0, 0, 0),
     5 : (2, 2, 2, 2, 2, 0, 0, 0, 0),
     6 : (2, 2, 2, 2, 2, 2, 0, 0, 0),
     7 : (2, 2, 2, 2, 2, 2, 2, 0, 0),
     8 : (2, 2, 2, 2, 2, 2, 2, 2, 0),
     9 : (2, 2, 2, 2, 2, 2, 2, 2, 2)
}

AXON_BLANK_PATTERN = (0,) * NUM_PIXELS_AXON

AXON_FIRING_PATTERNS = {
     0 : (7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     1 : (7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     2 : (7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     3 : (7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     4 : (7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     5 : (7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0),
     6 : (7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0),
     7 : (7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0),
     8 : (7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0),
     9 : (7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0),
    10 : (7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0),
    11 : (7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0),
    12 : (7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0),
    13 : (7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0),
    14 : (7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7)
}

def display_pattern(pattern, led_start_index):
    for i in range(len(pattern)):
        dots[led_start_index+i] = RGB_COLORS[pattern[i]]
    dots.show()
