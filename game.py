import sys, pygame
from pygame.locals import *

from colours import *

import controllers

class GameEngine(object):
  """Generic 2D game engine"""
  FRAMES_PER_SECOND = 30

  def __init__(self):
    # Set up the screen
    self.screen = pygame.display.set_mode(
      (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
    )
    self.screen.fill(WHITE)
    pygame.display.flip()

    # Set up the clock
    self.clock = pygame.time.Clock()

    # Keep alive, program should terminate when False
    self.keep_alive = True

    # Initialise controller storage
    self.active_controllers = []

    # Setup initial state
    self.setup_state(self.STARTING_STATE)

  def setup_state(self, state):
    # Initialise controllers
    for controller in self.STATES[state]:
      self.active_controllers.append(controller(self))

  def close_state(self):
    # Destroy controllers
    pass

  def event_handle(self, event):
    """Handle a single event"""
    if hasattr(event, 'key'):
      if event.key == K_ESCAPE: self.quit()

  def tick(self):
    """Main game loop"""
    # Tick the clock
    self.framerate = self.clock.tick(self.FRAMES_PER_SECOND)

    # Events
    for event in pygame.event.get(): self.event_handle(event)

    # Controller actions
    for controller in self.active_controllers: controller.tick()

    # Flip the screen
    pygame.display.flip()

  def quit(self):
    """Quit the game"""
    self.keep_alive = False

class FroggerGameEngine(GameEngine):
  """Frogger specific game engine"""
  SCREEN_WIDTH = 300
  SCREEN_HEIGHT = 500

  STATES = {
    'menu': [controllers.MenuController],
    'game': [
      controllers.PlayerController,
      controllers.LevelController,
    ],
    'gameover': [controllers.GameOverController]
  }

  STARTING_STATE = 'menu'
