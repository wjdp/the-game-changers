import pygame
from pygame.locals import *


from consts import *

class Object(object):
  def __init__(self, controller, pos=(0,0)):
    self.controller = controller
    self.pos = pos
    self.rect = pygame.Rect(pos ,(32, 32))

  def get_image(self):
    if hasattr(self, 'image'):
      return self.image
    elif hasattr(self, 'IMAGE'):
      self.image = pygame.image.load('images/{}'.format(self.IMAGE))
      return self.image
    else:
      return None

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

  #x = self.pos[0]
  #y = self.pos[1]

  def collide(self, rect):
    print "colliosion check1"
    x = self.pos[0]
    y = self.pos[1]
    if(x > self.left) and (x < self.right) and (y > self.top) and (y < self.bottom):
     return True
  

  def collision_check(self, all_objects): 
    print "collision check 1 start"
    for obj in all_objects:
      print "collision check 2 continue" 
      if not obj is self:
        print "collision check 3 continue"
        if self.rect.colliderect(obj.rect):
          print "collision check 4 return True self: {} obj: {}" .format(type(self), type(obj))
          return False
        else:
          return False
          print "collision check 5 False {}"  .format(type(self.rect))
      else:
        print "collision check 6 else"
  
  #x = self.pos[0]
  #y = self.pos[1]

#for a, b in [(obj.pos, self.pos),(self.pos, obj.pos)]:

#((self.collide(a.left, a.top, b)) or
#(self.collide(a.left, a.bottom, b)) or
#(self.collide(a.right, a.top, b)) or
#(self.collide(a.right, a.bottom, b))):
#return True"""


  
     

