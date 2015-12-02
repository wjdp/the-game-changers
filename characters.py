from objects import MovableObject, CollisionDetectionObject
from consts import *


class Character(MovableObject):
  """Characters are objects that are a bit more intelligent. They know
  where they should start at and handle their own velocity"""

  def __init__(self, controller, *args, **kwargs):
    # Run the object init method
    super(Character, self).__init__(controller)
    # Run the Character's create method
    prite.Sprite.__init__(self)
    self.create(*args, **kwargs)

  def create(self):
    """Should return a position, if not will default to Object's default"""
    pass

class Frog(Character, CollisionDetectionObject):
  IMAGE = "chicken.png"
  def create(self):
    self.move_to_start()

  def move_to_start(self):
    """Move the frog to the starting position"""
    self.pos = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 64)


class Car(Character):
  SPEED = 0.04
  SPEED_INCREMENT = 0.01
  LANE_HEIGHT = 32
  LANE_ORIGIN = SCREEN_WIDTH / 2
  CAR_WIDTH = 17
  CAR_SPACING = 64

  def create(self, lane, delay, speed_multiplier):
    self.lane = lane

    py = self.LANE_ORIGIN - (self.LANE_HEIGHT * lane), 
    px = delay * self.CAR_SPACING
    self.pos = (px, py)

    self.set_speed(speed_multiplier) # Set level 0 speed

  def set_speed(self, level):
    speed = self.SPEED + (self.SPEED_INCREMENT * level)

    if self.lane % 2:
      # Move to the right
      self.velocity = (speed, 0)
    else:
      # Move to the left
      self.velocity = (-speed, 0)

  def tick_move(self):
    """Move the object based on velocity with wrapping"""
    if self.velocity[0] > 0 and self.pos[0] > SCREEN_WIDTH:
      # Moving right, reposition to off the left of the screen
      new_pos = (-self.CAR_WIDTH, self.pos[1])
    elif self.velocity[0] < 0 and self.pos[0] < -self.CAR_WIDTH:
      # Moving left, reposition to off the right of the screen
      new_pos = (SCREEN_WIDTH + self.CAR_WIDTH, self.pos[1])
    else:
      # Car not offscreen, move as normal
      new_pos = (
        self.pos[0] + (self.velocity[0] * self.controller.engine.last_tick),
        self.pos[1]
      )

    self.pos = new_pos



