ORIGIN = (0, 0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

YELLOW = (255, 255, 0)
COLORKEY = (255, 0, 255)

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

E_WIN = 5001
E_DIE = 5002
E_SOFT_RESET = 5003
E_HOP = 5004
E_SCORE_CHANGED = 5005

# Directions

LEFT = 1
UP = 2
RIGHT = 3
DOWN = 4

# Points awarded

POINTS_PROGRESSION = 1 # Points for a 'progression', a non repeatable hop up
POINTS_WIN = 10 # Points for completing a level

# Screen dimensions, we're using a 32x32 grid

SCREEN_WIDTH = 26 * 32
SCREEN_HEIGHT = 18 * 32

