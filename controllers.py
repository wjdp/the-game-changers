import pygame
from pygame.locals import *

from consts import *
from object_manager import ObjectManagerMixin
from characters import *

class BaseController(object):
  pass

class Controller(BaseController, ObjectManagerMixin):
  EVENT_BINDINGS = [] # Empty bindings

  def __init__(self, engine):
    self.engine = engine
    self.create() # Use create in sub-classes for any init stuff

  # Method stubs

  def create(self):
    pass

  def tick(self):
    pass

  def destroy(self):
    self.purge_objects()

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

class GameController(Controller):
  def create(self):
    self.engine.clear_background()

class PlayerController(Controller):
  def create(self):
    print "Create player controller"
    self.player_object = self.create_object(Frog, (150, 400))

  def tick(self):
    print self.player_object.pos

  def move(self, rel_pos):
    cp = self.player_object.pos
    self.player_object.pos = (cp[0] + rel_pos[0], cp[1] + rel_pos[1])

  def move_left(self):
    self.move((-6, 0))

  def move_right(self):
    self.move((6, 0))

  def move_up(self):
    self.move((0, -6))

  def move_down(self):
    self.move((0, 6))

  EVENT_BINDINGS = {
    KM_LFET: move_left,
    KM_RIGHT:  move_right,
    KM_UP: move_up,
    KM_DOWN: move_down,
  }


class LevelController(Controller):
  def create(self):
    print "Create level controller"


class GameOverController(Controller):
  def create(self):
    print "Create game over controller"


class FPSCounterController(Controller):
  def create(self):
    self.font = pygame.font.SysFont("Arial", 16)

  def tick(self):
    text = self.font.render(str(self.engine.get_fps()), True, YELLOW)
    self.engine.foreground_blit(text, (0, 0))

