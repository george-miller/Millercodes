import pygame
import random
import math
from classes import *
from stream_io import *


# ----------- NOTES ------------------
"""This game is actually really addicting and fun to play.  A little grapics doover, more clever incrementinfinite method, and mass expand levels will make this awesome and probably be easy to implement(especially since infinite increments could be the same as the levels).  With saves already implemented, lives becomes the easy pay element but I'm sure we can come up with more.  Also a side note, I think making 3 streams is a little stupid considering it would make it a pain to play and I think it'll harm more than it helps.  Two is a good balance between being casual and also making you feel like you can do better"""


# ---------- FEATURES -------------
# One paddle or two paddle play
# Mutable colorstreams, with varialbes such as real time changing width, height(which also serves as downward speed), frequency of color change, and moving x positions - All these changes are possible because of the ColorBlock class
# The game now saves at which level you are on, and saves highscore and lives (pay element)
# There is also a way through the options menu to reset highscore and levels and to buy more lives
# More in depth splash screen with instructions
# Infinite mode, where players can go for the high score

# ---------- BUGS ----------
# One known bug is that if you hold left or right when entering a new level or entering a level from the start screen, 
# the player's x_change will become messed up and the player will be glued to one side of the screen



#size of the game window
window_height = 500
window_width = 300

#state of the game,
#-1 is loss screen
#0 is title screen
#1 is game

state = 0


