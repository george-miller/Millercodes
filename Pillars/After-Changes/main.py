"""
This is the blank game template for our PyGame Prototypes.


Code contained herein is copyright 2015, MillerCodes LLC.
All rights reserved. Violators will be prosecuted.

We trust you know the general rules:
1) Think Before You Type
2) With Great Power Comes Great Responsibility

"""

"""
NEW FEATURES!
- if you win or lose, you can restart
- better (sorta) collisions and bounces
- the ball now uses angles intead of x and y speed

WEIRD BUGS!
- start game, press left twice and watch 
- sometimes multiballs spawn in top left I have no idea why
"""


#>>>>>>>>>Import Modules

#Here we import the PyGame module, and a few other things we will likely need.
import pygame
import math
import random

from global_vars import *
from pieces import *

#>>>>>>>>>>>Gloabl Parameters for This Game

#The stuff here is a placeholder for a future version.

#Now fetch the Background Image>>>
#background_image = pygame.image.load("HST_pillars_1136x640.png")
#And fetch the sounds library>>

#>>>>>>>>>>>Now we can start the game, appearing below.

def main():
	#We initialize the engine
	pygame.init()
	
	#defaults for an iPhone 5S are 640 x 1136
	screen_size = (700, 700)
	
	TITLE = "Pillars, A Creation of MillerCodes LLC"
	BACKGROUND = BLACK

	#Then we launch the window
	screen = pygame.display.set_mode(screen_size)
	pygame.display.set_caption(TITLE)
	
	#And now we intitiate the main loop that will run the game.
	done = False
	clock = pygame.time.Clock()
	
	#-----Create the Blocks--------#
	
	#This is the master sprite list
	all_sprites_list = pygame.sprite.Group()
	#This is the list of Bricks
	brick_list = pygame.sprite.Group()
	
	#Level defines all the brick orientation and color information
	level = Level(all_sprites_list, brick_list, LEVELS)
	level.load(1) #Load level one
	
	#-------Create the Paddle-------#
	my_paddle = Paddle(screen, RED, (100, 20), (330, 600))
	
	#Create a list of paddles
	paddle_list = pygame.sprite.Group()
	paddle_list.add(my_paddle)
	
	all_sprites_list.add(my_paddle)
	
	#------Create the Ball---------#
	ball = Gameball(screen, WHITE, 8, 5,math.pi/2, my_paddle)
	
	#Create a list of balls
	ball_list = pygame.sprite.Group()
	ball_list.add(ball)
	all_sprites_list.add(ball)

	#Define the text used when the player loses
	font = pygame.font.SysFont('Calibri', 36, False, False)
	win = font.render("YOU WIN!!", True, RED)
	game_over = font.render("GAME OVER", True, RED)
	restart_text = font.render("Restart?", True, RED)

	#Create a group for all powerups
	power_list = pygame.sprite.Group()

	#------Set the Initial Game Data---------#
	
	score = 0
	
	lives = 3
	
	#------------------Main Program Loop---------------#
	
	while not done:
		#-----------BEGIN EVENT PROCESSING--------------#
		for event in pygame.event.get(): #user did something
			if event.type == pygame.QUIT: #If user clicked close, then:
				done = True		#Close and get out.
				
		#What to do if user pressed a key
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					for ball in ball_list:
						ball.launch() #This event begins the balls motion
					
				if event.key == pygame.K_LEFT:
					if ball_list.sprites()[0].launched:
						my_paddle.x_speed -= 9
					else:
						ball_list.sprites()[0].angle += .05	
				if event.key == pygame.K_RIGHT:
					if ball_list.sprites()[0].launched:
						my_paddle.x_speed += 9
					else:
						ball_list.sprites()[0].angle -= .05
				if event.key == pygame.K_UP:
					my_paddle.y_speed -= 9
				if event.key == pygame.K_DOWN:
					my_paddle.y_speed += 9

			#What to do if user lets go a key
			#subtracting the velocity added when pressing down the key
			#instead of setting it to 0 solves the problem that occurs
			#when both left and right are simultaneously pressed
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					if ball_list.sprites()[0].launched:	
						my_paddle.x_speed += 9
				if event.key == pygame.K_RIGHT:
					if ball_list.sprites()[0].launched:
						my_paddle.x_speed -= 9
				if event.key == pygame.K_UP:
					my_paddle.y_speed += 9
				if event.key == pygame.K_DOWN:
					my_paddle.y_speed -= 9
			

			elif event.type == pygame.MOUSEBUTTONDOWN:
				pos = pygame.mouse.get_pos()
				#When the game is over and the user clicks the restart button
				if pos[0] >= 300 and pos[0] <= 300 + restart_text.get_width():
					if pos[1] >= 400 and pos[1] <= 400 + restart_text.get_height():
						level.load(1) #Reload level 1
						lives = 3 #Reset lives
						my_paddle.__init__(screen, RED, (100, 20), (330, 600))


		#-----------END EVENT PROCESSING----------------#		
		screen.fill(BACKGROUND)	
		#-----------BEGIN GAME LOGIC--------------------#
		
		if lives > 0 and len(brick_list) != 0:
			my_paddle.slide() #Move the paddle
			

			if len(ball_list) == 0: #If there are no balls left
				lives -= 1
				my_paddle.__init__(screen, RED, (100, 20), (330, 600))
				player_ball = Gameball(screen, WHITE, 8, 5, math.pi/2, my_paddle) #Create a new ball
				ball_list.add(player_ball)
				all_sprites_list.add(player_ball)

			for player_ball in ball_list: #Check each ball in the game
				player_ball.bounce() #Move the ball
 				
				if not player_ball.launched:
					player_ball.holdpaddle(screen, my_paddle) #Have the ball follow the paddle

				#Using the bit masks created for each sprite, find the touching balls and bricks
				brick_hit_list = pygame.sprite.spritecollide(player_ball, brick_list, False, pygame.sprite.collide_mask)
	
				#Use the same method for the paddles
				paddle_hit_list = pygame.sprite.spritecollide(player_ball, paddle_list, False, pygame.sprite.collide_mask)
				
				if paddle_hit_list != []:
					#Calculate the balls new trajectory
					player_ball.hit(paddle_hit_list[0], 'paddle')
				
				for brick in brick_hit_list:
					player_ball.hit(brick)
					#Calculate the effect of the ball on the brick
					score = brick.hit(score, power_list, all_sprites_list)
				

				
					

			#Find all powerups touching the paddle
			power_hit_list = pygame.sprite.spritecollide(my_paddle, power_list, False, pygame.sprite.collide_mask)
			for power in power_hit_list:
				#Activate the corresponding power
				###### Need to find a better way to handle the sprite lists in these situations
				power.activate(screen, my_paddle, ball_list, all_sprites_list)

			for power in power_list:
				power.move() #Move the powers
		
		else: 
			if len(brick_list) == 0:
				screen.blit(win, [300,300])
				screen.blit(restart_text, [300,400])
			else:			
				screen.blit(game_over, [300, 300])
				screen.blit(restart_text, [300, 400])
	

		#-----------END GAME LOGIC----------------------#	


		#----------------BEGIN DRAWING CODE--------------#
		
		font = pygame.font.SysFont('Calibri', 36, False, False)

		score_text = font.render("Score:" + str(score), True, YELLOW)

		lives_text = font.render("Lives:" + str(lives), True, YELLOW)
		
		#>First, wipe the screen to black>>>
		

		#>Implement Your Drawings>>>

		#Draw the Background
		#screen.blit(background_image, [0, 0])

		#Draw the Box
		#draw_shadowbox(screen, box_x_loc, box_y_loc)

		#Draw the ball

		#player_ball.draw(screen)

		all_sprites_list.draw(screen)
		screen.blit(score_text, [100, 720])

		screen.blit(lives_text, [400, 720])

		#>Update the screen with the most recent frame>>>
		pygame.display.flip()

		#----------------END DRAWING CODE----------------#

		#>Limit the framerate (in fps)>>>
		clock.tick(60)
		
	#CREATE RESTART CODE
		
		
	#Close the window to quit the game
	pygame.quit()

if __name__ == "__main__":
	main()

