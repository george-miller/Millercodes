import pygame
from colors import *
from levels import *
from board import *
import level_design
import level_gen

'''
FILE SUMMARY
This file contains class definitions for states of the game.
Game_State is the master state. It controls everything kind of.
Super_State is the state that all states inherit from.
Main_Menu is the state that displays when the game is launched
Level_Select is the state that displays when story is chosen
Main_Game controls the game. It is the old main game loop.
Victory_State is a simple state that displays score.
Exit_State is a state that exits the game after one call to update()

All states have init(), update(), and draw(). States optionally have prepare().
'''

'''
Game_State stores all values related to game operation.
It is passed to all states as an argument

done - whether the game is done running
score - the current score of the player
dirty - whether the canvas needs repainting
clock - all states share a clock
size - size of window
screen - screen Surface to draw on
level - what level is currently loaded
mouse - current mouse position tuple - updated every main loop
states - the different states the game can be in
state - which state the game is in
events - events to process
'''
class Game_State():
	def __init__(self):
		self.done = False
		self.score = 0
		self.dirty = True
		self.clock = pygame.time.Clock()
		self.size = (600,650)
		self.screen = pygame.display.set_mode(self.size)
		# This will hold which level we want from the LEVEL_DESIGN array is level_design.py
		self.level_type = 0
		# This will hold a reference to our instance of the Level class
		self.Level = Level(**level_design.LEVEL_DESIGN[self.level_type])
		# NOTE
		# level_type is either 0 if we are in arcade mode or a 1 if we are in story mode
		self.mouse = (0,0)
		self.state = 0
		self.states = [Main_Menu(self), Level_Select(self), Main_Game(self), Exit_State(self), Victory_State(self), Victory_State(self)]
		self.events = []
		self.completed = []
	def pause(self, frames):
		for i in range(frames):
			self.clock.tick(30)

'''
superclass for states.
allows us to neglect methods in certain states but still be able to call them.

prepare - only used by Main_Game, used to load a level before switching to the state
update - called every loop, performs most of the logic
draw - draws state to screen
highlight_rects - finds which rect is colliding with the mouse and returns the index of it in the passed list of rects
draw_rects - takes a list of rects and a list of strings along with a highlight index and draws the buttons that they represent
'''
class Super_State():
	def __init__(self, g):
		self.g = g
	def prepare(self):
		pass
	def update(self):
		pass
	def draw(self):
		pass
	def highlight_rects(self, button_rects, highlight):

		#set collide to -1, if it remains then the mouse is not hovering over anything
		collide = -1

		#collide mouse with each button rect
		for i in range(len(self.button_rects)):
			if self.button_rects[i].collidepoint(self.g.mouse):
				collide = i
				break

		#if what we are colliding with is not what is highlighted, set dirty and highlight
		if highlight != collide:
			self.g.dirty = True
			return collide
		return highlight

	# This method draws rects according to the arrays given
	def draw_rects(self, button_rects, button_labels, highlight, button_color):

		font = pygame.font.SysFont('Calibri', 50, False, False)
		for i in range(len(button_rects)):

			#create surfaces out of the rects
			button = pygame.Surface((button_rects[i].width,button_rects[i].height))
			button.fill(button_color)

			#set color of text according to highlight
			if i == highlight:
				color = GREEN
			else:
				color = WHITE

			#render the text, blit to button, blit to screen
			text = font.render(str(button_labels[i]), True, color)
			button.blit(text, (button_rects[i].width/2 - text.get_rect().width/2, button_rects[i].height/2 - text.get_rect().height/2))
			self.g.screen.blit(button, (button_rects[i].x, button_rects[i].y))

