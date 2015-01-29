import pygame
from level_gen import *

'''
Levels are stored as 2d arrays of tuples of the form (type, orientation)
Level 0 is a randomly generated one.
'''

TILE_TYPES = ['start', 'end', 'line', 'elbow', 'tee' ,'cross']


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

#  -------------- STORY MODE LEVELS -------
# There is only 8 levels right now, clicking on any of the levels in level select
# greater than 8 causes an error.  I have made more levels, going from width height
# (3,3) incrementing both by one until we get to (10,10)



#LEVEL 1

{
    'num' : 1,
    'moves' : 50,
    'multiplier' : 1,
    'width' : 3,
    'height': 3,
    'pieces' : [[('start',1),('elbow',0),('tee',3)],
                [('elbow',2),('elbow',1),('line',2)],
                [('elbow',1),('line',2),('end',3)]]
},

# LEVEL 2
{
    'num' : 2,
    'moves' : 50,
    'multiplier' : 1,
    'width' : 4,
    'height': 4,
    'pieces' : [[('start',1),('tee',0),('elbow',3),('elbow',2)],
                [('line',2),('line',1),('line',2),('cross',0)],
                [('elbow',1),('line',3),('elbow',2),('elbow',1)],
                [('elbow',1),('line',2),('line',1),('end',3)]]    
},

# LEVEL 3
{
    'num' : 3,
    'moves' : 50,
    'multiplier' : 1,
    'width' : 5,
    'height': 5,
    'pieces' : [[('start',1),('line',0),('cross',3),('elbow',0),('elbow',0)],
                [('tee',2),('line',1),('line',2),('elbow',1),('elbow',3)],
                [('line',1),('elbow',2),('line',3),('elbow',3),('cross',0)],
                [('line',1),('elbow',3),('line',0),('line',1),('line',0)],
                [('elbow',1),('tee',3),('line',1),('tee',2),('end',3)]]    
},
# LEVEL 4
{
    'num' : 4,
    'moves' : 50,
    'multiplier' : 1,
    'width' : 6,
    'height': 6,
    'pieces' : [[('start',1),('elbow',0),('line',2),('line',1),('elbow',0),('tee',2)],
                [('elbow',2),('elbow',1),('elbow',2),('cross',1),('line',3),('line',2)],
                [('tee',1),('line',2),('line',3),('line',1),('elbow',0),('line',2)],
                [('line',1),('cross',3),('line',0),('line',1),('line',0),('elbow',3)],
                [('line',2),('elbow',2),('elbow',1),('elbow',0),('line',1),('line',0)],
                [('line',1),('elbow',3),('elbow',1),('line',2),('elbow',2),('end',3)]]       
},
# LEVEL 5
{
    'num' : 5,
    'moves' : 50,
    'multiplier' : 1,
    'width' : 7,
    'height': 7,
    
    'pieces' : [[('start',1),('tee',0),('line',2),('elbow',1),('line',0),('line',2),('cross',0)],
                [('tee',2),('elbow',1),('line',2),('line',1),('elbow',3),('line',2),('line',3)],
                [('line',1),('elbow',2),('line',3),('elbow',1),('elbow',0),('elbow',2),('cross',0)],
                [('line',1),('elbow',3),('line',0),('line',1),('line',0),('line',3),('elbow',0)],
                [('elbow',2),('elbow',2),('line',1),('elbow',0),('tee',1),('elbow',0),('elbow',2)],
                [('cross',0),('elbow',0),('elbow',2),('elbow',0),('tee',1),('line',0),('line',1)],
                [('line',1),('line',3),('line',1),('line',2),('cross',2),('elbow',1),('end',3)]]     
},

# LEVEL 6
{
    'num' : 6,
    'moves' : 50,
    'multiplier' : 1,
    'width' : 8,
    'height': 8,
    
    'pieces' : [[('start',1),('tee',0),('elbow',2),('line',1),('line',0),('line',2),('line',0),('cross',0)],
                [('line',1),('line',1),('line',2),('line',1),('line',2),('line',2),('elbow',3),('line',1)],
                [('elbow',1),('line',2),('line',3),('elbow',1),('elbow',0),('tee',2),('line',0),('line',1)],
                [('line',1),('line',3),('line',0),('elbow',1),('line',0),('line',3),('elbow',0),('tee',1)],
                [('line',2),('elbow',2),('line',1),('tee',0),('elbow',1),('line',0),('elbow',2),('line',1)],
                [('line',0),('elbow',0),('line',1),('line',0),('line',1),('line',0),('line',1),('line',0)],
                [('cross',0),('line',0),('elbow',3),('line',0),('line',0),('line',0),('line',0),('elbow',2)],
                [('line',1),('line',3),('line',1),('line',2),('cross',2),('elbow',1),('line',1),('end',3)]]     
},

# LEVEL 7
{
    'num' : 7,
    'moves' : 50,
    'multiplier' : 1,
    'width' : 9,
    'height': 9,
    
    'pieces' : [[('start',1),('tee',0),('line',2),('line',1),('tee',0),('line',2),('line',0),('elbow',0),('elbow',3)],
                [('line',1),('elbow',1),('line',2),('line',1),('line',2),('line',2),('line',3),('line',1),('cross',0)],
                [('line',1),('elbow',2),('line',3),('elbow',1),('line',0),('elbow',2),('line',0),('line',1),('elbow',2)],
                [('tee',1),('elbow',3),('elbow',0),('line',1),('line',0),('tee',3),('line',1),('elbow',0),('elbow',0)],
                [('line',2),('elbow',2),('tee',1),('line',1),('line',1),('line',0),('line',1),('line',1),('line',0)],
                [('line',0),('line',1),('line',1),('line',0),('cross',1),('elbow',0),('line',1),('elbow',0),('line',1)],
                [('cross',0),('line',0),('line',1),('elbow',0),('line',0),('line',0),('cross',0),('line',1),('line',0)],
                [('elbow',1),('line',1),('line',1),('line',0),('line',1),('line',1),('elbow',2),('line',0),('line',1)],
                [('line',1),('line',3),('tee',1),('line',2),('line',1),('line',1),('tee',1),('line',0),('end',3)]]     
},

# LEVEL 8
{
    'num': 8,
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
}
]
