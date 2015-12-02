ORIGIN = (0, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
COLORKEY = (255, 0, 255)

# Fonts
FONT_ACTION_MAN = "fonts/Action_Man.ttf"
FONT_ACTION_MAN = "fonts/Action_Man_Bold.ttf"

# Images
BLUELORRY = "bluelorry.png"
GREENLORRY = "greenlorry.png"
LORRIES = [BLUELORRY, GREENLORRY]
LORRY_WIDTH = 60

REDTRUCK = "redtruck.png"
PURPLETRUCK = "purpletruck.png"
TRUCKS = [REDTRUCK, PURPLETRUCK]
TRUCK_WIDTH = 65

ORANGECAR = "orangecar.png"
PINKCAR = "pinkcar.png"
REDCAR = "redcar.png"
BLUECAR = "bluecar.png"
CARS = [ORANGECAR, PINKCAR, REDCAR, BLUECAR]
CAR_WIDTH = 46

CHICKEN = "chicken.png"

HUT = "hut.png"
INTRO = "intro.png"
END = "end.png"

# Keymap controls

from pygame.locals import *

KM_LEFT = K_LEFT
KM_RIGHT = K_RIGHT
KM_UP = K_UP
KM_DOWN = K_DOWN
KM_LEFT1 = K_a
KM_RIGHT1 = K_d
KM_UP1 = K_w
KM_DOWN1 = K_s

# Controller events

E_WIN = 1
E_DIE = 2
E_SOFT_RESET = 3
E_HOP = 4
E_SCORE_CHANGED = 5

# Directions

LEFT = 1
UP = 2
RIGHT = 3
DOWN = 4

# Scoring

LIVES = 5 # Number of lives a player starts with
POINTS_PROGRESSION = 1 # Points for a 'progression', a non repeatable hop up
POINTS_WIN = 10 # Points for completing a level

# Screen dimensions, we're using a 32x32 grid

SCREEN_WIDTH = 30 * 32
SCREEN_HEIGHT = 22 * 32

