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
this means there will be no loops in this traversal, like a classic maze I guess.
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
basically the algorithm is a depth-first traversal
at each cell, it chooses a random unvisited direction to travel
when it reaches a dead end, it returns to the last cell at which it had a choice of where to go and resumes.
'''
class LevelGen():
	def __init__(self, rows, columns):
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
	args: cell = current cell, d is a tuple (dRow, dCol) of where we came from
	'''
	def visit(self, cell, d):
		#if we have been here, do nothing.
		if cell.visited == True:
			return
		#otherwise, mark it.
		cell.visited = True
		
		#these two lines break down the walls.
		#d is a tuple that stores (dRow, dCol)
		#wall of current cell facing the direction we came from
		cell.walls[ 1 + d[0] - d[1] + (d[1]%2) ] = False
		#wall of old cell facing the direction we went
		self.level_array[ cell.i + d[0] ][ cell.j + d[1] ].walls[ 1 - d[0] + d[1] + (d[1]%2) ] = False

		#add all valid adjacent cells to toVisit. Check if they are visited later.
		toVisit = []
		if cell.i > 0:
			toVisit.append((cell.i-1,cell.j))
		if cell.i < self.rows-1:
			toVisit.append((cell.i+1,cell.j))
		if cell.j > 0:
			toVisit.append((cell.i,cell.j-1))
		if cell.j < self.columns-1:
			toVisit.append((cell.i,cell.j+1))

		#we loop through the list randomly, removing as we go.
		#we return to this loop every time visit returns.
		while len(toVisit) > 0:
			#choose one
			this_one = toVisit[random.randrange(len(toVisit))]
			#visit it, passing the new cell and the direction we are coming from
			self.visit(self.level_array[this_one[0]][this_one[1]],(cell.i-this_one[0],cell.j-this_one[1]))
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
		self.visit(self.level_array[initial_choice[0]][initial_choice[1]],(-initial_choice[0],-initial_choice[1]))

'''
this is the method that we will call to build the level.
it calls all of the methods in this module and builds the array that is readable by the game
it examines the grid and puts wires where the walls aren't
'''
def generate_level(rows,columns,difficulty):
	#make the grid and traverse it
	start_walls = 4
	while start_walls != 3:
		generator = LevelGen(rows,columns)
		generator.generate()
		start_walls = generator.level_array[0][0].count_walls()
	ends = 0
	while ends < difficulty:

		#the array that we will return
		out_array = []

		for row in generator.level_array:
			out_array.append([])

			for cell in row:
				#count the walls to find out which tile it is easier
				walls = cell.count_walls()
				#assume we have a cross in orientation 0
				cell_type = 'cross'
				cell_orientation = 0
				#walls are stored [u,r,d,l]

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
		end_locs = []
		for i in range(len(out_array)):
			for j in range(len(out_array[0])):
				if out_array[i][j][0] == 'end':
					end_locs.append((i,j))
		ends = len(end_locs)

	#set number of end pieces based on difficulty
	while len(end_locs) > difficulty:
		i = random.randrange(len(end_locs))
		out_array[end_locs[i][0]][end_locs[i][1]] = (level_design.TILE_TYPES[random.randrange(len(level_design.TILE_TYPES)-2)+2], out_array[end_locs[i][0]][end_locs[i][1]][1])
		end_locs.remove(end_locs[i])
		
	#fix the start because we can't rotate it while playing
	out_array[0][0] = ('start',1)
	if generator.level_array[0][0].walls[1]:
		out_array[0][0] = ('start',2)
	#put the end in because we might have turned a corner at the bottom right of the board during our algorithm
	'''
	sometimes this generates unsolvable puzzles
	if generator.level_array[9][9].walls[0]:
		out_array[9][9] = ('end',3)
	else:
		out_array[9][9] = ('end',0)
	'''
	#return! woo
	return out_array