'''
Main Menu displayed at the start of every run of the program
lets user choose story, arcade, or quit
'''
class Main_Menu(Super_State):
	def __init__(self, g):
		#set g
		self.g = g

		#set the labels for the buttons we are going to draw
		self.button_labels = ('Story','Arcade','Quit')

		#highlight stores the index of the currently highlighted button
		self.highlight = -1

		#prebuild the rects for the buttons based on screen size
		self.button_rects = []
		self.step = self.g.screen.get_width()/25
		self.button_y = self.g.screen.get_height()/2-len(self.button_labels)*2*self.step
		for i in range(len(self.button_labels)):
			self.button_rects.append(pygame.Rect(g.screen.get_width()*3/8,self.button_y,self.g.screen.get_width()/4,self.step*2))
			self.button_y += self.step*4

	def update(self):

		#highlight the appropriate rect
		self.highlight = super().highlight_rects(self.button_rects, self.highlight)

		for event in self.g.events:
			if event.type == pygame.QUIT:
				self.g.done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:

				#if we clicked and something was highlighted, change state appropriately
				# if we clicked story
				if self.highlight == 0:
					self.g.level_type = 1 # make level_type be story
					
					#set dirty, we are going to have to repaint to reflect the new state
					self.g.dirty = True

					#state is highlight+1
					self.g.state = self.highlight+1

					#prepare the new state
					self.g.states[self.g.state].prepare()
				
				# if we hit arcade
				elif self.highlight == 1:
					self.g.level_type = 0 # set level_type to arcade
					
					self.g.dirty = True
					#state is highlight+1
					self.g.state = self.highlight+1

					#prepare the new state
					self.g.states[self.g.state].prepare()		
					
				# if we hit quit
				elif self.highlight == 2:
					self.g.done = True

	def draw(self):
		self.g.screen.fill(WHITE)
		super().draw_rects(self.button_rects, self.button_labels, self.highlight, BLACK)

		#done painting! no longer dirty.
		self.g.dirty = False

'''
this class handles selecting a level.
'''
class Level_Select(Super_State):
	def __init__(self, g):
		#set g
		self.g = g
		self.button_rects = []
		self.button_labels = range(1,26)
		step_x = g.screen.get_width()/5
		step_y = g.screen.get_width()/5
		self.highlight = -1
		#build list of rects for the buttons
		for i in range(5):
			for j in range(5):
				self.button_rects.append(pygame.Rect(step_x*j+step_x/4,step_y*i+step_y/4,step_x/2,step_y/2))

	def update(self):
		# get the new highlight
		self.highlight = super().highlight_rects(self.button_rects, self.highlight)

		#event handling
		for event in self.g.events:
			if event.type == pygame.QUIT:
				self.g.done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:

				#if we clicked and something was highlighted, change state appropriately
				if self.highlight >= 0:

					#set dirty, we are going to have to repaint to reflect the new state
					self.g.dirty = True

					#level is highlight+1
					self.g.Level.num = self.highlight+1

					#state is Main_Game
					self.g.state = 2

					#prepare the new state
					self.g.states[self.g.state].prepare()

	def draw(self):
		self.g.screen.fill(WHITE)
		# To draw the level select screen, we first make a list of completed rects
		completed_rects = []
		completed_labels = []
		# draw all the rects
		super().draw_rects(self.button_rects, self.button_labels, self.highlight, BLACK)
		for i in range(len(self.button_rects)):
			if i in self.g.completed:
				# must do i-1 because in self.button_rects, the rect numbered 1 is actually at array loaction 0
				completed_rects.append(self.button_rects[i-1])
				completed_labels.append(i)
		# draw over some rects to show they are completed
		super().draw_rects(completed_rects, completed_labels, self.highlight, GREEN)
		self.g.dirty = False

