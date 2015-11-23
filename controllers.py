import pygame

class Controller(object):
  def __init__(self, engine):
    self.engine = engine
    self.create()

  # Method stubs

  def create(self):
    pass

  def tick(self):
    pass

class MenuController(Controller):
  def create(self):
    print "Create menu controller"
    bg = pygame.image.load('images/menu.png')
    self.engine.screen.blit(bg, (0,0))


class PlayerController(Controller):
  pass

class LevelController(Controller):
  pass

class GameOverController(Controller):
  pass
