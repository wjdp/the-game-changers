import re
import csv
import random
import pygame
from pygame.locals import *

from consts import *
from object_manager import ObjectManagerMixin
from characters import *
from objects import *
from text import TextObject

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
    """Called after __init__, to be overridden by children"""
    pass

  def tick(self):
    """Called on each frame, to be extended by children"""
    self.tick_objects()

  def destroy(self):
    """Called on destroy, to be extended by children"""
    self.purge_objects()

class MenuController(Controller):
  """Draws the main menu, changes the game state to start the game on user input"""
  MENU_VOLUME = 0.3
  def create(self):
    self.engine.set_background_image(BG_MENU)

	#play menu music

    self.menu_music = pygame.mixer.Sound('sounds/GameMenu.wav')
    self.menu_music.set_volume(self.MENU_VOLUME)
    self.menu_music.play(-1)

    self.start_text = self.create_object(TextObject, self,
      font_size=64,
      pos=(0, SCREEN_HEIGHT - 80),
      centre=True,
      text="Press ENTER to start",
    )

    self.highscore_text = self.create_object(TextObject, self,
      font_size=16,
      pos=(0, SCREEN_HEIGHT - 20),
      centre=True,
      text="Press H to view highscores",
    )

  #Stopmusic
  def destroy(self):
    super(MenuController, self).destroy()
    pygame.mixer.stop()

  def start_game(self):
    self.engine.setup_state('game')

  def show_highscores(self):
    self.engine.setup_state('highscores')

  def tick(self):
    super(MenuController, self).tick()
    self.start_text.visible = self.engine.get_ticks() % 1000 > 500

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
    self.engine.set_background_image(BG_GAME)
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
    """Initialise the player object and controller instance variables"""
    self.player_object = self.create_object(Frog, self)
    self.max_height = 0
    self.current_height = 0
    self.movement_enabled = True

  def movement_allowed(self):
    """Check for if we're allowed to move"""
    return self.player_object.visible and self.movement_enabled

  def move_left(self):
    """Move to the left"""
    if not self.player_object.pos[0] <= self.LEFT_BOUND and self.movement_allowed():
      self.player_object.move((-1, 0))
      self.engine.post_event(E_HOP, direction=LEFT, progress=False)

  def move_right(self):
    """Move to the right"""
    if not self.player_object.pos[0] >= self.RIGHT_BOUND and self.movement_allowed():
      self.player_object.move((1, 0))
      self.engine.post_event(E_HOP, direction=RIGHT, progress=False)

  def move_up(self):
    """Move up"""
    if not self.player_object.pos[1] <= self.TOP_BOUND and self.movement_allowed():
      self.player_object.move((0, -1))

      self.current_height += 1
      progressed = self.max_height < self.current_height

      self.engine.post_event(E_HOP, direction=LEFT, progress=progressed)

      if progressed:
        self.max_height = self.current_height

  def move_down(self):
    """Move down"""
    if not self.player_object.pos[1] >= self.BOTTOM_BOUND \
      and self.movement_allowed():
      self.current_height -= 1
      self.player_object.move((0, 1))
      self.engine.post_event(E_HOP, direction=DOWN, progress=False)

  def reset(self, event):
    """Reset the player to the starting position"""
    self.player_object.move_to_start()
    self.player_object.visible = True

  def disable_movement(self, event):
    self.movement_enabled = False

  def enable_movement(self, event):
    self.movement_enabled = True

  def tick(self):
    super(PlayerController, self).tick()

    # Deal with collisions
    collision_object = self.player_object.collision_check()
    if collision_object and self.player_object.visible:
      if isinstance(collision_object, Car):
        # Collided with Car, so die
        self.player_object.visible = False
        self.engine.post_event(E_DIE)
      elif isinstance(collision_object, Hut):
        # Collided with Hut, so win
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

    E_DISABLE_MOVEMENT: disable_movement,
    E_ENABLE_MOVEMENT: enable_movement,
  }


class LevelController(Controller):
  """Creates the level (cars and huts), rearranges the level on reset event"""

  # Define the car generator variables
  # List of lanes, each element:
  # (num_of_cars, (delay_low, delay_high), speed_multiplier, images, width)
  LORRY_LANE_1 = (5, (4,5), .5, LORRIES, LORRY_WIDTH)
  LORRY_LANE_2 = (6, (2,5), .6, LORRIES, LORRY_WIDTH)

  TRUCK_LANE_1 = (5, (4,5), 0.2, TRUCKS, TRUCK_WIDTH)
  TRUCK_LANE_2 = (4, (2,3), 0.7, TRUCKS, TRUCK_WIDTH)
  TRUCK_LANE_3 = (5, (3,4), 1, TRUCKS, TRUCK_WIDTH)

  CAR_LANE_1 = (4, (4,6), 5, CARS, CAR_WIDTH)
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
    """Create the huts at game start"""
    self.huts = []
    for hut_pos in self.HUT_POSITIONS:
      self.huts.append(self.create_object(Hut, self, hut_pos))

  def reset(self, event):
    """Regenerate the level"""
    self.purge_objects(Car)

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

  EVENT_BINDINGS = {
    E_SOFT_RESET: reset
  }


