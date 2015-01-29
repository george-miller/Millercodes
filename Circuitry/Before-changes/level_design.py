import pygame
from level_gen import *

'''
Levels are stored as 2d arrays of tuples of the form (type, orientation)
Level 0 is a randomly generated one.
'''
TILE_TYPES = ['start', 'end', 'line', 'elbow', 'tee' ,'cross']
def regenerate():
	LEVEL_DESIGN[0]['pieces'] = generate_level(10,10,3)

LEVEL_DESIGN = [
#Random Level
{

	'num'	: 1,
	'moves' : 50, 
	'multiplier': 1,
	'width' : 10, #Number of tiles wide
	'height': 10, #Number of tiles tall
	'pieces': generate_level(10,10,3)
},

#LEVEL 1
{	
	'num'	: 1,
	'moves' : 50, 
	'multiplier': 1,
	'width' : 10, #Number of tiles wide
	'height': 10, #Number of tiles tall
	'pieces': [ #Pieces is a double indexed list of tuples (TYPE,ORIENTATION)
			[('start',1),('line',1),('line',2),('line',0),('line',0),('line',0),('line',0),('line',0),('line',0),('elbow',0)],
			[('line',0),('line',0),('line',0),('elbow',0),('line',0),('line',0),('line',1),('line',0),('line',0),('line',0)],
			[('elbow',0),('elbow',0),('line',0),('line',0),('line',2),('line',0),('elbow',0),('line',3),('line',0),('line',0)],
			[('elbow',0),('line',1),('tee',0),('line',0),('elbow',0),('line',0),('line',0),('line',0),('line',0),('line',0)],
			[('line',0),('line',0),('elbow',0),('line',0),('line',0),('elbow',0),('line',0),('line',0),('line',0),('line',0)],
			[('elbow',0),('line',0),('tee',0),('cross',0),('line',0),('line',0),('line',0),('line',0),('elbow',0),('line',0)],
			[('line',0),('line',1),('elbow',0),('line',2),('line',0),('line',0),('elbow',0),('line',0),('line',0),('line',0)],
			[('line',0),('elbow',0),('line',0),('line',0),('line',0),('line',0),('line',0),('elbow',0),('line',0),('line',0)],
			[('line',0),('line',0),('line',0),('elbow',0),('line',0),('line',0),('line',0),('line',0),('elbow',0),('elbow',0)],
			[('elbow',0),('line',0),('line',0),('line',0),('line',0),('line',0),('line',0),('line',0),('elbow',0),('end',3)],
		]
},				  

#LEVEL test
{
	'num' : 2,
	'moves' : 50,
	'multiplier' : 1,
	'width' : 3,
	'height': 3,
	'pieces' : [[('start',1),('line',0),('elbow',3)],
				[('tee',2),('cross',1),('elbow',2)],
				[('line',1),('tee',2),('end',3)]]
}
]
