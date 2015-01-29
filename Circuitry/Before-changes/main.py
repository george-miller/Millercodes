import pygame
from colors import *
from board import *
from levels import *
from states import *

'''
Circuitry
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