class FPSCounterController(Controller):
  """Optional controller to show the FPS at the top of the screen"""

  FPS_POS = (300, 0)

  def create(self):
    self.fps_text = self.create_object(TextObject, self,
      text="0",
      pos=self.FPS_POS,
      colour = RED,
    )
    self.fps_text.visible = False

  def tick(self):
    super(FPSCounterController, self).tick()
    self.fps_text.set_text(self.engine.get_fps())

  def toggle_fps(self):
    """Toggle display of the framerate counter"""
    self.fps_text.visible = not self.fps_text.visible

  EVENT_BINDINGS = {
    K_f: toggle_fps,
  }


class ScoreTextController(Controller):
  """Shows the score and lives at the top of the screen, is updated by events
  sent by the GameController"""

  lives = None
  score = None

  EGG_ORIGIN = (SCREEN_WIDTH - (GRID * LIVES), 0)

  SCORE_FONT_SIZE = 27

  def create(self):
    # Create text objects
    self.score_text = self.create_object(TextObject, self,
      font_size=self.SCORE_FONT_SIZE,
      pos=(2,6),
    )
    self.lives_text = self.create_object(TextObject, self,
      font_size=self.SCORE_FONT_SIZE,
      pos=(self.EGG_ORIGIN[0] - 76, 6),
      text="Lives",
    )

    self.eggs = []

  def update(self, event):
    self.lives = event.lives
    self.update_score(event)

  def update_score(self, event):
    self.score_text.set_text("Score: {}".format(event.score))

  def update_eggs(self):
    # Remove all objects
    self.purge_objects(Egg)

    # Create objects (Eggs) to represent lives
    for i in range(self.lives):
      egg = self.create_object(Egg, self,
        pos=(self.EGG_ORIGIN[0] + (GRID * i), self.EGG_ORIGIN[1]))
      self.eggs.append(egg)

  def tick(self):
    super(ScoreTextController, self).tick()
    # If we need to update the eggs (Lives) do so
    if self.lives is not None and len(self.eggs) != self.lives:
      self.update_eggs()

  EVENT_BINDINGS = {
    E_SOFT_RESET: update,
    E_SCORE_CHANGED: update_score,
  }


class SoundController(Controller):
  """Plays sounds for the game state, plays reactionary sounds on events"""

  BACKGROUND_VOLUME = 0.4
  ROAD_VOLUME = 0.1

  def create(self):
	# Background music
    self.sound = pygame.mixer.Sound('sounds/GameSoundtrack.wav')
    self.sound.set_volume(self.BACKGROUND_VOLUME)
    self.sound.play(-1)

    # Background sound effect
    self.road = pygame.mixer.Sound('sounds/GameTraffic.wav')
    self.road.set_volume(self.ROAD_VOLUME)
    self.road.play(-1)

    # Preload sounds
    self.win = pygame.mixer.Sound('sounds/GameWin.wav')
    self.die = pygame.mixer.Sound('sounds/GameDie.wav')
    self.jump = pygame.mixer.Sound('sounds/Jump.wav')

  def destroy(self):
    """Stop all running sounds"""
    super(SoundController, self).destroy()
    pygame.mixer.stop()

  def win(self, event):
    """Play win sound"""
    self.win.play()

  def die(self, event):
    """Play die sound"""
    self.die.play()

  def jump(self, event):
    """Play jump sound"""
    self.jump.play()

  EVENT_BINDINGS = {
    E_WIN: win,
    E_DIE: die,
    E_HOP: jump,
  }


class PopupController(Controller):
  """Shows a popup on events (win, die)"""

  def create(self):
    # Initialise instance variables
    self.hide_popup = 0

  def show_popup(self, obj, duration=1000):
    """Show a popup"""
    popup = self.create_object(obj, self)
    popup.set_pos_centre()
    self.hide_popup = self.engine.get_ticks() + duration
    self.engine.post_event(E_DISABLE_MOVEMENT)

  def show_alive_popup(self, event):
    """Show the death popup"""
    self.show_popup(AliveChickenPopup)

  def show_death_popup(self, event):
    """Show the death popup"""
    self.show_popup(DeadChickenPopup)

  def tick(self):
    super(PopupController, self).tick()
    """Remove popups after their time is done"""
    if len(self.objects) > 0 and self.engine.get_ticks() > self.hide_popup:
      self.purge_objects()
      self.engine.post_event(E_ENABLE_MOVEMENT)

  EVENT_BINDINGS = {
    E_WIN: show_alive_popup,
    E_DIE: show_death_popup,
  }


