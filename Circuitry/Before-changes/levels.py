'''
bugs found:
calcPower() would sometimes try and calc the Power of a tile that lies off the board
lastTiles array fix for endless looping did not allow for more than one tile to try and power a tile
this is in main but only redraw when needed.

TODO: I'd like to switch the implementation of power calculation from switch blocks to wire directions.
	  The code will be harder to read but then the type of tile can be separated from the wires.
	  useful for special tiles maybe.
	  or different color wires.
	  also the logic will be nicer.
	  
	  Fix the mechanism for using randomly generated levels vs premade ones.

	  Also make a better random generation algorithm
'''
import pygame
from colors import *

LINE_WIDTH = 4
BORDER_WIDTH = 2


#This class defines each level and hold all the logic functions for the board
class Level():
	#This is the initialization function
	def __init__(self, num, moves, multiplier, width, height, pieces):
		self.num = num #Level number
		self.tile_height = height #Number of rows
		self.tile_width = width #Number of columns
		
		self.moves = moves #Moves the player is allowed to make
		self.multiplier = multiplier #Score multiplier for remaining moves
		
		self.tile_size = (0, 0) #Holding value for time draw size

		self.pieces = pieces
		
		self.tiles = [] #Grid of tile class objects
		for row in range(self.tile_height):
			self.tiles.append([]) #Creating second index for array
			for col in range(self.tile_width):
				self.tiles[row].append(Tile(pieces[row][col][0],pieces[row][col][1],(row,col))) #Initialize each tile object
		
		self.calcPower() #Calculate initial power values for tiles
		
	#This is the function used to draw the board on screen
	def draw(self, screen, size):
		self.tile_size = (size, size)
		
		for row in self.tiles:
			for tile in row:
				tile.draw(screen, size)
	
	#This function changes the orientation of a certian tile
	def turnTile(self,x,y,d):
		if self.moves > 0: #If there are no moves, do not turn tile
			self.moves -= 1 #Remove one move from the level
			col = int(x / self.tile_size[0]) #Calculate tile from mouse position
			row = int(y / self.tile_size[1]) #Calculate tile from mouse position
			
			self.tiles[row][col].turn(d) #Call tile function to turn
		
	def calcPower(self):
		#Set all tile power to false
		for i in range(len(self.tiles)):
			for j in range(len(self.tiles[i])):
				self.tiles[i][j].power = False
		
		#Find all starting tiles
		for i in range(len(self.tiles)):
			for j in range(len(self.tiles[i])):
				if self.tiles[i][j].type == 'start':
					self.tiles[i][j].calcPower(self, (0,0))
		
		#Search for all end tiles to determine if the level is complete
		self.done = True
		for i in range(len(self.tiles)):
			for j in range(len(self.tiles[i])):
				if self.tiles[i][j].type == 'end' and not self.tiles[i][j].power:
					self.done = False
	
	#Calculate score for level
	def getScore(self):
		return self.moves * self.multiplier
	
	#Try to find a certain tile from coordinates
	def getTile(self, i, j):
		if i in range(len(self.tiles)):
			if j in range(len(self.tiles[i])):
				return self.tiles[i][j]
		
