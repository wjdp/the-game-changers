# Main game script

from game import FroggerGameEngine

if __name__ == "__main__":
  print "Starting game..."
  engine = FroggerGameEngine()

  while engine.keep_alive:
    engine.loop()

  print "Game ended gracefully"