#start pygame, do normal stuff
pygame.init()
size = (window_width, window_height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Streams")
done = False
clock = pygame.time.Clock()

# load music and play it indefenitely if sound is on
pygame.mixer.music.load("arcade-music-loop.ogg")
if readFile(3) == 1:
	pygame.mixer.music.play(-1)

# initialize the click sound when the player clicks a key (all except q, a, w, and s)
click_sound = pygame.mixer.Sound("clicksound.ogg")

# Initialize player and colorstreams
player = Player(1)

# We must initiatlize the streams so that we can pass them into the levels method
stream1 = ColorStream(0,0,0,0,0,0)
stream2 = ColorStream(0,0,0,0,0,0)

# This will keep track of where the user is in a current level:
# 0 is uninitiated, 1 is active and running, 2 is completed and awaiting a keypress to continue
initiated = 0


# A method to house the code for an event checker for when the game is being played (not on a spash screen or gameover screen)
def activeevents(state,initiated,done):
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
				if readFile(3) == 1:
					click_sound.play()
				player.color_left = (player.color_left - 1)%len(color_list)
			elif event.key == pygame.K_a:
				if readFile(3) == 1:
					click_sound.play()
				player.color_left = (player.color_left + 1)%len(color_list)
			elif event.key == pygame.K_w:
				if readFile(3) == 1:
					click_sound.play()
				player.color_right =  (player.color_right + 1)%len(color_list)
			elif event.key == pygame.K_s:
				if readFile(3) == 1:
					click_sound.play()
				player.color_right = (player.color_right - 1)%len(color_list)
			# IF the user presses return while initiated = 2, that means he needs to move onto the next level
			elif event.key == pygame.K_RETURN:
				if readFile(3) == 1:
					click_sound.play()
				if initiated == 2:
					# move on to the next level
					# clear the sprite group
					initiated = 0
					state+=1
					colorblocks.empty()
				# If the user presses enter while he is on the out of lives screen, go back to the title screen
				elif readFile(1) < 1:
					state = 0
			# If the user wants to quit, he can press escape to go back to the title screen
			elif event.key == pygame.K_ESCAPE:
				if readFile(3) == 1:
					click_sound.play()
				if readFile(2) < player.score:
					updateFile(2,player.score)
				# If we just quit out of infinite mode, reset the score
				if state == -2:
					player.score = 0
				colorblocks.empty()
				player.__init__(player.mode)
				initiated = 0
				state = 0
					
		#more movement
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				player.change_x += 3
			elif event.key == pygame.K_RIGHT:
				player.change_x -= 3
				
	return (state,initiated,done)
	

# A function to make a level.  This method handles all everything to do with a level. To create a level, all you have to do is call this
#                      player mode for this level   various stream characteristics
def levels(initiated, state, stream1,stream2,player, mode,streams_x_midpoint, stream_dist_mid, stream_width,stream_height,
           stream_rand, stream_width_chance):
	
	if initiated == 0:
		if readFile(1) < 1:
			# If we are out of lives, don't let the player play
			screen.blit(splash_font.render("You're out of lives", False, WHITE), (10,100))
			screen.blit(instructions_font.render("Wait some time or buy more!", False, WHITE), (50,150))
		else:
			# reinitiate player, streams
			player.__init__(mode)
			updateFile(0,state)
			stream1 = ColorStream(streams_x_midpoint - stream_dist_mid, random.randrange(4), 
			                      stream_width, stream_height,stream_rand,stream_width_chance)
			if player.mode == 2:
				stream2 = ColorStream(streams_x_midpoint + stream_dist_mid, random.randrange(4), 
			                      stream_width, stream_height,stream_rand,stream_width_chance)
			initiated = 1
	
	elif initiated == 1:
		#update and draw
		stream1.update()
		if player.mode == 2:
			stream2.update()
		colorblocks.update(player)
		player.update()
		
		# Check if the player went across the win or loss thresholds
		if player.rect.y > 460:
			updateFile(1,readFile(1)-1)
			state = -1
			initiated = 0
		elif player.rect.y < 150:
			initiated = 2
		
		screen.blit(instructions_font.render("Score: %.1f" % player.score, False, WHITE), (40,470))
		player.draw(screen)
		colorblocks.draw(screen)
		
	elif initiated == 2:
		# draw text for win screen
		screen.blit(splash_font.render("You win this round!", False, WHITE), (20,100))
		screen.blit(instructions_font.render("Press Enter to continue", False, WHITE), (80,200))
		
	# return initiated and state to caller
	return (initiated,state,stream1,stream2)






#game font
splash_font = pygame.font.SysFont('Courier',25,True,False)
instructions_font = pygame.font.SysFont('Courier', 12, False, False)

#list of words on start screen
start_screen_options = ("Start", "Infinite Start","Instructions", "Options","Quit")
options = ("Reset Levels", "Reset Highscore" , "Buy lives", "Sound Toggle","Go back")

#currently selected word on start screen
selected_option = 0
title_state = 0
instructions = ("Welcome to stream!","", "The goal of this game is to match your", "paddle with the falling color streams.", 
                "You will gain points if your color is", " matched with the stream color, and you", 
                "will lose points if you are collecting the", "wrong color.  When you are collecting the", 
                "right color, your paddle moves up the",  "screen and when you are collecting the", "wrong color your paddle moves down the",
                "screen.  Get to the top of the screen to", "complete the level!","",  "GL & HF,", "Millercodes Team.")
controls = ("CONTROLS:", "Use the arrow keys to move your paddle", "'q' and 'a' cycle through your left color", "'w' and 's' cycle through your right color", "Press esc while in a level to go to the", "title screen."," ", "OTHER", "Your game will save as you go through the", "levels. It will not save in infinite mode.", "You start with 5 lives and you will gain", "more over time. You only lose lives in the", "levels, not in infinite mode.")

# possible story briefing - currently unused
#brief = ("A mysterious spaceship has entered the atmosphere and is dropping paint at an alarming rate! Climb the line of paint to reach the spaceship and uncover the truth behind this mysterious craft")

# This is a list of values that will be incremented in infinite mode to make the game harder and harder as you go
# These values are used to initiatlize the colorstreams
#          xPos   color              width,height(and speed),random chance, a counter, and a widthchange
infinite = [110, random.randrange(4), 20,     2,              100,              0,            0]

# and a method to increase the values of infinite
def increment_infinite():
	# increment conter, keeping track of how many time we have incremented the array
	infinite[5]+= 1
	# make another random color the start color
	infinite[1] = random.randrange(4)
	
	infinite[2] += 5
	# we don't want the width of the stream to become bigger than the width of the player
	# I made it max out to paddle_width - 15 because it's annoying to play with a stream too wide
	if infinite[2] >= player.paddle_width-15:
		infinite[2] = player.paddle_width-15
	
	# increase the height and speed every so often
	if infinite[5] % 4 == 0:
		infinite[3] += 1
	# increase the chance to change color
	infinite[4] -= 5
	if infinite[4] < 40:
		infinite[4] = 40
		
	# if we are past level 4, start changing the width of the streams
	# as we progress more, change the width faster and faster
	if infinite[5] > 4:
		infinite[6] += .1
		# but don't let it get too high
		if infinite[6] > 1.5:
			infinite[6] = 1.5

# -------------------- ENGINE --------------------
while not done:
	#start with black screen, each state has custom drawing code
	screen.fill(BLACK)
	
	# infiinite mode
	if state == -2:
		(state,initiated,done) = activeevents(state,initiated,done)
		if initiated == 0 and state == -2:
			# Initiate player and streams
			player.__init__(2)
			stream1 = ColorStream(infinite[0], infinite[1],infinite[2], infinite[3], infinite[4], infinite[6])
			stream2 = ColorStream(infinite[0] + 80, infinite[1], infinite[2], infinite[3], infinite[4], infinite[6])
			initiated = 1
		elif initiated == 1:
			# Update and draw everything
			stream1.update()
			stream2.update()
			colorblocks.update(player)
			player.update()
			# Check if the player went across the win or loss thresholds
			if player.rect.y > 460:
				# We don't lose lives in infinite mode
				state = -1
				initiated = 0
			elif player.rect.y < 150:
				initiated = 2			
			
			screen.blit(instructions_font.render("Score: %.1f" % player.score, False, WHITE), (40,470))
			player.draw(screen)
			colorblocks.draw(screen)
		elif initiated == 2:
			# When moving on to the next part, reinitiate everything
			# incremenet infinite and then reinitialize streams with new values
			increment_infinite()
			colorblocks.empty()
			player.__init__(player.mode)
			stream1 = ColorStream(infinite[0], infinite[1], infinite[2], infinite[3],infinite[4], infinite[6])
			stream2 = ColorStream(infinite[0] + 80, infinite[1], infinite[2], infinite[3],infinite[4], infinite[6])
			initiated = 1
		
	
	
	#state of loss
	elif state == -1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			if event.type == pygame.KEYDOWN:
				if readFile(3) == 1:
					click_sound.play()
				if event.key == pygame.K_RETURN:
					#reset the game
					# If there's a new highscore, record it
					if readFile(2) < player.score:
						updateFile(2, player.score)
					initiated = 0
					colorblocks.empty()
					player.__init__(player.mode)
					state = 0
		#draw text for loss screen
		screen.blit(splash_font.render("{:^20}".format("Game Over"),True,RED),(0,200))
		screen.blit(splash_font.render("{:^20}".format("Score:{:>5d}".format(int(math.floor(player.score)))),False,WHITE),(0,250))
		screen.blit(splash_font.render("{:^20}".format("press enter"),False,WHITE),(0,300))	
	
	#title screen
	elif state == 0:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			#handle switching options
			elif event.type == pygame.KEYDOWN:
				if readFile(3) == 1:
					click_sound.play()
				if event.key == pygame.K_DOWN:
					selected_option = (selected_option+1)%len(start_screen_options)
				elif event.key == pygame.K_UP:
					selected_option = (selected_option-1)%len(start_screen_options)
				elif event.key == pygame.K_RETURN:
					# choose!
					# These two lines are for navigating the instruction screen
					if title_state == 1:
						title_state = 2
					elif title_state == 2:
						title_state = 0
						
					# While we are on the options menu and press return	
					elif title_state == 3:
						# reset lives
						if selected_option == 0:
							updateFile(0,1)
						# reset highscore
						elif selected_option == 1:
							updateFile(2,0)
						# buy lives
						elif selected_option == 2:
							updateFile(1,readFile(1)+5)
						# Toggle music
						elif selected_option == 3:
							if readFile(3) == 1:
								pygame.mixer.music.stop()
								updateFile(3,0)
							else:
								pygame.mixer.music.play()
								updateFile(3,1)
						# go back 
						elif selected_option == 4:
							title_state = 0
					
					elif selected_option == 0:
						#if start is selected, transition to state 1
						state = readFile(0)
					elif selected_option == 1:
						# go into infinite
						state = -2
					elif selected_option == 2:
						# Go to instructions
						title_state = 1
					elif selected_option == 3:
						# go to options
						title_state = 3
					else:
						#quit
						done=True
		
		
		# in each of these loops used to draw words, the selected option is highlighted through the use of the 
		# if statement: if i == selected_option make the color blue
		i = 0
		if title_state == 0:
			# show current state of the save file
			screen.blit(instructions_font.render("Current level: " + str(readFile(0)), False, WHITE), (100,400))
			screen.blit(instructions_font.render("Current lives: " + str(readFile(1)), False, WHITE), (100,420))
			screen.blit(instructions_font.render("Current highscore: " + str(readFile(2)), False, WHITE), (100,440))
			#draw the words
			for opt in start_screen_options:
				color = WHITE
				if i == selected_option:
					color = BLUE
				screen.blit(splash_font.render("{:^20}".format(opt),False,color),(0, 100+50*i))
				i += 1
		elif title_state == 1:
			# draw words
			for line in instructions:
				if i > 13:
					screen.blit(instructions_font.render("{:>40}".format(line), False, WHITE), (0,50+20*i))
				else:
					screen.blit(instructions_font.render("{:<40}".format(line), False, WHITE), (0,50+20*i))
				i+= 1
			
		elif title_state == 2:
			# draw words
			for line in controls:
				if i > 13:
					screen.blit(instructions_font.render("{:>40}".format(line), False, WHITE), (0,50+20*i))
				else:
					screen.blit(instructions_font.render("{:<40}".format(line), False, WHITE), (0,50+20*i))
				i+= 1			
		
		elif title_state == 3:
			#draw words
			for opt in options:
				color = WHITE
				if i == selected_option:
					color = BLUE
				screen.blit(splash_font.render("{:^20}".format(opt),False,color),(0, 100+50*i))
				i += 1			
			


	else:
		# If we are not on the title screen, we are playing and need events handled
		(state,initiated,done) = activeevents(state,initiated,done)
		
	# level 1, start off easy with one paddle and one stream
	if state == 1:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,1,150,40,20,2,100,0)
			
		
	# level 2, now you have 2 streams and 2 paddles	
	elif state == 2:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,2,150,40,20,2,100,0)
		
	# level 3, now streams are wider (from 20 to 30)
	elif state == 3:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,2,150,40,30,2,100,0)		
		
	# level 4, now streams change color faster (from 100 to 80)		
	elif state == 4:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,2,150,40,30,2,80,0)		
		
	# level 5, now streams change width
	elif state == 5:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,2,150,40,30,2,80,.5)		
		
	# Level 6, now streams start a little wider
	elif state == 6:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,2,150,40,40,2,80,.5)		
			
	# Level 7, now streams change width faster
	elif state == 7:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,2,150,40,40,2,80,.8)		
			
		
	# Level 8, now streams change color faster
	elif state == 8:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,2,150,40,40,2,60,.8)		
		
			
	# Level 9, now streams change width faster
	elif state == 9:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,2,150,40,40,2,60,1)		
			
		
			
	# Level 10, now streams go down faster
	elif state == 10:
		(initiated,state,stream1,stream2) = levels(initiated,state,stream1,stream2,player,2,150,40,40,3,60,1)		
		
	# Out of levels -_- common man 
	elif state == 11:
		activeevents()
		# update the file saying we got here and update highscore if need be
		if readFile(2) < player.score:
			updateFile(0,11)
			updateFile(2,player.score)
		else:
			updateFile(0,11)
		# Write some text
		screen.blit(splash_font.render("You win!", False, WHITE), (100,100))
		screen.blit(instructions_font.render("There are no more levels", False, WHITE), (80,200))
		screen.blit(instructions_font.render("Try infinite mode!", False, WHITE), (90,300))
		

	pygame.display.flip()

	clock.tick(60)

pygame.quit()
