import random
import pygame
from pygame.locals import *

from consts import *
from object_manager import ObjectManagerMixin
from characters import *
from objects import Egg

class BaseController(object):
  pass

class Controller(BaseController, ObjectManagerMixin):
  EVENT_BINDINGS = [] # Empty bindings

  def __init__(self, engine, messages):
    super(Controller, self).__init__()

    # Store a reference to the engine
    self.engine = engine
    # Set the engine as the ObjectManagerMixin parent
    self.object_super = engine

    # Store any messages from the state change
    self.messages = messages

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
    bg = pygame.image.load('images/intro.png')
    self.engine.clear_background()
    self.engine.background_blit(bg, ORIGIN)

    self.font1 = pygame.font.Font(FONT_ACTION_MAN, 64)

  def start_game(self):
    self.engine.setup_state('game')

  def tick(self):
    text1 = self.font1.render("Press ENTER To Start", True, YELLOW)
    x1 = (SCREEN_WIDTH - text1.get_width()) / 2

    if self.engine.get_ticks() % 1000 > 500:
      self.engine.foreground_blit(text1, (x1, SCREEN_HEIGHT - 80))

  EVENT_BINDINGS = {
    K_RETURN: start_game
  }

class SoundController(Controller):
  BACKGROUND_VOLUME = 0.3

  def create(self):
    pygame.mixer.init()
    self.sound = pygame.mixer.Sound('sounds/GameSoundtrack.wav')
    self.sound.set_volume(self.BACKGROUND_VOLUME)
    self.sound.play()

    # Preload sounds
    self.win = pygame.mixer.Sound('sounds/GameWin.wav')
    self.die = pygame.mixer.Sound('sounds/GameDie.wav')
	
  def destroy(self):
	 pygame.mixer.stop()
     
  def win(self, event):
    self.win.play()

  def die(self, event):
    self.die.play()

  EVENT_BINDINGS = {
    E_WIN: win,
    E_DIE: die,
  }



class GameController(Controller):
  level = 1
  score = 0
  lives = LIVES

  def create(self):
    bg = pygame.image.load('images/background.png')
    self.engine.clear_background()
    self.engine.background_blit(bg, ORIGIN)

    self.reset()

  def reset(self):
    self.engine.post_event(
      E_SOFT_RESET,
      level=self.level,
      lives=self.lives,
      score=self.score
    )

  def win(self, event):
    """Handle game state changes for win"""
    self.add_score(POINTS_WIN)
    self.level += 1
    self.reset()

  def die(self, event):
    """Handle game state changes for die"""
    self.lives -= 1

    if self.lives < 1:
      self.gameover()

    self.reset()

  def gameover(self):
    self.engine.setup_state('gameover', messages={'score': self.score})

  def player_moved(self, event):
    if event.progress:
      self.add_score(POINTS_PROGRESSION)

  def add_score(self, addition):
    self.score += addition
    self.engine.post_event(E_SCORE_CHANGED, score=self.score)

  EVENT_BINDINGS = {
    E_WIN: win,
    E_DIE: die,
    E_HOP: player_moved,
  }


