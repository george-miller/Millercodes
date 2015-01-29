import pygame
from colors import *
from board import *
from levels import *
from states import *

'''
Circuitry

Version 3.0

NEW Features!
- All navigation works as advertised (continue goes to next level, main menu goes to main menu, etc)
- There are levels 1-8 in story mode
- Arcade mode smartly chooses 1 end of the ones created by the creation algorithm absed on path length
- Arcade mode is now infinite
- Various code cleanups (e.g. in level select the completed levels now highlight correctly), and more comments

Possible futute enhancements:
- More levels
- save file for keeping track of highscore and the completed levels
'''

pygame.init()
pygame.display.set_caption("Circuitry")

#the Game_State object stores all data related to game operation.
#see states.py for more details
g = Game_State()
while not g.done:
	g.mouse = pygame.mouse.get_pos()
	g.events = pygame.event.get()
	#every state has an update function
	g.states[g.state].update()
	#dirty if canvas needs repainting
	if g.dirty:
		g.states[g.state].draw()
	pygame.display.flip()
	g.clock.tick(30)
pygame.quit()
