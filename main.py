# Main game script

from game import FroggerGameEngine

if __name__ == "__main__":
  print "Starting game..."
  engine = FroggerGameEngine()

  # Main game loop, tick uses pygame.time.Clock to make this loop run at a
  #  sensible speed
  while engine.keep_alive:
    engine.tick()

  print "Game ended gracefully"
