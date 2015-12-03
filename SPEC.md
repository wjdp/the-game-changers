# G54PRG, The Game Changers

- Will Pimblett
- Anna Dodson
- Janice Atuahene
- Danielle Styles

## Project Spec

Develop a simple game in a group of 3-4 people. The game should include a graphical interactive component and it is suggested that you use the pygame api. E.g. you may implement an arcade game like tetris or space invaders.

The following criteria will contribute to your mark:

1. Quality of game play (40 %)
  - Is the game fun to play?
  - Does it look and sound good?
  - Is it free from errors?
  - Is it platform independent (i.e does it run on mac, windows and linux) ?

2. Software quality (40 %)
  - Good use of Python (objects, functions etc)
  - Reusable code
  - Is the code well documented?

3. Other factors (20 %)
  - Did the team work well together?
  - Are the instructions clear?
  - Did the demo go well?

The submission should include the following (as one zip file)

- Python source code (with comments explaining the structure of the code).
- Any other files required, e.g. graphics or soundfiles.
- A short installation instruction in a file README (<= 1 page)
- A short description of the game in a file called DESCRIPTION (<= 2 pages)
- A short statement describing the individual contribution to the project CONTRIB (<= 1 page)
- Each member of the group should submit their own copy (which should agree with the other team member's submission apart froom CONTRIB).

All group members have to show up the the scheduled demo and may be asked to explain part of the code during the demo.

The final mark will be based on the group marked and a moderated peer assessment. That is you will have to assess each others contribution to the project and based on this the mark will be split.

## Project Structure

- **game.GameEngine** - Generic game engine, deals with game state
  - Subclassed to **game.FroggerGameEngine**
- **controllers.Controller** - Generic systems controller, created by GameEngine, creates and manages Objects
  - **controllers.MenuController** - Deals with menu
  - **controllers.PlayerController** - Deals with user interaction while playing
  - **controllers.LevelController** - Deals with level generation and level runtime
- **objects.Object** - Generic 2D object
  - **objects.MovableObject** - 2D object that moves
- **characters.Character** - A MovableObject with behaviour
  - **characters.Frog** - The player's character