'''
this class handles the actual game. state 2.
'''
class Main_Game(Super_State):
	def __init__(self, g):
		#set g
		self.g = g
		self.ctrl = 1

	def prepare(self):
		
		
		# regenerate the pieces if we are playing a new arcade round
		if self.g.level_type == 0:
			self.g.Level.__init__(self.g.Level.num,50,1,10,10,level_gen.generate_level(10,10,3))
		else: # otherwise, make the new level from the list of story levels in level_design
			self.g.Level = Level(**level_design.LEVEL_DESIGN[self.g.Level.num])
		

	def update(self):
		#handle events
		for event in self.g.events:
			if event.type == pygame.QUIT:
				self.g.done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL:
					self.ctrl = -1
				if event.key == pygame.K_LSHIFT:
					self.ctrl = 2
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LCTRL:
					self.ctrl = 1
				if event.key == pygame.K_LSHIFT:
					self.ctrl = 1
			elif event.type == pygame.MOUSEBUTTONDOWN:
				# If we clicked somewhere on the top of the screen, outside the board
				if self.g.mouse[1]-self.textheight < 0:
					# specific positions for buttons can be found in board.py under headers()
					# If we are in the quit button
					if self.g.mouse[0] > self.g.screen.get_width()* (7/8):
						self.g.state = 0
						self.g.level_type = 0
					# If we are on the buy more moves button
					elif self.g.mouse[0] > self.g.screen.get_width() * (5/8) + 10:
						# Give them some more moves
						# This is where we would go to the shop screen if on a mobile device
						self.g.Level.moves = self.g.Level.moves + 10
				else:
					self.g.Level.turnTile(self.g.mouse[0], self.g.mouse[1]-self.textheight, self.ctrl) #Turn the tile clicked
					self.g.Level.calcPower() #Recalculate power for level
					if self.g.Level.done: #If you finished the level
						self.g.score += self.g.Level.getScore() #Add score
						self.g.Level.moves = 0 #Remove remaining moves
						self.draw()
						pygame.display.flip()
						self.g.pause(30) # wait a little for glory
						if self.g.level_type != 0: # if we are not in arcade mode
							# mark that we just completed a level in story mode
							self.g.completed.append(self.g.Level.num)
							# goto victory state for story mode
							self.g.state = 5
							
						# if we are in arcade mode, go to victory state for acrade mode
						else :
							self.g.state = 4
							
						self.g.Level.num = self.g.Level.num + 1 # increment the level number

				self.g.dirty = True

	def draw(self):
		self.g.screen.fill(WHITE)
		self.textheight = fullboard(self.g.screen, self.g.score, self.g.Level)
		self.g.dirty = False

'''
This state just displays a victory message and a score and lets you click a button 
'''
class Victory_State(Super_State):
	def __init__(self, g):
		self.g = g
		#only one button on this one, just create it.
		if self.g.state == 5:
			self.button_labels = ['Level Select']
		else:
			self.button_labels = ['Main Menu','Continue']
		self.button_rects = []
		# make two rects to be the buttons
		self.button_rects.append(pygame.Rect(g.screen.get_width()/4,g.screen.get_height()*3/4,g.screen.get_width()/2,g.screen.get_height()/10))
		self.button_rects.append(pygame.Rect(g.screen.get_width()/4,g.screen.get_height()*3/4 - g.screen.get_height()/8,g.screen.get_width()/2,g.screen.get_height()/10))
		self.highlight = -1
 
	def update(self):
		# check to see if our mouse has moved onto a button
		# if it has, set our highlight to that button
		self.highlight = super().highlight_rects(self.button_rects, self.highlight)

		#event handling
		for event in self.g.events:
			if event.type == pygame.QUIT:
				self.g.done = True
			elif event.type == pygame.MOUSEBUTTONDOWN:

				#if we clicked and something was highlighted, change state appropriately
				# If we clicked the main menu button
				if self.highlight == 0:

					#set dirty, we are going to have to repaint to reflect the new state
					self.g.dirty = True

					#we go back to the default level (random)
					self.g.level_type = 0

					#state is Main menu
					self.g.state = 0
				# If we clicked the continue button
				elif self.highlight == 1:
					# reset things
					self.g.dirty = True
					
					# move to main game state and prepare
					self.g.state = 2
					self.g.states[self.g.state].prepare()

	def draw(self):
		self.g.screen.fill(WHITE)
		# draw the rects
		super().draw_rects(self.button_rects, self.button_labels, self.highlight, BLACK)

		#Calibri, size 50, not bold, not italic
		font = pygame.font.SysFont('Calibri', 50, False, False)

		#just draw this text
		text = font.render('You win!', True, BLACK)
		self.g.screen.blit(text, (self.g.screen.get_width()/2 - text.get_rect().width/2, self.g.screen.get_height()/4))
		text = font.render('Score: '+str(self.g.score), True, BLACK)
		self.g.screen.blit(text, (self.g.screen.get_width()/2 - text.get_rect().width/2, self.g.screen.get_height()*3/8))

		#done painting! no longer dirty.
		self.g.dirty = False


'''
simple state to transition to when the user wants to quit
kills the program after one update
'''
class Exit_State(Super_State):
	def __init__(self, g):
		self.g = g

	def update(self):
		self.g.done = True
