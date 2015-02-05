#>>>>>>>>>Define Colors (Should be Library Soon)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (15, 126, 45)
GRAY01 = [20, 20, 20]
GRAY02 = [40, 40, 40]
GRAY03 = [60, 60, 60]
GRAY04 = [80, 80, 80]
GRAY05 = [100, 100, 100]
GRAY06 = [120, 120, 120]
GRAY07 = [140, 140, 140]
GRAY08 = [160, 160, 160]
GRAY09 = [180, 180, 180]
GRAY10 = [200, 200, 200]
GRAY11 = [220, 220, 220]
GRAY12 = [240, 240, 240]

#Define types of bricks
BRICKS = {
	'pink': {'image':"pinkbrick.png",'score':50,'lives':2},
	'blue': {'image':"bluebrick.png", 'score':50, 'lives':1}
}

#Define the list of bricks to create for each level
LEVELS = {1:
	[('pink', BLACK, (i,j)) for i in range(14) for j in range(2)]
	+
	[('blue', BLACK, (i,j)) for i in range(14) for j in range(2,8,1)]
}
