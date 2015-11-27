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
    self.tick_objects()

  def destroy(self):
    self.purge_objects()

class MenuController(Controller):
  def create(self):
    bg = pygame.image.load('images/menu.png')
    self.engine.clear_background()
    self.engine.background_blit(bg, ORIGIN)


  def start_game(self):
    self.engine.setup_state('game')

  EVENT_BINDINGS = {
    K_RETURN: start_game
  }

class GameController(Controller):
  level = 0

  def create(self):
    self.engine.clear_background()

  def win(self, event):
    """Handle game state changes for win"""
    self.level += 1
    self.engine.post_event(E_SOFT_RESET, level=self.level)

  def die(self, event):
    """Handle game state changes for die"""
    self.engine.post_event(E_SOFT_RESET, level=self.level)

  EVENT_BINDINGS = {
    E_WIN: win,
    E_DIE: die,
  }

class PlayerController(Controller):
  max_height = 0
  current_height = 0

  def create(self):
    self.player_object = self.create_object(Frog, self)

  def move(self, rel_pos):
    cp = self.player_object.pos
    self.player_object.pos = (cp[0] + rel_pos[0], cp[1] + rel_pos[1])

  def move_left(self):
    self.move((-32, 0))

  def move_right(self):
    self.move((32, 0))

  def move_up(self):
    self.current_height += 1
    if self.max_height < self.current_height:
      self.max_height = self.current_height
      # Increase score
      print "+1"
    self.move((0, -32))

  def move_down(self):
    self.current_height -= 1
    self.move((0, 32))

  def reset(self, event):
    self.player_object.move_to_start()

  EVENT_BINDINGS = {
    KM_LEFT: move_left,
    KM_RIGHT:  move_right,
    KM_UP: move_up,
    KM_DOWN: move_down,
    KM_LEFT1: move_left,
    KM_RIGHT1:  move_right,
    KM_UP1: move_up,
    KM_DOWN1: move_down,
    E_SOFT_RESET: reset,
  }


class LevelController(Controller):
  def create(self):
    self.cars = [
      self.create_object(Car, self, lane=0, delay=0),
      self.create_object(Car, self, lane=0, delay=3),
      self.create_object(Car, self, lane=0, delay=6),
      self.create_object(Car, self, lane=0, delay=8),
      self.create_object(Car, self, lane=1, delay=2),
      self.create_object(Car, self, lane=1, delay=4),
      self.create_object(Car, self, lane=1, delay=7),
      self.create_object(Car, self, lane=1, delay=9),
      self.create_object(Car, self, lane=2, delay=0),
      self.create_object(Car, self, lane=2, delay=4),
      self.create_object(Car, self, lane=3, delay=6),
      self.create_object(Car, self, lane=3, delay=2),
      self.create_object(Car, self, lane=3, delay=6),
      self.create_object(Car, self, lane=4, delay=0),
      self.create_object(Car, self, lane=4, delay=3),
      self.create_object(Car, self, lane=4, delay=6),
      self.create_object(Car, self, lane=4, delay=8),
    ]

  def speed_up_cars(self, event):
    for car in self.cars:
      car.change_speed(event.level)

  EVENT_BINDINGS = {
    E_SOFT_RESET: speed_up_cars
  }

class GameOverController(Controller):
  pass

class FPSCounterController(Controller):

  def create(self):
    self.font = pygame.font.SysFont("Arial", 16)

  def tick(self):
    
    text = self.font.render(str(self.engine.get_fps()), True, YELLOW)
    self.engine.foreground_blit(text, (0, 0))
    

class GameScoreController(Controller):

  def create(self):
    self.font = pygame.font.SysFont("verdana", 20, bold = True, italic = False)    

  def tick(self):
    self.scores = 0
    self.points = 10
    
    text = self.font.render("Scores: " + str(self.scores), 1 , (0, 0, 255))
    self.engine.foreground_blit(text, (0,0))    
	
