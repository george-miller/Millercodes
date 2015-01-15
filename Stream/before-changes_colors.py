import pygame
import random

#colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)

#color list, used for streams and player
color_list = (GREEN,BLUE,CYAN,MAGENTA)

#size of the game window
window_height = 500
window_width = 300

#Player class, handles the state of the player
class Player(pygame.sprite.Sprite):
	#player midpoint velocity
	change_x = 0
	#player midpoint position
	mid = window_width/2
	#colors on either side of the midpoint
	color_left = random.randrange(4)
	color_right = random.randrange(4)
	#start with 200 health, 0 score, and not dead
	health = 200
	score = 0
	dead = False

	def __init__(self):
		super().__init__()
		#set the player's drawable area
		self.image = pygame.Surface((window_width,60))
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = window_height-60

	def update(self):
		#move the midpoint if necessary
		self.mid += self.change_x
		#fix if necessary
		if self.mid < 30:
			self.mid = 30
		if self.mid > window_width-30:
			self.mid = window_width-30
		#check if dead
		if self.health < 0:
			self.dead = True
		#check if more than full health
		if self.health > 200:
			#increase score by how much over the max the player is
			self.score += self.health - 200
			self.health = 200

		#these lines are for drawing the player
		#                     the left color        the drawable surface   shrink it in y
		self.image.fill(color_list[self.color_left],self.image.get_rect().inflate(0,-30))
		self.image.fill(color_list[self.color_right],self.image.get_rect().inflate(0,-30).move(self.mid,0))
		#these lines are for drawing the colors the player can switch to
		#basically get the drawable area and transform it a bunch of ways
		self.image.fill(color_list[(self.color_left+1)%len(color_list)], self.image.get_rect().inflate(-(window_width-30),-50).move(15-window_width/2,-20))
		self.image.fill(color_list[(self.color_left-1)%len(color_list)], self.image.get_rect().inflate(-(window_width-30),-50).move(15-window_width/2,20))
		self.image.fill(color_list[(self.color_left+2)%len(color_list)], self.image.get_rect().inflate(-(window_width-20),-55).move(10-window_width/2,-27))
		self.image.fill(color_list[(self.color_left-2)%len(color_list)], self.image.get_rect().inflate(-(window_width-20),-55).move(10-window_width/2,28))
		self.image.fill(color_list[(self.color_right+1)%len(color_list)], self.image.get_rect().inflate(-(window_width-30),-50).move(window_width/2-15,-20))
		self.image.fill(color_list[(self.color_right-1)%len(color_list)], self.image.get_rect().inflate(-(window_width-30),-50).move(window_width/2-15,20))
		self.image.fill(color_list[(self.color_right+2)%len(color_list)], self.image.get_rect().inflate(-(window_width-20),-55).move(window_width/2-10,-27))
		self.image.fill(color_list[(self.color_right-2)%len(color_list)], self.image.get_rect().inflate(-(window_width-20),-55).move(window_width/2-10,28))

#Class for each color stream.
#Handles the animation and decides when the stream color changes
class ColorStream(pygame.sprite.Sprite):

	#argument is x coord of left side
	def __init__(self,x):
		super().__init__()
		#set the drawable surface
		self.image = pygame.Surface((10,window_height-45))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = 0
		#set the color based on the player color
		#otherwise when starting a new game after losing,
		#youll probably lose again right away
		#(current_color is the color touching the top of the screen)
		if x < window_width/2:
			self.current_color = player.color_left
		else:
			self.current_color = player.color_right
		#this is to store each color as an int and its position in the stream
		self.color_duple_list = []

	def update(self):
		#move each color downward
		for duple in self.color_duple_list:
			duple[1] += 3
			#if we reach the player, remove the duple from the list
			if duple[1] > window_height:
				self.color_duple_list.remove(duple)

		#now draw
		#start with the current base color, the color that is touching the top of the screen
		self.image.fill(color_list[self.current_color])
		#then fill the stream with each color and its position down the stream
		for duple in self.color_duple_list:
			self.image.fill(color_list[duple[0]], self.image.get_rect().move(0,duple[1]))
		#see if we start a new color from the top
		if random.randrange(150) == 0:
			#add the new color at the top, using the current color
			self.color_duple_list.insert(0,[self.current_color,0])
			#set new current color to a random one
			self.current_color = random.randrange(len(color_list))

