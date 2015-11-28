import sys, pygame
from pygame.locals import *

from consts import *
from object_manager import ObjectManagerMixin

import controllers

class BaseGameEngine(object):
  pass

class GameEngine(BaseGameEngine, ObjectManagerMixin):
  """Generic 2D game engine"""
  FRAMES_PER_SECOND = 30

  active_controllers = []

  def __init__(self):
    pygame.init()

    # Set up the screen
    self.screen = pygame.display.set_mode(
      (SCREEN_WIDTH, SCREEN_HEIGHT)
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

  def get_screen_sized_surface(self):
    return pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

  def create_controller(self, controller):
    new_controller = controller(self)
    # Set the game engine as the ObjectManager parent
    new_controller.object_super = self
    self.active_controllers.append(new_controller)

  def destroy_controller(self, controller):
    controller.destroy()
    self.active_controllers.remove(controller)

  def setup_state(self, state):
    """Remove old controllers, start a new state's controllers"""
    new_controllers = self.STATES[state]

    # Destroy controllers not in new state
    for controller in set(self.active_controllers) - set(new_controllers):
      self.destroy_controller(controller)

    # Add controllers not already running
    for controller in set(new_controllers) - set(self.active_controllers):
      self.create_controller(controller)

  def purge_controllers(self):
    """Destroy all controllers"""
    for controller in self.active_controllers:
      self.destroy_controller(controller)

  def event_handle(self, event):
    """Handle a single event"""
    if hasattr(event, 'key') and event.type == KEYDOWN:
      # Global key binding to quit things, set keep_alive to false to trigger
      #  quitting at the end of the current tick

      if event.key == K_ESCAPE: self.keep_alive = False

      # Debug commands
      if event.key == K_o: print self.objects # Print all active objects
      if event.key == K_c: print self.active_controllers # Print all active objects

      if event.key == K_n: self.post_event(E_WIN) # Debug make win state
      if event.key == K_m: self.post_event(E_DIE) # Debug make win state


      # Run event bindings in all the active controllers
      for controller in self.active_controllers:
        if event.key in controller.EVENT_BINDINGS:
          # Argument needed here to satisfy the need for self within method
          controller.EVENT_BINDINGS[event.key](controller)

    elif hasattr(event, 'game_event'):
      # Controller events
      for controller in self.active_controllers:
        if event.game_event in controller.EVENT_BINDINGS:
          controller.EVENT_BINDINGS[event.game_event](controller, event)

    elif event.type == pygame.QUIT:
      # Respond to the window manager's close button and all other cases of
      #  being asked to quit
      self.keep_alive = False

  def post_event(self, event, **kwargs):
    """Post a controller event"""
    ev = pygame.event.Event(pygame.USEREVENT, game_event = event, **kwargs)
    pygame.event.post(ev)

  def clear_foreground(self):
    self.foreground_surface = self.get_screen_sized_surface()

    # Set and fill with the colorkey (the colour that means transparent)
    self.foreground_surface.set_colorkey(COLORKEY)
    self.foreground_surface.fill(COLORKEY)

  def clear_background(self):
    self.background_surface = self.get_screen_sized_surface()

  def foreground_blit(self, surface, coord):
    self.foreground_surface.blit(surface, coord)

  def background_blit(self, surface, coord):
    self.background_surface.blit(surface, coord)

  def tick(self):
    """Main game loop"""
    # Tick the clock
    self.last_tick = self.clock.tick(self.FRAMES_PER_SECOND)

    # Events
    for event in pygame.event.get(): self.event_handle(event)

    # Clear the foreground
    self.clear_foreground()

    # Controller actions
    for controller in self.active_controllers: controller.tick()

    # Draw active objects to the foreground
    for obj in self.objects:
      obj_surface = obj.draw()
      if obj_surface:
        self.foreground_blit(obj_surface, obj.pos)

    self.screen.blit(self.background_surface, ORIGIN)
    self.screen.blit(self.foreground_surface, ORIGIN)

    # Flip the screen
    pygame.display.flip()

    # If we are going to quit, call the quit method
    if not self.keep_alive: self.quit()

  def quit(self):
    """Quit the game"""
    print "Game engine quitting"
    self.purge_controllers()
    pygame.quit()


class FroggerGameEngine(GameEngine):
  """Frogger specific game engine"""
  SCREEN_WIDTH = SCREEN_WIDTH # i have added this into the consts file
  SCREEN_HEIGHT = SCREEN_HEIGHT # i have added this into the consts file

  STATES = {
    'menu': [
      controllers.MenuController,
      controllers.FPSCounterController,
    ],
    'game': [
      controllers.GameController,
      controllers.PlayerController,
      controllers.LevelController,
      controllers.FPSCounterController,
      controllers.ScoreTextController,
    ],
    'gameover': [
      controllers.GameOverController,
    ]
  }

  STARTING_STATE = 'menu'
