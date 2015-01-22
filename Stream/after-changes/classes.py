
import pygame
import random

# This file contains the classes used in streams: Player, Colorblock, ColorStream

#size of the game window
window_height = 500
window_width = 300

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

# Initialize some variables
colorblocks = pygame.sprite.Group()

#Player class, handles the state of the player
class Player(pygame.sprite.Sprite):
	
	score = 0.0
	

	def __init__(self, mode):
		super().__init__()
		# mode is a way to make the player have one or two paddles (three not supported)
		# if mode = 1, there's one paddle if mode = 2, there's 2 paddles
		self.mode = mode
		
		#player midpoint velocity
		self.change_x = 0
		
		# The two paddles will be start self.paddle_gap away from the midpoint on either side, then continue self.paddle_width
		self.mid = window_width/2
		self.paddle_gap = 20
		self.paddle_width = 60
		
		#colors for each paddle
		self.color_left = random.randrange(4)
		self.color_right = random.randrange(4)
		
		
		# The carosel for displaying next and previous colors to the player
		self.carosel = pygame.image.load("carosel.png").convert()
		self.carosel.set_colorkey((255,255,255))
		
		# Additional carosels must be created so that we can rotate them without harming the original
		self.carosel0 = self.carosel
		self.carosel1 = self.carosel
		
		#set the player's drawable area
		self.image = pygame.Surface((window_width,60))
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = window_height-100
		# self.y will be changed and self.rect.y will be set to self.y because we need a floating point number to keep the position
		self.y = self.rect.y + 0.0
		
		

	def update(self):		
		
		global initiated
		global state
		# set the position to the float
		self.rect.y = self.y
		
		#move the midpoint if necessary
		self.mid += self.change_x
		
		#fix if necessary
		if self.mid < 50:
			self.mid = 50
		elif self.mid > window_width-50:
			self.mid = window_width-50
		
		
		
		# reset the surface for more drawing
		self.image.fill((0,0,0))
		
		# This handles drawing the paddles
		# I had to create a rect object because I needed the rect.x field, since inflate() keeps the midpoint the same and changes x and y positions
		if self.mode == 2:
			# Don't draw the right paddle if it's one paddle mode
			rect = self.image.get_rect().inflate(-(window_width-self.paddle_width), -30)
			self.image.fill(color_list[self.color_right], rect.move(self.mid - rect.x + self.paddle_gap,-10))
		rect = self.image.get_rect().inflate(-(window_width-self.paddle_width), -30)
		self.image.fill(color_list[self.color_left], rect.move(self.mid-rect.right - self.paddle_gap,-10))
		
	def draw(self,screen):
		# draw self.image and draw carosels
		# set the carosels to their default
		self.carosel0 = self.carosel
		self.carosel1 = self.carosel
		screen.blit(self.image, (self.rect.x,self.rect.y))
		# rotate carosels and then draw them
		if self.mode == 2:
			screen.blit(pygame.transform.rotate(self.carosel0,(self.color_right*45) +117.5), (window_width-30, self.rect.y))
		screen.blit(pygame.transform.rotate(self.carosel1,(self.color_left*45) +117.5), (-35, self.rect.y))