#This class defines each tile and its functions
class Tile():
	#Initialization function
	def __init__(self, type, orientation, pos):
		self.type = type #Type of tile
		self.orientation = orientation #Orientation as an integer {"UP":0,"RIGHT":1,:"DOWN":2,"LEFT":3}
		### Should convert orientation to string for readbility ####
		
		self.pos = pos #Position of tile on board in a tuple (row,col)
		
		self.power = False #Boolean if tile is powered
		
	#Draws tile and stamps on board
	def draw(self, screen, size, textheight = 0):
		#Set the color of lines
		if self.power or self.type == 'start':
			color = GREEN
		else:
			color = RED
		
		#Draw piece border
		pygame.draw.rect(screen, BLACK, [self.pos[1]*size, self.pos[0]*size + textheight, size, size], BORDER_WIDTH)
		
		#Create surface for piece art
		piece = pygame.Surface((size-BORDER_WIDTH,size-BORDER_WIDTH))
		piece.fill(WHITE)
		
		##### Piece art requires accounting for LINE_WIDTH and BORDER_WIDTH in order to properly center ######
		
		#Lines are a simple line down the middle
		if self.type == 'line':
			pygame.draw.line(piece, color, [(size-LINE_WIDTH)/2, 0], [(size-LINE_WIDTH)/2, size], LINE_WIDTH)
		
		#Elbows are a 90 degree bend to the right drawn with two lines
		elif self.type == 'elbow':
			pygame.draw.line(piece, color, [(size-LINE_WIDTH)/2, 0], [(size-LINE_WIDTH)/2, size/2], LINE_WIDTH)
			pygame.draw.line(piece, color, [(size-LINE_WIDTH)/2, (size-LINE_WIDTH)/2], [size, (size-LINE_WIDTH)/2], LINE_WIDTH)
			
		#Tees are a t-shape with the longer line vertical and the shorter line extending to the right
		elif self.type == 'tee':
			pygame.draw.line(piece, color, [(size-LINE_WIDTH)/2, 0], [(size-LINE_WIDTH)/2, size], LINE_WIDTH)
			pygame.draw.line(piece, color, [(size-LINE_WIDTH)/2, (size-LINE_WIDTH)/2], [size, (size-LINE_WIDTH)/2], LINE_WIDTH)

		#Crosses are shaped like a cross. Wires go in 4 directions.
		elif self.type == 'cross':
			pygame.draw.line(piece, color, [(size-LINE_WIDTH)/2, 0], [(size-LINE_WIDTH)/2, size], LINE_WIDTH)
			pygame.draw.line(piece, color, [0, (size-LINE_WIDTH)/2], [size, (size-LINE_WIDTH)/2], LINE_WIDTH)

		#Start is a circle with one line extending up
		elif self.type == 'start':
			pygame.draw.line(piece, color, [(size-LINE_WIDTH)/2, (size-LINE_WIDTH)/2], [(size-LINE_WIDTH)/2, 0], LINE_WIDTH)
			# Draw an ellipse, using a rectangle as the outside boundaries
			pygame.draw.ellipse(piece, color, [size/4-BORDER_WIDTH/2, size/4-BORDER_WIDTH/2, size/2, size/2], 0)
			
		#End is a circle with one line extending up
		elif self.type == 'end':
			pygame.draw.line(piece, color, [(size-LINE_WIDTH)/2, (size-LINE_WIDTH)/2], [(size-LINE_WIDTH)/2, 0], LINE_WIDTH)
			# Draw an ellipse, using a rectangle as the outside boundaries
			pygame.draw.ellipse(piece, color, [size/4-BORDER_WIDTH/2, size/4-BORDER_WIDTH/2, size/2, size/2], 0)
		
		
		piece = pygame.transform.rotate(piece, -90*self.orientation) #Rotate the piece depending on its orientation
		screen.blit(piece, [self.pos[1]*size + BORDER_WIDTH, self.pos[0]*size + textheight + BORDER_WIDTH]) #Stamp the piece on the board
	
	def turn(self, d):
		if self.type not in ['start', 'end']: #You cannot turn start and end pieces
			self.orientation = (self.orientation + d) % 4 #All turns are clockwise
	
	#Function to calculate current tile power and find connected tiles
	def calcPower(self, level, lastTile):

		#if the tile already has power, then that means we have already calculated it's neighbors' power
		#solves endless looping problem in a situation where four tiles are all powering eachother
		#needed after removing the lastTiles list method of loop prevention
		if self.power == True:
			return

		#lastTile is a relative position tuple of the previously computed tile
		#lastTiles is a list of all previously computed tiles, to prevent endless looping
		
		nextTiles = [] #This is a list of all tiles connected to current tile
		
		#Logic for start tiles
		if self.type == 'start':
			#Start tiles are always powered and connect to one tile
			self.power = True
			if self.orientation == 0: #If pointed up
				nextTiles.append(level.getTile(self.pos[0]-1, self.pos[1])) #Add the tile directly above
			elif self.orientation == 1:
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]+1))
			elif self.orientation == 2:
				nextTiles.append(level.getTile(self.pos[0]+1, self.pos[1]))
			elif self.orientation == 3:
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]-1))
		
		#Logic for end tiles
		if self.type == 'end':
			if self.orientation == 0 and lastTile == (-1,0): #If pointed up and last tile was above
				self.power = True #The end tile is powered
			elif self.orientation == 1 and lastTile == (0,1):
				self.power = True
			elif self.orientation == 2 and lastTile == (1,0):
				self.power = True
			elif self.orientation == 3 and lastTile == (0,-1):
				self.power = True
		
		#Logic for line tiles
		elif self.type == 'line':
			if self.orientation in [0,2] and lastTile in [(-1,0),(1,0)]: #If pointed up/down and last tile was above/below
				self.power = True
				nextTiles.append(level.getTile(self.pos[0]-1, self.pos[1]))
				nextTiles.append(level.getTile(self.pos[0]+1, self.pos[1]))
			elif self.orientation in [1,3] and lastTile in [(0,-1),(0,1)]:
				self.power = True
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]+1))
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]-1))
		
		#Logic for elbow tiles
		elif self.type == 'elbow':
			if self.orientation in [0] and lastTile in [(-1,0),(0,1)]: #If pointed up and last tile was above or to the left
				self.power = True
				nextTiles.append(level.getTile(self.pos[0]-1, self.pos[1]))
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]+1))
				
			if self.orientation in [1] and lastTile in [(0,1),(1,0)]:
				self.power = True
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]+1))
				nextTiles.append(level.getTile(self.pos[0]+1, self.pos[1]))
				
			if self.orientation in [2] and lastTile in [(1,0),(0,-1)]:
				self.power = True
				nextTiles.append(level.getTile(self.pos[0]+1, self.pos[1]))
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]-1))
				
			if self.orientation in [3] and lastTile in [(0,-1),(-1,0)]:
				self.power = True
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]-1))
				nextTiles.append(level.getTile(self.pos[0]-1, self.pos[1]))

		#Logic for tee tiles
		elif self.type == 'tee':
			if self.orientation in [0] and lastTile in [(1,0),(-1,0),(0,1)]:
				self.power = True
				nextTiles.append(level.getTile(self.pos[0]+1, self.pos[1]))
				nextTiles.append(level.getTile(self.pos[0]-1, self.pos[1]))
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]+1))
			if self.orientation in [1] and lastTile in [(0,-1),(0,1),(1,0)]:
				self.power = True
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]-1))
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]+1))
				nextTiles.append(level.getTile(self.pos[0]+1, self.pos[1]))
			if self.orientation in [2] and lastTile in [(1,0),(-1,0),(0,-1)]:
				self.power = True
				nextTiles.append(level.getTile(self.pos[0]+1, self.pos[1]))
				nextTiles.append(level.getTile(self.pos[0]-1, self.pos[1]))
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]-1))
			if self.orientation in [3] and lastTile in [(-1,0),(0,1),(0,-1)]:
				self.power = True
				nextTiles.append(level.getTile(self.pos[0]-1, self.pos[1]))
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]+1))
				nextTiles.append(level.getTile(self.pos[0], self.pos[1]-1))

		#Logic for cross tiles
		elif self.type == 'cross':
			self.power = True
			nextTiles.append(level.getTile(self.pos[0]+1,self.pos[1]))
			nextTiles.append(level.getTile(self.pos[0]-1,self.pos[1]))
			nextTiles.append(level.getTile(self.pos[0],self.pos[1]+1))
			nextTiles.append(level.getTile(self.pos[0],self.pos[1]-1))
		
		for row in nextTiles: #Loop through nextTiles
			# sanity check, if row == None it means that it is off the board
			if row != None:
				lastTile = (self.pos[0] - row.pos[0], self.pos[1] - row.pos[1]) #Set relative position
				row.calcPower(level, lastTile) #Calculate next tile


