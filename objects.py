class Object(object):
  def __init__(self, pos=(0,0)):
    self.pos = pos

  def get_image(self):
    if self.IMAGE:
      return pygame.image.load('images/{}'.format(self.IMAGE))
    else:
      return None

  def draw(self):
    return None

  def destroy(self):
    pass

class MovableObject(Object):
  pass