class Colorblock(pygame.sprite.Sprite):
	"""This class represents a piece of a stream that is falling from the top of the screen to the bottom.
	This class controls collision with the player and score calculations"""
	
	def __init__(self, color, x, width, height):
		super().__init__()
		# color stored as an int
		self.color = color
		# NOTE - The height atttribute serves as downward speed as well because if downward speed was greater than height
		# the blocks would seperate
		self.height = height
		self.image = pygame.Surface((width,height))
		self.rect = self.image.get_rect()
		# This makes the rect.x start at the midpoint of the colorblock instead of the left side
		# This way, it makes width changes look smoother because it is changed on both sides, not just one
		self.rect.x = x - (width/2)
		self.rect.y = 0
		self.image.fill(color_list[self.color])
	def update(self, player):
		# This is why height must be the same as speed.  If we were to have a speed variable of 2, and a height of 1, then there
		# would be a seperating between the individual color blocks as they are moving down the screen.  Similiarly, if speed was
		# less than height, then there would be overlapping colorblocks
		self.rect.y += self.height
		
		# when within the player's paddle y values
		if self.rect.y >= player.rect.y and self.rect.y < player.rect.bottom:
			
			if player.mode == 2 and self.rect.x >player.mid+player.paddle_gap and self.rect.right < player.mid+player.paddle_gap+player.paddle_width:
				# we hit the right paddle
				if self.color == player.color_right:
					#player.health += 1
					player.score += 1
					player.y -=.2
				# if the wrong color is on the paddle we hit
				else:
					#player.health -= 1
					player.score -= .6
					player.y += .2
				colorblocks.remove(self)
			elif self.rect.right < player.mid-player.paddle_gap and self.rect.x > player.mid - player.paddle_gap - player.paddle_width:
				# we hit the left paddle
				if self.color == player.color_left:
					#player.health+= 1
					player.score += 1
					player.y -=.2
				# if the wrong color is on the paddle we hit
				else:
					#player.health -= 1
					player.score -= .6
					player.y += .2
				colorblocks.remove(self)
		elif self.rect.y > window_height:
			# If the player misses a block and it goes off the screeen, remove it from the sprites and decrease score
			colorblocks.remove(self)
			player.score -= .6
		


class ColorStream():
	"""This class creates blocks and adds them to the colorblocks sprites list.  A ColorStream object is essentially a source point for colorblocks"""
	#argument is x coord of left side
	def __init__(self,x,color,width, height, randchance, width_change):
		# This float determines whether the colorstream will change the width of colorblocks as it is going
		# If this is zero, it won't change but if it's nonzero, the width will change according to random numbers
		# If nonzero, the initial value of width_change will determine to range of how fast it can change.  Say width_change
		# is .4, then the speed of change will be random from -.4 to .4.  If width change is 1, the speed of change will
		# be a random number from -1 to 1
		self.width_change = width_change
		self.width_rand_range = width_change
		
		# This variable determines how fast to change color, the higher the less the lower the more
		self.randchance = randchance
		self.x = x
		self.x_speed = (random.random()*2) -1
		self.current_color = color
		self.left = x
		# current width of blocks coming down
		self.width = width
		# current height/speed of blocks coming down
		self.height = height
		self.right = self.left+width
		self.x_range = 60
		
	def update(self):
		# These 4 lines set the speed to a random value in the current direction.
		if self.x_speed > 0:
			self.x_speed = random.random()
		elif self.x_speed < 0:
			self.x_speed = -random.random()
		# Increment x position	
		self.x += self.x_speed
		# If we are not within the proper ranges, switch the sign of our speed so we go the other way
		if self.x > self.left + self.x_range or self.x < self.left - self.x_range:
			self.x_speed *= -1
		
			
		if self.width_change != 0:
			self.width_change = (random.random()*(self.width_rand_range*2)) - self.width_rand_range
			# If this becomes zero, it won't change the width after this frame and we don't want that because
			# initialization determined that we want the width to be changing
			if self.width_change == 0:
				self.width_change += .01
			self.width += self.width_change
			# Make sure we stay within acceptable ranges
			# the '60' is supposed to be player.paddle_width
			if self.width > 60 -15:
				self.width = 60 -15
			elif self.width < 20:
				self.width = 20
			
			
		# drop some colorblocks from the stream starting point
		self.drop_color(self.current_color,self.width, self.height)
		# chance to change the current color
		if random.randrange(self.randchance) == 0:
			self.current_color = random.randrange(4)
		
		
		
			
	
	def drop_color(self,color, width,height):
		# Simply create a colorblock and add it to the sprite list
		block = Colorblock(color,self.x, width,height)
		colorblocks.add(block)
		