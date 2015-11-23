import sys, pygame
from pygame.locals import *

from colours import *

import controllers

class GameEngine(object):
  """Generic 2D game engine"""
  FRAMES_PER_SECOND = 30

  active_controllers = []

  def __init__(self):
    pygame.init()

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

    # Setup initial state
    self.setup_state(self.STARTING_STATE)

  def get_ticks(self):
    # Can be got globally, but asking the engine for this feels nicer
    return pygame.time.get_ticks()

  def get_fps(self):
    """Return the framerate, computed from last 10 clocks"""
    return int(self.clock.get_fps())

  def setup_state(self, state):
    """Remove old controllers, start a new state's controllers"""
    new_controllers = self.STATES[state]

    # Close controllers not in new state
    for controller in set(self.active_controllers) - set(new_controllers):
      controller.close()
      self.active_controllers.remove(controller)

    # Add controllers not already running
    for controller in set(new_controllers) - set(self.active_controllers):
      self.active_controllers.append(controller(self))

  def event_handle(self, event):
    """Handle a single event"""
    if hasattr(event, 'key'):
      if event.key == K_ESCAPE: self.keep_alive = False

      for controller in self.active_controllers:
        if event.key in controller.EVENT_BINDINGS:
          controller.EVENT_BINDINGS[event.key](controller)

  def tick(self):
    """Main game loop"""
    # Tick the clock
    self.last_tick = self.clock.tick(self.FRAMES_PER_SECOND)

    # Events
    for event in pygame.event.get(): self.event_handle(event)

    # Controller actions
    for controller in self.active_controllers: controller.tick()

    # Flip the screen
    pygame.display.flip()

    # If we are going to quit, call the quit method
    if not self.keep_alive: self.quit()

  def quit(self):
    """Quit the game"""
    pygame.quit()


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
