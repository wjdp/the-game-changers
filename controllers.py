import pygame
from pygame.locals import *

from consts import *

class Controller(object):
  EVENT_BINDINGS = [] # Empty bindings

  def __init__(self, engine):
    self.engine = engine
    self.create() # Use create in sub-classes for any init stuff

  # Method stubs

  def create(self):
    pass

  def tick(self):
    pass

  def close(self):
    pass

class MenuController(Controller):
  def create(self):
    print "Create menu controller"
    bg = pygame.image.load('images/menu.png')
    self.engine.clear_background()
    self.engine.background_blit(bg, ORIGIN)

  def close(self):
    print "Closing menu controller"

  def start_game(self):
    self.engine.setup_state('game')

  EVENT_BINDINGS = {
    K_RETURN: start_game
  }


class PlayerController(Controller):
  def create(self):
    print "Create player controller"

class LevelController(Controller):
  def create(self):
    print "Create level controller"

class GameOverController(Controller):
  def create(self):
    print "Create GO controller"

class FPSCounterController(Controller):
  def create(self):
    self.font = pygame.font.SysFont("Arial", 16)

  def tick(self):
    text = self.font.render(str(self.engine.get_fps()), True, YELLOW)
    self.engine.foreground_blit(text, (0, 0))

