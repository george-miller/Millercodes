import pygame
from colors import *

#Main function for drawing board
def fullboard(screen, score, level):
	#Draw headers and save text height
	textheight = headers(screen,score, level)
	#Draw board
	board(screen, level, textheight)
	
	return textheight
	
def headers(screen, score, level):
	# Select the font to use, size, bold, italics
	font = pygame.font.SysFont('Calibri', 20, True, False)
	left = 10
	
	text = font.render("Score: " + str(score), True, BLACK) # Render the text. "True" means anti-aliased text.
	screen.blit(text, [left, 5]) # Put the image of the text on the screen at 250x250
	left += text.get_width() + 10
	
	text = font.render("Lvl: " + str(level.num), True, BLACK) # Render the text. "True" means anti-aliased text.
	screen.blit(text, [left, 5]) # Put the image of the text on the screen at 250x250
	left += text.get_width() + 10
	
	text = font.render("Moves: " + str(level.moves), True, BLACK) # Render the text. "True" means anti-aliased text.
	screen.blit(text, [left, 5]) # Put the image of the text on the screen at 250x250

	text = font.render("Buy Moves", True, BLACK)
	screen.blit(text, [screen.get_width() * (12/16) - text.get_width()/2, 5])
	pygame.draw.rect(screen, BLACK, [screen.get_width()*5/8 + 10, 0, screen.get_width()/5, text.get_height() + 10], 4)
	
	text = font.render("Quit", True, BLACK)
	screen.blit(text, [screen.get_width()*15/16-text.get_width()/2,5])
	pygame.draw.rect(screen, BLACK, [screen.get_width()*7/8, 0, screen.get_width()/8, text.get_height() + 10], 4)

	
	return text.get_height() + 10
	
def board(screen, level, textheight):
	width = screen.get_width() #Get available width of the screen
	height = screen.get_height()-textheight #Get available height of the screen
	
	#Find the smallest square dimension for the tile in order to fit level on screen
	if width/level.tile_width > height/level.tile_height:
		size = height/level.tile_height
	else:
		size = width/level.tile_width
	
	board = pygame.Surface((size * level.tile_width, size * level.tile_height)) #Create sized board for level
	level.draw(board, size) #Draw level
	
	screen.blit(board, [0, textheight]) #Stamp board on screen
	
	
