import random
import math
import pygame
import level_design
'''
This module generates two-dimensional arrays to be used for levels in Circuitry
The format for each entry is (string type, int orientation)
'''

'''
this class stores the status of each cell of the grid.
i and j are position (row, col)
walls are broken down as the algorithm traverses the grid.
a broken wall signifies an open path, aka a wire ending.
walls are stored as a list of boolean values corresponding to [up, right, down, left]
visited records whether we have already traversed that cell.
'''
class Cell():
	def __init__( self , i , j ):
		self.i = i
		self.j = j
		self.walls = [True,True,True,True]
		self.visited = False
	
	#used for determining the type of tile the cell corresponds to
	def count_walls(self):
		count = 0
		for wall in self.walls:
			if wall == True:
				count += 1
		return count

'''
this is the class that does the legwork (haha) in traversing the grid.
basically the algorithm is a depth-first traversal (look up an animation for depth first maze algorithm)
at each cell, it chooses a random unvisited direction to travel
when it reaches a dead end, it returns to the last cell at which it had a choice of where to go and resumes.
'''
class LevelGen():
	def __init__(self, rows, columns):
		# multiple ends are created in this creation algorithm.  We need to keep one and remove the rest
		# this array will be a list of lengths of paths from the start to an end.  It will be like this [pathLength, (endLoci, endLocj),...]
		# It will help to get the length of the paths so that we can decide which end to make the real end
		# For more on this array, look in the generate_level method and you will see a print statment.  Uncomment it and
		# run the game to see it in action.  format: (end1pathlength, (end1posx,end1posy), end2pathlength, ...)
		self.maximum = []
		#level_array stores the cells as we traverse the grid
		self.level_array = []
		self.rows = rows
		self.columns = columns
		#build the grid and populate it with cells
		for i in range(self.rows):
			self.level_array.append([])
			for j in range(self.columns):
				self.level_array[i].append(Cell(i,j))



	'''
	this is the recursive method that we use to traverse the grid
	args: cell = current cell, d is a tuple (change in Row, change in Col) of where we came from
	and current is a int that stores the current path length
	'''
	def visit(self, cell, d, current):
		#if we have been here, do nothing.
		if cell.visited == True:
			return
		#otherwise, mark it.
		cell.visited = True
		
		# Increment current
		current = current + 1
		
		
		#these two lines break down the walls.
		#d is a tuple that stores (dRow, dCol)
		#wall of current cell facing the direction we came from
		cell.walls[ 1 + d[0] - d[1] + (d[1]%2) ] = False
		#wall of old cell facing the direction we went
		self.level_array[ cell.i + d[0] ][ cell.j + d[1] ].walls[ 1 - d[0] + d[1] + (d[1]%2) ] = False
		
		
		
		#add all valid adjacent cells to toVisit. Check if they are visited later.
		toVisit = []
		if cell.i > 0 and not(self.level_array[cell.i-1][cell.j].visited):
			toVisit.append((cell.i-1,cell.j))
		if cell.i < self.rows-1 and not(self.level_array[cell.i+1][cell.j].visited):
			toVisit.append((cell.i+1,cell.j))
		if cell.j > 0 and not(self.level_array[cell.i][cell.j-1].visited):
			toVisit.append((cell.i,cell.j-1))
		if cell.j < self.columns-1 and not(self.level_array[cell.i][cell.j+1].visited):
			toVisit.append((cell.i,cell.j+1))
		
		# If we are at an end, add it to our list of paths	
		if len(toVisit) == 0:
			# we add current which now is the length from the start to this end piece
			self.maximum.append(current)
			# And the position of this cell which is now an end piece
			self.maximum.append( (cell.i, cell.j) )
			
		#we loop through the list randomly, removing as we go.
		#we return to this loop every time visit returns.
		while len(toVisit) > 0:
			#choose one
			this_one = toVisit[random.randrange(len(toVisit))]
			#visit it, passing the new cell and the direction we are coming from
			self.visit(self.level_array[this_one[0]][this_one[1]],(cell.i-this_one[0],cell.j-this_one[1]),current)
			#remove it when we get back to the method
			toVisit.remove(this_one)


	'''
	this is the method that builds the grid and initiates recursion
	'''
	def generate(self):
		#the first one is weird.
		start_cell = self.level_array[0][0]
		start_cell.visited = True
		#choose a direction to go, we need one to pass to the recursive method
		initial_choice = [0,0]
		initial_choice[random.randrange(2)] = 1

		#go!
		self.visit(self.level_array[initial_choice[0]][initial_choice[1]],(-initial_choice[0],-initial_choice[1]),0)

