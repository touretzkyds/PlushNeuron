import adafruit_dotstar as dotstar

global dots

NUM_PIXELS = 3*7 + 2*9 + 4

DENDRITE_1_LED_START_INDEX = 0
DENDRITE_2_LED_START_INDEX = 7
DENDRITE_3_LED_START_INDEX = 14
NET_INPUT_LED_START_INDEX = 21
THRESHOLD_LED_START_INDEX = 30
AXON_LED_START_INDEX = 39

def init_leds():
    global dots
    dots = dotstar.DotStar(board.SCK, board.MOSI, NUM_PIXELS, brightness=0.25)
    for i in range(NUM_PIXELS):
        dots[i].value = (0, 0, 0)


RGB_COLORS = (
    (  0,   0,   0),  # 0 - black
    (255,   0,   0),  # 1 - red
    (  0, 255,   0),  # 2 - green
    (  0,   0, 255),  # 3 - blue
    (128,   0,   0),  # 4 - dim-red
    (  0, 128,   0)   # 5 - dim-green
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

THRESHOLD_ROTARY_COLORS = (
    (0, 0, 0, 0, 3, 0, 0, 0, 0), #  0 = blue
    (0, 0, 0, 4, 0, 0, 0, 0, 0), #  1 = dim-green
    (0, 0, 4, 2, 0, 0, 0, 0, 0), #  2 = green dim-green
    (0, 0, 2, 2, 0, 0, 0, 0, 0), #  3 = green green
    (0, 4, 2, 2, 0, 0, 0, 0, 0), #  4 = green green dim-green
    (0, 2, 2, 2, 0, 0, 0, 0, 0), #  5 = green green green
    (4, 2, 2, 2, 0, 0, 0, 0, 0), #  6 = green green green dim-green
    (2, 2, 2, 2, 0, 0, 0, 0, 0), #  7 = green green green green
    (0, 0, 0, 0, 0, 0, 0, 0, 0), #  8 = nothing
    (0, 0, 0, 0, 0, 1, 1, 1, 1), #  9 = red red red red
    (0, 0, 0, 0, 0, 1, 1, 1, 5), # 10 = red red red dim-red
    (0, 0, 0, 0, 0, 1, 1, 1, 0), # 11 = red red red
    (0, 0, 0, 0, 0, 1, 1, 5, 0), # 12 = red red dim-red
    (0, 0, 0, 0, 0, 1, 1, 0, 0), # 13 = red red
    (0, 0, 0, 0, 0, 1, 5, 0, 0), # 13 = red dim-red
    (0, 0, 0, 0, 0, 1, 0, 0, 0), # 14 = red
    (0, 0, 0, 0, 0, 5, 0, 0, 0), # 15 = dim-red
)

def display_pattern(patterns, led_start_index, value):
    pattern = patterns[value]
    for i in range(len(pattern)):
        dots[led_start_index+i] = RGB_COLORS[pattern[i]]
    dots.show()