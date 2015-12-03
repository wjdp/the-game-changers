import pygame
from pygame.locals import *

from consts import *

class Object(object):
  """Generic object, a thing with a position that's drawn to the screen"""
  PLACEHOLDER_COLOUR = YELLOW
  Z_INDEX = 0

  def __init__(self, controller, pos=(0,0)):
    # Set instance variables
    self.controller = controller
    self.pos = pos
    self.rect = pygame.Rect(pos, (GRID, GRID))
    self.visible = True

  def get_image(self, image_path=None):
    """Load in a image surface or return the cached one"""
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
    """Generate a placeholder surface"""
    placeholder_surface = pygame.Surface(self.rect.size)
    placeholder_surface.fill(YELLOW)
    return placeholder_surface

  def draw(self):
    """Return a surface to represent object"""
    if self.get_image():
      # We have an image, return its surface
      return self.get_image()
    else:
      # We don't have an image, return a placeholder surface
      return self.get_placeholder()

  def get_width(self):
    """Return width of image"""
    if self.get_image():
      return self.get_image().get_width()
    else:
      return GRID

  def get_height(self):
    """Return height of image"""
    if self.get_image():
      return self.get_image().get_height()
    else:
      return GRID

  def set_pos_centre(self):
    """Set the object's position to screen centre"""
    self.pos = (
      (SCREEN_WIDTH / 2) - (self.get_width() / 2),
      (SCREEN_HEIGHT / 2) - (self.get_height() / 2),
    )

  def tick(self):
    # Update the stored rect of object given its pos, width and height
    self.rect = pygame.Rect(self.pos, (self.get_width(), self.get_height()))

  def destroy(self):
    pass

class MovableObject(Object):
  """An object that moves, has a velocity which updates the position on each
  tick"""

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


class CollisionDetectionMixin(Object):
  """Adds a collision check mechanism"""

  def collision_check(self):
    for obj in self.controller.engine.objects:
      if not (obj is self or self.rect.colliderect(obj.rect) == 0):
        return obj
    return False


class Hut(Object):
  """Huts at top of screen the player reaches to win"""
  IMAGE = HUT
  PLACEHOLDER_COLOUR = GREEN


class Egg(Object):
  """Eggs represent lives in the score bar"""
  Z_INDEX = 10
  IMAGE = EGG


class PopupObject(Object):
  """Base class for popups"""
  Z_INDEX = 100


class DeadChickenPopup(PopupObject):
  """Death popup"""
  Z_INDEX = 100
  IMAGE = DEAD_CHICKEN
