import pygame

from consts import *

class Object(object):
  def __init__(self, pos=(0,0)):
    self.pos = pos

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
    placeholder_surface.fill(YELLOW)
    return placeholder_surface

  def draw(self):
    if self.get_image():
      return None
    else:
      return self.get_placeholder()

  def destroy(self):
    pass

class MovableObject(Object):
  pass

