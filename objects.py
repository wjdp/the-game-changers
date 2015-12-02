import pygame
from pygame.locals import *


from consts import *

class Object(object):
  PLACEHOLDER_COLOUR = YELLOW

  def __init__(self, controller, pos=(0,0)):
    self.controller = controller
    self.pos = pos
    self.rect = pygame.Rect(pos ,(32, 32))

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
    placeholder_surface = pygame.Surface(self.rect.size)
    placeholder_surface.fill(YELLOW)
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



class CollisionDetectionObject(Object):

  def collision_check(self, all_objects):
    print "collision check 1 start"
    for obj in all_objects:
      print "collision check 2 continue"
      if not obj is self:
        print "collision check 3 continue"
        if not self.rect.colliderect(obj.rect):
          print "collision check 4 return True self: {} obj: {}" .format(type(self), type(obj))
          return True
        else:
          return False
          print "collision check 5 False {}"  .format(type(self.rect))
      else:
        print "collision check 6 else"



