import pygame

from objects import MovableObject, CollisionDetectionMixin
from consts import *

class Character(MovableObject):
  """Characters are objects that are a bit more intelligent. They know
  where they should start at and handle their own velocity"""

  def __init__(self, controller, *args, **kwargs):
    # Run the object init method
    super(Character, self).__init__(controller)
    # Run the Character's create method
    self.create(*args, **kwargs)

  def create(self, pos):
    """Should return a position, if not will default to Object's default"""
    self.pos = pos

class Frog(Character, CollisionDetectionMixin):
  """The player object, is a chicken rather than a frog"""

  IMAGE = "chicken.png"
  PLACEHOLDER_COLOUR = RED
  Z_INDEX = 5

  def create(self):
    self.move_to_start()

  def move_to_start(self):
    """Move the frog to the starting position"""
    self.pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 64)

  def move(self, rel_pos):
    """Move the frog the provided number of GRID squares, (x, y)"""
    self.pos = (self.pos[0] + rel_pos[0] * GRID, self.pos[1] + rel_pos[1] * GRID)

class Car(Character):
  """The 'car' object, it drives on roads and collides with the player"""

  SPEED = 0.01
  SPEED_INCREMENT = 0.01
  LANE_HEIGHT = GRID
  LANE_ORIGIN = SCREEN_HEIGHT - (GRID * 3)
  CAR_SPACING = 64

  def create(self, lane, delay, level, speed_multiplier, image_path, width):
    # Store as instance variables
    self.lane = lane
    self.width = width

    # Set the position based on provided params
    py = self.LANE_ORIGIN - (self.LANE_HEIGHT * lane)
    px = delay * self.CAR_SPACING
    self.pos = (px, py)

    # Set the speed based on level and individual speed_multiplier
    self.set_speed((level + 1) * speed_multiplier)

    # Set the image, and if in a right moving lane flip in the horizontal
    self.image = self.get_image(image_path)
    if self.lane % 2:
      # If move to right, flip image in x
      self.image = pygame.transform.flip(self.image, True, False)

  def set_speed(self, level):
    """Set the velocity of the object"""
    speed = self.SPEED + (self.SPEED_INCREMENT * level)

    if self.lane % 2:
      # Move to the right
      self.velocity = (speed, 0)
    else:
      # Move to the left
      self.velocity = (-speed, 0)

  def get_width(self):
    # Override object get_width function
    return self.width

  def tick_move(self):
    """Move the object based on velocity with wrapping"""
    if self.velocity[0] > 0 and self.pos[0] > SCREEN_WIDTH:
      # Moving right, reposition to off the left of the screen
      new_pos = (-self.width, self.pos[1])
    elif self.velocity[0] < 0 and self.pos[0] < -self.width:
      # Moving left, reposition to off the right of the screen
      new_pos = (SCREEN_WIDTH + self.width, self.pos[1])
    else:
      # Car not offscreen, move as normal
      new_pos = (
        self.pos[0] + (self.velocity[0] * self.controller.engine.last_tick),
        self.pos[1]
      )

    self.pos = new_pos



