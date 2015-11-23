import sys, pygame
from pygame.locals import *

from colours import *

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

    # Keepalive
    self.keep_alive = True

  def event_handle(self, event):
    """Handle a single event"""
    if hasattr(event, 'key'):
      if event.key == K_ESCAPE: self.quit()

  def loop(self):
    """Main game loop"""
    # Events
    for event in pygame.event.get(): self.event_handle(event)

    # Tick the clock
    self.framerate = self.clock.tick(self.FRAMES_PER_SECOND)

  def quit(self):
    """Quit the game"""
    self.keep_alive = False

class FroggerGameEngine(GameEngine):
  """Frogger specific game engine"""
  SCREEN_WIDTH = 300
  SCREEN_HEIGHT = 500
