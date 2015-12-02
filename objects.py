import pygame

from consts import *

class Object(object):
  PLACEHOLDER_COLOUR = YELLOW

  def __init__(self, controller):
    self.controller = controller

  def get_image(self, image_path=None):
    if hasattr(self, 'image'):
      # Image already loaded, return it
      return self.image
    elif image_path:
      # Provided image path
      selected_image_path = image_path
    elif hasattr(self, 'IMAGE'):
      # Class has IMAGE const
      selected_image_path = self.IMAGE
    else:
      # No image path
      return None

    self.image = pygame.image.load('images/{}'.format(selected_image_path)).convert_alpha()
    return self.image

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
