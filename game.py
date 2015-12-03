import sys, pygame
from pygame.locals import *


from consts import *
from object_manager import ObjectManagerMixin

import controllers

class BaseGameEngine(object):
  pass

class GameEngine(BaseGameEngine, ObjectManagerMixin):
  """Generic 2D game engine"""
  FRAMES_PER_SECOND = 60

  active_controllers = []

  def __init__(self):
    super(GameEngine, self).__init__()

    pygame.init()

    # Set up the screen
    self.screen = pygame.display.set_mode(
      (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    self.screen.fill(WHITE)
    pygame.display.set_caption(self.GAME_TITLE)
    pygame.display.flip()

    # Set the application icon
    self.icon = pygame.image.load('images/{}'.format(self.ICON)).convert_alpha()
    pygame.display.set_icon(self.icon)

    # Set up the surfaces
    self.background_surface = self.get_screen_sized_surface()
    self.foreground_surface = self.get_screen_sized_surface()

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

  def create_controller(self, controller, messages):
    """Create a controller and append to the active_controllers list"""
    # Pass a reference to self, the engine, and any messages for this state change
    new_controller = controller(self, messages)
    self.active_controllers.append(new_controller)

  def destroy_controller(self, controller):
    """Remove a controller from the active state, calling that controller's
    destroy method"""
    controller.destroy()
    self.active_controllers.remove(controller)

  def setup_state(self, state, purge=False, messages={}):
    """Remove old controllers, start a new state's controllers"""
    # Add the requested state into the messages dict
    messages["state"] = state

    # Make a copy of active controller. This needs doing as looping over a list
    # while removing items from that list causes the for loop to mis-index.
    # Bug #17
    active_controllers_copy = list(self.active_controllers)
    new_controllers = self.STATES[state]

    # Destroy controllers not in new state
    for controller in active_controllers_copy:
      if controller.__class__ not in new_controllers or purge:
        self.destroy_controller(controller)

    # Add controllers not already running
    active_controller_classes = [c.__class__ for c in self.active_controllers]
    for controller in set(new_controllers) - set(active_controller_classes):
      self.create_controller(controller, messages)

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
      if event.key == K_F12: pygame.display.toggle_fullscreen()

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
    """Post a game event"""
    ev = pygame.event.Event(pygame.USEREVENT, game_event = event, **kwargs)
    pygame.event.post(ev)

  def get_screen_sized_surface(self):
    """Return a pygame screen sized surface with a transparent background"""
    return pygame.Surface(
      (self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
      pygame.SRCALPHA
    ).convert_alpha()

  def clear_foreground(self):
    """Clear the foreground surface"""
    self.foreground_surface.fill(pygame.SRCALPHA)

  def clear_background(self):
    """Clear the background surface"""
    self.background_surface.fill(BLACK)

  def set_background_image(self, image_path):
    """Fill the background with an image given its path"""
    bg_surf = pygame.image.load('images/{}'.format(image_path))
    self.background_blit(bg_surf, ORIGIN)

  def foreground_blit(self, surface, coord):
    """Draw a pygame surface to the foreground"""
    self.foreground_surface.blit(surface, coord)

  def background_blit(self, surface, coord):
    """Draw a pygame surface to the background"""
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

    # Sort objects by Z_INDEX
    self.objects.sort(key = lambda obj: obj.Z_INDEX)

    # Draw active objects to the foreground
    for obj in self.objects:
      # Cancel if object is set not to be drawn
      if not obj.visible: continue

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

  GAME_TITLE = 'Why Did The Chicken Cross The Road?'

  ICON = CHICKEN

  STATES = {
    'menu': [
      controllers.MenuController,
      controllers.FPSCounterController,
    ],
    'game': [
      controllers.GameController,
      controllers.PlayerController,
      controllers.LevelController,
      controllers.ScoreTextController,
      controllers.FPSCounterController,
	    controllers.SoundController,
      controllers.PopupController,
    ],
    'gameover': [
      controllers.GameController,
      controllers.GameOverController,
      controllers.FPSCounterController,
      controllers.HighScoreController,
    ],
    'highscores': [
      controllers.ScoreBoardController,
      controllers.FPSCounterController,
    ]
  }

  STARTING_STATE = 'menu'
