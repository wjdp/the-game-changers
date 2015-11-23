import pygame
from pygame.locals import *

class Controller(object):
  EVENT_BINDINGS = []

  def __init__(self, engine):
    self.engine = engine
    self.create()

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
    self.engine.screen.blit(bg, (0,0))

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
