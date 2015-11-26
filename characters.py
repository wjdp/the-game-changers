from objects import MovableObject

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
    self.pos = (150, 400)

class Car(Character):
  SPEED = 0.06
  LANE_HEIGHT = 32
  LANE_ORIGIN = 300
  CAR_WIDTH = 32
  CAR_SPACING = 64

  def create(self, lane, delay):
    py = self.LANE_ORIGIN - (self.LANE_HEIGHT * lane)
    if lane % 2:
      # Start on LHS
      px = -self.CAR_WIDTH - (delay * self.CAR_SPACING)
      self.velocity = (self.SPEED, 0)
    else:
      # Start on RHS
      px = self.controller.engine.SCREEN_WIDTH + self.CAR_WIDTH + + (delay * self.CAR_SPACING)
      self.velocity = (-self.SPEED, 0)

    self.pos = (px, py)

