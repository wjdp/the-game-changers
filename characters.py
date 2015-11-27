from objects import MovableObject
from consts import *


class Character(MovableObject):
  """Characters are objects that are a bit more intelligent. They know
  where they should start at and handle their own velocity"""

  def __init__(self, controller, *args, **kwargs):
    # Run the object init method
    super(Character, self).__init__(controller)
    # Run the Character's create method
    self.create(*args, **kwargs)

  def create(self):
    """Should return a position, if not will default to Object's default"""
    pass

class Frog(Character):
  def create(self):
    self.pos = (SCREEN_WIDTH/2, SCREEN_HEIGHT-50)


class Car(Character):
  SPEED = 1
  LANE_HEIGHT = 40
  LANE_ORIGIN = SCREEN_WIDTH/2
  CAR_WIDTH = 32
  CAR_SPACING = 64 

  def create(self, lane, delay):
    py = self.LANE_ORIGIN - (self.LANE_HEIGHT * lane)
    if lane % 2:
      # Start on LHS
      px = -self.CAR_WIDTH - (delay * self.CAR_SPACING)
      self.velocity = (self.SPEED, 0)
      self.direction = 0
    else:
      # Start on RHS
      px = self.controller.engine.SCREEN_WIDTH + self.CAR_WIDTH + + (delay * self.CAR_SPACING)
      self.velocity = (-self.SPEED, 0)
      self.direction = 1

    self.pos = [px, py]
    

  def tick(self):
    #super(Car, self,).tick()
    self.pos[0] = (self.pos[0] + self.velocity[0]) % SCREEN_WIDTH

 

