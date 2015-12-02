import pygame

from consts import *

class Object(object):
  PLACEHOLDER_COLOUR = YELLOW

  def __init__(self, controller):
    self.controller = controller

  def get_image(self):
    if hasattr(self, 'image'):
      return self.image
    elif hasattr(self, 'IMAGE'):
      self.image = pygame.image.load('images/{}'.format(self.IMAGE))
      return self.image
    else:
      return None

  def get_placeholder(self):
    placeholder_surface = pygame.Surface((32, 32))
    placeholder_surface.fill(self.PLACEHOLDER_COLOUR)
    return placeholder_surface

  def draw(self):
    if self.get_image():
      return self.get_image()
    else:
      return self.get_placeholder()

  def tick(self):
    pass

  def destroy(self):
    pass

class MovableObject(Object):
  velocity = (0, 0)

  def tick(self):
    super(MovableObject, self).tick()
    self.tick_move()

  def tick_move(self):
    """Move the object based on velocity"""
    new_pos = (
      self.pos[0] + (self.velocity[0] * self.controller.engine.last_tick),
        self.pos[1] + (self.velocity[1] * self.controller.engine.last_tick)
    )
    self.pos = new_pos
