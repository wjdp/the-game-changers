import random
import pygame
from pygame.locals import *

from consts import *
from object_manager import ObjectManagerMixin
from characters import *
from objects import *

class BaseController(object):
  pass

class Controller(BaseController, ObjectManagerMixin):
  """Controllers manage various aspects of the game, they can manage objects,
  interact via events and request changes to the state of the game"""
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
  """Draws the main menu, changes the game state to start the game on user input"""
  def create(self):
    bg = pygame.image.load('images/intro.png')
    self.engine.clear_background()
    self.engine.background_blit(bg, ORIGIN)

    self.font1 = pygame.font.Font(FONT_ACTION_MAN, 64)
    self.font2 = pygame.font.Font(FONT_ACTION_MAN, 16)

  def start_game(self):
    self.engine.setup_state('game')

  def show_highscores(self):
    self.engine.setup_state('highscores')

  def tick(self):
    text1 = self.font1.render("Press ENTER To Start", True, YELLOW)
    x1 = (SCREEN_WIDTH - text1.get_width()) / 2

    text2 = self.font2.render("Press H To See Highscores", True, YELLOW)
    x2 = (SCREEN_WIDTH - text2.get_width()) / 2

    if self.engine.get_ticks() % 1000 > 500:
      self.engine.foreground_blit(text1, (x1, SCREEN_HEIGHT - 80))

    self.engine.foreground_blit(text2, (x2, SCREEN_HEIGHT - 20))

  EVENT_BINDINGS = {
    K_RETURN: start_game,
    K_h: show_highscores,
  }


class GameController(Controller):
  """Manages the state of the game, keeps track of lives and score, acts as a
  broker for reset events"""

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
  """Manages the player object, handles controls for movement and collision
  events"""

  LEFT_BOUND = 0
  RIGHT_BOUND = SCREEN_WIDTH - GRID
  TOP_BOUND = GRID
  BOTTOM_BOUND = SCREEN_HEIGHT - (GRID * 2)

  def create(self):
    self.player_object = self.create_object(Frog, self)
    self.max_height = 0
    self.current_height = 0

  def move_left(self):
    if not self.player_object.pos[0] <= self.LEFT_BOUND and self.player_object.visible:
      self.player_object.move((-1, 0))
      self.engine.post_event(E_HOP, direction=LEFT, progress=False)

  def move_right(self):
    if not self.player_object.pos[0] >= self.RIGHT_BOUND and self.player_object.visible:
      self.player_object.move((1, 0))
      self.engine.post_event(E_HOP, direction=RIGHT, progress=False)

  def move_up(self):
    if not self.player_object.pos[1] <= self.TOP_BOUND and self.player_object.visible:
      self.player_object.move((0, -1))

      self.current_height += 1
      progressed = self.max_height < self.current_height

      self.engine.post_event(E_HOP, direction=LEFT, progress=progressed)

      if progressed:
        self.max_height = self.current_height

  def move_down(self):
    if not self.player_object.pos[1] >= self.BOTTOM_BOUND and self.player_object.visible:
      self.current_height -= 1
      self.player_object.move((0, 1))
      self.engine.post_event(E_HOP, direction=DOWN, progress=False)

  def reset(self, event):
    self.player_object.move_to_start()
    self.player_object.visible = True

  def tick(self):
    super(PlayerController, self).tick()
    collision_object = self.player_object.collision_check()
    if collision_object and self.player_object.visible:
      if isinstance(collision_object, Car):
        # Collided with Car, so die
        self.player_object.visible = False
        self.engine.post_event(E_DIE)
      elif isinstance(collision_object, Hut):
        self.player_object.visible = False
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
  """Creates the level (cars and huts), rearranges the level on reset event"""

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

  HUT_POSITIONS = [ (x, GRID) for x in range(GRID, SCREEN_WIDTH-GRID)[::GRID*6] ]

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
  """Optional controller to show the FPS at the top of the screen"""

  def create(self):
    self.font = pygame.font.Font(FONT_ACTION_MAN, 32)
    self.show_fps = False

  def tick(self):
    # If fps active, blit to top left
    if self.show_fps:
      text = self.font.render(str(self.engine.get_fps()), True, RED)
      self.engine.foreground_blit(text, (300, 0))

  def toggle_fps(self):
    self.show_fps = not self.show_fps

  EVENT_BINDINGS = {
    K_f: toggle_fps,
  }


class ScoreTextController(Controller):
  """Shows the score and lives at the top of the screen, is updated by events
  sent by the GameController"""

  lives = None
  score = None

  EGG_ORIGIN = (SCREEN_WIDTH - (GRID * LIVES), 0)

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
        pos=(self.EGG_ORIGIN[0] + (GRID * i), self.EGG_ORIGIN[1]))
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


class SoundController(Controller):
  """Plays sounds for the game state, plays reactionary sounds on events"""

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


class PopupController(Controller):
  """Shows a popup on events (win, die)"""

  popup = None

  def create(self):
    self.hide_popup = 0

  def show_popup(self, event):
    self.popup = self.create_object(DeadChickenPopup, self)
    self.popup.set_pos_centre()
    self.hide_popup = self.engine.get_ticks() + 1000

  def tick(self):
    if self.popup is not None and self.engine.get_ticks() > self.hide_popup:
      self.purge_objects()

  EVENT_BINDINGS = {
    E_DIE: show_popup,
  }


class GameOverController(Controller):
  """Draws the gameover screen along with the player score"""

  def create(self):
    bg = pygame.image.load('images/end.png')
    self.engine.clear_background()
    self.engine.background_blit(bg, ORIGIN)

    self.font1 = pygame.font.Font(FONT_ACTION_MAN, 64)
    self.font2 = pygame.font.Font(FONT_ACTION_MAN, 32)
    self.font3 = pygame.font.Font(FONT_ACTION_MAN, 16)

    self.score = self.messages['score']

  def tick(self):
    text1 = self.font1.render("Your Score: {}".format(self.score), True, YELLOW)
    x1 = (SCREEN_WIDTH - text1.get_width()) / 2
    text2 = self.font2.render("Press ENTER to try again".format(self.score), True, YELLOW)
    x2 = (SCREEN_WIDTH - text2.get_width()) / 2
    text3 = self.font3.render("Press SPACE to return to menu", True, YELLOW)
    x3 = (SCREEN_WIDTH - text3.get_width()) / 2

    self.engine.foreground_blit(text1, (x1, 32))

    if self.engine.get_ticks() % 1000 > 500:
      self.engine.foreground_blit(text2, (x2, 96))

    self.engine.foreground_blit(text3, (x3, 140))

  def restart(self):
    self.engine.setup_state('game', purge=True)

  def go_menu(self):
    self.engine.setup_state('menu')

  EVENT_BINDINGS = {
    K_RETURN: restart,
    K_SPACE: go_menu,
  }