class PlayerController(Controller):
  LEFT_BOUND = 0
  RIGHT_BOUND = SCREEN_WIDTH - 32
  TOP_BOUND = 32
  BOTTOM_BOUND = SCREEN_HEIGHT - (32 * 2)

  def create(self):
    self.player_object = self.create_object(Frog, self)
    self.max_height = 0
    self.current_height = 0
    self.active = True

  def move(self, rel_pos):
    cp = self.player_object.pos
    self.player_object.pos = (cp[0] + rel_pos[0], cp[1] + rel_pos[1])

  def move_left(self):
    if not self.player_object.pos[0] <= self.LEFT_BOUND and self.active:
      self.move((-32, 0))
      self.engine.post_event(E_HOP, direction=LEFT, progress=False)

  def move_right(self):
    if not self.player_object.pos[0] >= self.RIGHT_BOUND and self.active:
      self.move((32, 0))
      self.engine.post_event(E_HOP, direction=RIGHT, progress=False)

  def move_up(self):
    if not self.player_object.pos[1] <= self.TOP_BOUND and self.active:
      self.move((0, -32))

      self.current_height += 1
      progressed = self.max_height < self.current_height

      self.engine.post_event(E_HOP, direction=LEFT, progress=progressed)

      if progressed:
        self.max_height = self.current_height

  def move_down(self):
    if not self.player_object.pos[1] >= self.BOTTOM_BOUND and self.active:
      self.current_height -= 1
      self.move((0, 32))
      self.engine.post_event(E_HOP, direction=DOWN, progress=False)

  def reset(self, event):
    self.player_object.move_to_start()
    self.active = True

  def tick(self):
    super(PlayerController, self).tick()
    collision_object = self.player_object.collision_check()
    if collision_object and self.active:
      if isinstance(collision_object, Car):
        # Collided with Car, so die
        self.active = False
        self.engine.post_event(E_DIE)
      elif isinstance(collision_object, Hut):
        self.active = False
        self.engine.post_event(E_WIN)

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
  # Define the car generator variables
  # List of lanes, each element:
  # (num_of_cars, (delay_low, delay_high), speed_multiplier, images, width)
  LORRY_LANE_1 = (6, (3,5), .5, LORRIES, LORRY_WIDTH)
  LORRY_LANE_2 = (5, (3,5), .6, LORRIES, LORRY_WIDTH) #max 6 distance on the road

  TRUCK_LANE_1 = (5, (2,6), 0.2, TRUCKS, TRUCK_WIDTH)
  TRUCK_LANE_2 = (6, (3,5), 0.7, TRUCKS, TRUCK_WIDTH)
  TRUCK_LANE_3 = (5, (4,6), 2, TRUCKS, TRUCK_WIDTH)

  CAR_LANE_1 = (4, (4,6), 5, CARS, CAR_WIDTH) #max 7 distance on the road
  CAR_LANE_2 = (2, (6,10), 6, CARS, CAR_WIDTH)

  PAVEMENT = (0, None, None)

  CAR_GENERATOR_VARS = [
    TRUCK_LANE_3, # Lane 1
    LORRY_LANE_1,
    CAR_LANE_1,
    PAVEMENT, # Pavement
    LORRY_LANE_1,
    TRUCK_LANE_3,
    CAR_LANE_2,
    TRUCK_LANE_1,
    LORRY_LANE_2,
    PAVEMENT, # Pavement
    TRUCK_LANE_2,
    LORRY_LANE_1,
    TRUCK_LANE_3,
    TRUCK_LANE_1,
    LORRY_LANE_1,
    TRUCK_LANE_3,
    CAR_LANE_2,
    LORRY_LANE_2,
  ]

  HUT_POSITIONS = [ (x, 32) for x in range(32, SCREEN_WIDTH-32)[::32*6] ]

  def create(self):
    self.huts = []
    for hut_pos in self.HUT_POSITIONS:
      self.huts.append(self.create_object(Hut, self, hut_pos))

    self.cars = []

  def reset(self, event):
    for car in list(self.cars): # list() to make a copy
      self.cars.remove(car)
      self.destroy_object(car)

    for i, lane in enumerate(self.CAR_GENERATOR_VARS):
      total_delay = 0
      for j in range(lane[0]):
        total_delay += random.randrange(*lane[1])
        image_path = random.choice(lane[3])
        car = self.create_object(Car, self,
          lane=i,
          delay=total_delay,
          level=event.level,
          speed_multiplier=lane[2],
          image_path=image_path,
          width=lane[4],
        )
        self.cars.append(car)

  EVENT_BINDINGS = {
    E_SOFT_RESET: reset
  }


class FPSCounterController(Controller):

  def create(self):
    self.font = pygame.font.Font(FONT_ACTION_MAN, 32)
    self.show_fps = False

  def tick(self):
    # If fps active, blit to top left
    if self.show_fps:
      text = self.font.render(str(self.engine.get_fps()), True, RED)
      self.engine.foreground_blit(text, (0, 0))

  def toggle_fps(self):
    self.show_fps = not self.show_fps

  EVENT_BINDINGS = {
    K_f: toggle_fps,
  }


class ScoreTextController(Controller):
  lives = None
  score = None

  EGG_ORIGIN = (SCREEN_WIDTH - (32 * LIVES), 0)

  def create(self):
    self.font = pygame.font.Font(FONT_ACTION_MAN, 30, bold = True, italic = False)
    self.eggs = []

  def update(self, event):
    self.lives = event.lives
    self.score = event.score

  def update_score(self, event):
    self.score = event.score

  def update_eggs(self):
    self.purge_objects()
    for i in range(self.lives):
      egg = self.create_object(Egg, self,
        pos=(self.EGG_ORIGIN[0] + (32 * i), self.EGG_ORIGIN[1]))
      self.eggs.append(egg)

  def tick(self):
    if self.lives is not None:
      if len(self.eggs) != self.lives:
        self.update_eggs()

      text1 = self.font.render("Score: {}".format(self.score), 1 , YELLOW)
      text2 = self.font.render("Lives", 1 , YELLOW)
      self.engine.foreground_blit(text1, (2,4))
      self.engine.foreground_blit(text2, (self.EGG_ORIGIN[0] - text2.get_width() - 12 ,4))

  EVENT_BINDINGS = {
    E_SOFT_RESET: update,
    E_SCORE_CHANGED: update_score,
  }


class GameOverController(Controller):
  def create(self):
    bg = pygame.image.load('images/end.png')
    self.engine.clear_background()
    self.engine.background_blit(bg, ORIGIN)

    self.font1 = pygame.font.Font(FONT_ACTION_MAN, 64)
    self.font2 = pygame.font.Font(FONT_ACTION_MAN, 32)

    self.score = self.messages['score']

  def tick(self):
    text1 = self.font1.render("Your Score: {}".format(self.score), True, YELLOW)
    x1 = (SCREEN_WIDTH - text1.get_width()) / 2
    text2 = self.font2.render("Press ENTER to try again".format(self.score), True, YELLOW)
    x2 = (SCREEN_WIDTH - text2.get_width()) / 2

    self.engine.foreground_blit(text1, (x1, 32))
    if self.engine.get_ticks() % 1000 > 500:
      self.engine.foreground_blit(text2, (x2, 96))

  def restart(self):
    self.engine.setup_state('game', purge=True)

  EVENT_BINDINGS = {
    K_RETURN: restart
  }
