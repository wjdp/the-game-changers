import pygame
from pygame.locals import *

from consts import *
from objects import Object

class TextObject(Object):
  """Object subclass for text"""
  FONT_NAME = FONT_ACTION_MAN

  def __init__(self, controller, text="", font_size=32, pos=(0,0), centre=False, colour=YELLOW):
    super(TextObject, self).__init__(controller)
    # Create font object
    self.font = pygame.font.Font(self.FONT_NAME, font_size)
    self.colour = colour

    # Create the text surface
    self.set_text(text)

    # Set position
    if centre:
      self.pos = ((SCREEN_WIDTH - self.get_width()) / 2, pos[1])
    else:
      self.pos = pos

  def set_text(self, text):
    """Create and store a surface with the text parameter"""
    # Create the text surface
    self.text_surface = self.font.render(unicode(text), True, self.colour)
    # Store the text as string for reference
    self.text = text

  def get_width(self):
    """Get the width of the text surface"""
    return self.text_surface.get_width()

  def get_height(self):
    """Get the height of the text surface"""
    return self.text_surface.get_height()

  def draw(self):
    """Return the stored text surface"""
    return self.text_surface