'''
this is the method that we will call to build the level.
it calls all of the methods in this module and builds the array that is readable by the game
it examines the grid and puts wires where the walls aren't
Add values to difficulty to make the levels more difficult.  This will increase the length of path needed to 
Consider it an end path.  Default is difficulty = 0, making path range 40 to 60 units long, 
for example if difficulty was 2, the range would be 42 to 62
'''
def generate_level(rows,columns,difficulty):
	#make the grid and traverse it with generate()
	generator = LevelGen(rows,columns)
	generator.generate()


	# Uncomment this to see how the maximum array works
	# print(generator.maximum)
	
	#the array that we will return
	out_array = []


	# Go throught the generated level_array and add to out_array the translated
	# pieces.  Essentially convert from level_array format (cell,cell,cell,...)
	# to out_array format (('end',1),('line',2),...)
	for row in generator.level_array:
		out_array.append([]) # add an empty array to be our row

		for cell in row:
			#count the walls to find out which tile it is
			walls = cell.count_walls()

			#assume we have a cross in orientation 0
			cell_type = 'cross'
			cell_orientation = 0
			# Reference: walls are stored [u,r,d,l]

			#if we have 3 walls, its an end piece.
			if walls == 3:
				cell_type = 'end'
				if not cell.walls[1]:
					cell_orientation = 1
				if not cell.walls[2]:
					cell_orientation = 2
				if not cell.walls[3]:
					cell_orientation = 3

			#if we have 2 walls, its either an elbow or a line.
			elif walls == 2:
				if not cell.walls[0] and not cell.walls[2]:
					cell_type = 'line'
				elif not cell.walls[1] and not cell.walls[3]:
					cell_type = 'line'
					cell_orientation = 1
				else:
					cell_type = 'elbow'
					if not cell.walls[0] and not cell.walls[1]:
						cell_orientation = 0
					elif not cell.walls[1] and not cell.walls[2]:
						cell_orientation = 1
					elif not cell.walls[2] and not cell.walls[3]:
						cell_orientation = 2
					else:
						cell_orientation = 3
			#only one wall? must be a tee
			elif walls == 1:
				cell_type = 'tee'
				if cell.walls[3]:
					cell_orientation = 0
				elif cell.walls[0]:
					cell_orientation = 1
				elif cell.walls[1]:
					cell_orientation = 2
				elif cell.walls[2]:
					cell_orientation = 3


			#randomize orientation
			#can be commented out to see presolved puzzle
			if cell_type != 'end':
				cell_orientation = random.randrange(4)
			#we now know what it is, so add it to the list we are building
			out_array[len(out_array)-1].append((cell_type,cell_orientation))
	
	# Simple linear search to find all end locations
	end_locs = []
	for i in range(len(out_array)):
		for j in range(len(out_array[0])):
			if out_array[i][j][0] == 'end':
				end_locs.append((i,j))
	
	
	# This is to find a path that is the right size for the player given his 50 moves
	# Look at every other element so it's the path length not the position
	for i in range(0,len(generator.maximum),2):
		# If the length of a certain path to an end is between 40 and 60, mark it so we can make it the only end
		if generator.maximum[i] > difficulty + 40 and generator.maximum[i] < difficulty + 60:
			# we found one! mark it
			# This can sometimes cause an error because there wasn't an end
			# generated in the given range of distances
			end_loc = generator.maximum[i+1]
			break
	
	# To get rid of this error, we try to accsess end_loc.
	# If an error happens, that means end_loc wasn't initialized
	# and we go to the exception.  If an error doesn't happen, we make
	# a poop varialbe and it can just chill
	try:
		poop = end_loc[0]
	except:
		# print a statement of the error and make a random end the end we want
		print("end_loc was nonexsistant so we made a new one")
		end_loc = end_locs[random.randrange( len( end_locs ) - 1 )]
	
	# make all end pieces that aren't the end piece we want into random pieces
	# Essentially get rid of all end pieces but 1
	for i in range(len(end_locs)):
		if end_locs[i] != end_loc:
			# set the thing at the position of the ends to a random thing grabbed from level_design.TILE_TYPES
			out_array[end_locs[i][0]][end_locs[i][1]] = (level_design.TILE_TYPES[random.randrange(len(level_design.TILE_TYPES)-2)+2], out_array[end_locs[i][0]][end_locs[i][1]][1])
		
	#fix the start because we can't rotate it while playing
	out_array[0][0] = ('start',1)
	if generator.level_array[0][0].walls[1]:
		out_array[0][0] = ('start',2)
	
	#return! woo
	return out_array