#class that manages the health bar. Mostly just change colors and draw the appropriate height
class HealthBar(pygame.sprite.Sprite):
	def __init__(self,player):
		super().__init__()
		#need the player to get the health
		self.player = player
		#drawable surface
		self.image = pygame.Surface((20,200))
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = window_height/2-100
	def update(self):
		self.image.fill(BLACK)
		health_color = GREEN
		#check if health is low, change color if so
		if self.player.health < 80:
			health_color = YELLOW
		if self.player.health < 40:
			health_color = RED
		#draw
		self.image.fill(health_color,self.image.get_rect().move(0,200-self.player.health))
#state of the game,
#0 is title screen
#1 is game
#2 is loss screen
state = 0

#start pygame, do normal stuff
pygame.init()
size = (window_width, window_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Streams")
done = False
clock = pygame.time.Clock()

#others holds player and health bar
#streams holds streams
others = pygame.sprite.Group()
streams = pygame.sprite.Group()
player = Player()
others.add(player)
others.add(HealthBar(player))
streams.add(ColorStream(95))
streams.add(ColorStream(145))
streams.add(ColorStream(195))

#game font
font = pygame.font.SysFont('Courier',25,True,False)

#list of words on start screen
start_screen_options = ("Start","Quit")
#currently selected word on start screen
selected_option = 0

#game loop
while not done:
	#start with black screen, each state has custom drawing code
	screen.fill(BLACK)
	#title screen
	if state == 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			#handle switching options
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					selected_option = (selected_option+1)%len(start_screen_options)
				elif event.key == pygame.K_UP:
					selected_option = (selected_option-1)%len(start_screen_options)
				elif event.key == pygame.K_RETURN:
					#choose!
					if selected_option == 0:
						#if start is selected, transition to state 1
						state = 1
					else:
						done=True

		i = 0
		#draw the words
		for opt in start_screen_options:
			bold = False
			if i == selected_option:
				bold = True
			screen.blit(font.render("{:^20}".format(opt),bold,WHITE),(0, 200+50*i))
			i += 1

	#game state
	elif state == 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.KEYDOWN:
				#movement
				if event.key == pygame.K_LEFT:
					player.change_x -= 3
				elif event.key == pygame.K_RIGHT:
					player.change_x += 3
				#color switching
				elif event.key == pygame.K_q:
					player.color_left = (player.color_left + 1)%len(color_list)
				elif event.key == pygame.K_a:
					player.color_left = (player.color_left - 1)%len(color_list)
				elif event.key == pygame.K_w:
					player.color_right =  (player.color_right + 1)%len(color_list)
				elif event.key == pygame.K_s:
					player.color_right = (player.color_right - 1)%len(color_list)
			#more movement
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					player.change_x += 3
				elif event.key == pygame.K_RIGHT:
					player.change_x -= 3
		#check for color matches
		for stream in streams.sprites():
			#get the player color
			if player.mid < stream.rect.x + 5:
				player_color = player.color_right
			else:
				player_color = player.color_left
			#if the stream is all one color currently, make sure not to try and access an empty array
			if len(stream.color_duple_list) > 0:
				stream_color = stream.color_duple_list[len(stream.color_duple_list)-1][0]
			else:
				stream_color = stream.current_color
			#check for a match, adjust the player health appropriately
			if stream_color == player_color:
				player.health += .6
			else:
				player.health -= 1
		
		#update and draw all sprites
		others.update()
		streams.update()
		others.draw(screen)
		streams.draw(screen)
		#draw the score
		screen.blit(font.render("{:>5d}".format(player.score),True,WHITE),(window_width - 80, 30))
		
		#if the player is dead, go to state 2
		if player.dead == True:
			state = 2

	#state of loss
	elif state == 2:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					#reset the game. This part could probably be improved,
					#I tried including a reset method but I didnt get it to work in time
					state = 0
					player.health = 200
					player.score = 0
					player.dead = False
					streams.empty()
					streams.add(ColorStream(95))
					streams.add(ColorStream(145))
					streams.add(ColorStream(195))
		#draw text for loss screen
		screen.blit(font.render("{:^20}".format("Game Over"),True,RED),(0,200))
		screen.blit(font.render("{:^20}".format("Score:{:>5d}".format(int(floor(player.score)))),False,WHITE),(0,250))
		screen.blit(font.render("{:^20}".format("press enter"),False,WHITE),(0,300))

	pygame.display.flip()

	clock.tick(60)

pygame.quit()