class GameOverController(Controller):
  """Draws the gameover screen along with the player score"""
  GAMEOVER_VOLUME = 0.9
  def create(self):
    self.engine.set_background_image(BG_GAME_OVER)

    # Gameover sound
    self.gameOver = pygame.mixer.Sound('sounds/GameOver.wav')
    self.gameOver.set_volume(self.GAMEOVER_VOLUME)
    self.gameOver.play()

  def show_text(self, event):
    # Create the text objects
    self.score_text = self.create_object(TextObject, self,
      font_size=64,
      pos=(0, 32),
      centre=True,
      text="Your Score: {}".format(self.messages['score']),
    )

    self.restart_text = self.create_object(TextObject, self,
      font_size=32,
      pos=(0, 96),
      centre=True,
      text="Press ENTER to try again",
    )

    self.menu_text = self.create_object(TextObject, self,
      font_size=16,
      pos=(0, 140),
      centre=True,
      text="Press SPACE to return to menu",
    )

  def tick(self):
    super(GameOverController, self).tick()

    if self.objects:
      self.restart_text.visible = self.engine.get_ticks() % 1000 > 500

  def restart(self):
    """Restart the game"""
    self.engine.setup_state('game', purge=True)

  def go_menu(self):
    """Go to the menu"""
    self.engine.setup_state('menu')

  EVENT_BINDINGS = {
    K_RETURN: restart,
    K_SPACE: go_menu,
    E_SCORE_SAVED: show_text,
  }

class ScoreBoardController(Controller):
  #High Score #

  def create(self):
    self.engine.set_background_image(BG_SCORE_BOARD)    
    name_score = [] 

    with open("high_score.csv", 'rb') as f:
      high_score_reader = csv.reader(f)
      for line in high_score_reader:
        name_score.append(line)
    print name_score
        
    name_score.sort(key = lambda i: i[1])

    for j, x in enumerate(name_score[:10]):
      #py = (72+(24+4))
      board_name = (300,(24+(24+4))*j)
      board_score = (600, (24+(24+4))*j)

      self.create_object(TextObject, self,
        font_size=28,
        #pos=(0, 32),
        pos=board_name,
        text="{}".format(x[0])
        )

      self.create_object(TextObject, self,
        font_size=28,
        #pos=(0, 32),
        pos=board_score,
        text="{}".format(x[1])
        )

    self.create_object(TextObject, self,
      font_size=16,
      pos=(0, 140),
      centre=True,
      text="HIGH SCORE",
    )

    self.menu_text = self.create_object(TextObject, self,
      font_size=16,
      pos=(0, 140),
      centre=True,
      text="Press SPACE to return to menu",
    )

  def tick(self):
    pass

  def go_menu(self):
    self.engine.setup_state('menu')

  EVENT_BINDINGS = {
    K_SPACE: go_menu
    }


class HighScoreController(Controller):
  """Handles user input (their name) and saving their score to the scores file"""

  def create(self):
    self.name = ""
    self.engine.capture_text = True

    self.create_object(TextObject, self,
      text="Enter your name:",
      font_size=64,
      pos=(0, 24),
      centre=True,
    )

    self.name_text = self.create_object(TextObject, self,
      font_size=48,
      pos=(0, 24 + 64 + 6),
      centre=True,
      text="_"
    )

  def user_input(self, event):
    """Handle user input"""
    if re.match('^[\w-]+$', event.unicode):
      # Input is letters, add to self.name
      self.name += event.unicode
      self.update_name_text()
    elif event.key == K_RETURN:
      # Input is enter, save and return to gameover state
      self.save_score()
      self.engine.capture_text = False # Enable engine event handling
      self.engine.post_event(E_SCORE_SAVED)
      self.purge_objects() # Get rid of our text

  def update_name_text(self):
    """Update the text objects with user input"""
    self.name_text.set_text("{}_".format(self.name))
    self.name_text.set_pos_centre((1,0))

  def save_score(self):
    """Save the score to CSV file"""
    with open("high_score.csv", "a") as f:
      writer = csv.writer(f)
      writer.writerow((self.name, self.messages['score']))

  EVENT_BINDINGS = {
    E_TEXT_CAPTURE: user_input,
  }
