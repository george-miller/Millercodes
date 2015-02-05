import pygame
import math
import random 

from global_vars import *


#>>>>>>>>>>>Class Definitions for This Game

#Level holds the brick information for each level
class Level():
    def __init__(self, all_sprites_list, brick_list, levels):
        self.all_sprites_list = all_sprites_list
        self.brick_list = brick_list
        self.levels = levels

    #This will add the level to the sprite lists
    def load(self, level):
        self.all_sprites_list.remove(self.brick_list)
        self.brick_list.empty()

        for args in self.levels[level]:
            #Add each to the lists
            brick = Brick(*args)
            self.brick_list.add(brick)
            self.all_sprites_list.add(brick)


class Gameball(pygame.sprite.Sprite):
    """
    This is a class that defines the Game Ball. It is a sprite.
    """
    left_bound = 0
    right_bound = 0
    top_bound = 0
    bottom_bound = 0
   
    last_pos = (0,0) #Will be used to improve accuracy on hit events
    
    launched = False #If the ball has been launched
    
    def __init__(self, screen, color, size, speed, angle, paddle):
        #We will pass in the color and size of the ball.
        
        #First we call the parent constructor
        super().__init__()

	# This will be the angle measure of the current trajectory measured
	# in radians.  By using this and keeping speed constant, the balls
	# will move more realistically and eliminate the problem where all
	# the balls are at the same y position all the time.  The angle
	# is measured from the positive x axis counterclockwise
        self.angle = angle
        self.speed = speed
        #Then we generate the surface and pull it's location.
        self.image = pygame.Surface([size, size])
        self.image.fill(BLACK)
        
        pygame.draw.circle(self.image, color, (int(size/2),int(size/2)), int(size/2))
        #Create a bit mask from the color added to the surface
        self.mask = pygame.mask.from_threshold(self.image, color, color)

        self.size = size #Save size for later
        self.color = color #Save color for later

        #print(self.mask.count())
        #These location attributes come from the parent.
        self.rect = self.image.get_rect()

        self.rect.center = (paddle.rect.center[0], paddle.rect.center[1] - paddle.rect.height/2 - 10)#Place the ball at its initial position
        
        #Set the edges of the screen
        self.right_bound = screen.get_width() 
        self.bottom_bound = screen.get_height()
	

       
    def launch(self):
        self.launched = True
    
    def holdpaddle(self, screen, paddle):
        #Move the ball directly above the paddle
        self.rect.center = (paddle.rect.center[0], paddle.rect.center[1] - paddle.rect.height/2 - 10)
	# Draw a line to indicate where the current angle is.  We do this 
	# by starting the line at the ball's current position and ending
	# the line at the balls center plus a constant times the cos/sin of the angle
        pygame.draw.line(screen, WHITE, (self.rect.center[0],self.rect.center[1]), (self.rect.center[0] + (math.cos(self.angle)*100), self.rect.center[1] - (math.sin(self.angle)*100)))


    #Methods for the class. We are going to create a method for the ball to bounce, rather than putting it in the game logic.
    # (We are doing this in case we want other shit to bounce in later levels.)
    def bounce(self):
        if self.launched:
            if self.rect.right >= self.right_bound or self.rect.x <= self.left_bound:
		# If we are hit the left or right edges just reverse the sign of the x component
                self.angle = math.atan2(math.sin(self.angle),-math.cos(self.angle))
            if self.rect.y <= self.top_bound:
		# If we hit the top reverse the sign of the y component
                self.angle = math.atan2(-math.sin(self.angle),math.cos(self.angle))
                self.rect.y = self.top_bound
            if self.rect.y >= self.bottom_bound:
                self.kill() #Removes the ball from all lists
            
            self.last_pos = (self.rect.center[0], self.rect.center[1])
             
            #Move the ball
            self.rect.x += self.speed*math.cos(self.angle)
            # We must subtract from y instead of adding because the traditional
            # coordinate plain that trigonometric funtions uses is a mirror of what
            # pygame uses
            self.rect.y -= self.speed*math.sin(self.angle)

    def hit(self, block, type = ''):
        # This method only get called when part of the ball.rect is inside block.rect
        # So we are guarenteed that, and can take advantage of that by only testing
        # where the ball is in relation to the block, we don't have to be sure the ball
        # is hitting the block because that's already given


        # We hit a block
        if type == '':
            # if we are in between the top and the bottom of the block, we must be on a side,
            # so switch the x velocity
            if self.rect.center[1] > block.rect.top and self.rect.center[1] < block.rect.bottom:
                print("right/left")
                self.angle = math.atan2(math.sin(self.angle), -math.cos(self.angle))
            # If we are in between the left and right of the block, we must have hit the top or bottom 
            # so switch the y velocity
            elif self.rect.center[0] > block.rect.left and self.rect.center[0] < block.rect.right:
                print("top/bottom")
                
                
                self.angle = math.atan2(-math.sin(self.angle), math.cos(self.angle))
            else:
                # if we didn't simply hit the top or bottom, it's going to be the more complex case
                # of the ball hitting the corner of the block
                print("Corner")
		# The rules I'm going to try to implement are the following:
		# If we hit the top corner while going downward, we will switch x
		# and y.  If we hit the bottom corner while going downward, we will
		# switch x and keep going downward.  If we hit the top corner while going
		# upward, we will keep going up and switch x.  If we hit the bottom corner
		# while going upward, we will switch x and y and make sure y keeps going downward 
		
		# NOTE: We are guarenteed to be at a corner 
		
		# we are going up
                if math.sin(self.angle) > 0:
			# bottom corner
                    if self.rect.center[1] > block.rect.bottom:
			    # bottom right
                        if self.rect.center[0] > block.rect.right:
                            # going up, bottom right, either way we are moving
                            # we should move right and move down
                            self.angle = math.atan2(abs(math.sin(self.angle)),abs(math.cos(self.angle)))
                            # bottom left
                        else:
                            #going up, bottom left, either way we are going
                            # we should move down and left
                            self.angle = math.atan2(abs(math.sin(self.angle)),-abs(math.cos(self.angle)))
		    # top corner
                    else:
                        if self.rect.center[0] > block.rect.right:
                            # going up, top right, we should go up and right
                            self.angle = math.atan2(-abs(math.sin(self.angle)), abs(math.cos(self.angle)))
                        else:
                            # going up, top left, we should go up and left
                            self.angle = math.atan2(-abs(math.sin(self.angle)), -abs(math.cos(self.angle)))
		# we are going down
                else:
			#top corner
                    if self.rect.center[1] < block.rect.top:
                        if self.rect.center[0] > block.rect.right:
                            # going down, top right, we should go up and right
                            self.angle = math.atan2(-abs(math.sin(self.angle)), abs(math.cos(self.angle)))
                        else:
                            # going down, top left, we should go left and up
                            self.angle = math.atan2(-abs(math.sin(self.angle)), -abs(math.cos(self.angle)))
		#bottom corner
                    else:
                        if self.rect.center[0] > block.rect.right:
                            # going down, bottom right, we should go down and right
                            self.angle = math.atan2(abs(math.sin(self.angle)), abs(math.cos(self.angle)))
                        else:
                            # going down, bottom left, we should go down and left
                            self.angle = math.atan2(abs(math.sin(self.angle)), -abs(math.cos(self.angle)))



            # We should move the ball with this new angle so that the ball dosen't infinitely hit the block
            #self.bounce()


        # We hit a paddle 
        # If the ball is in between the paddle.rect.top and in between the sides of the paddle
        elif self.rect.bottom > block.rect.top and self.rect.top < block.rect.top and self.rect.right > block.rect.left and self.rect.left < block.rect.right:
            # Change the angle of the ball based on the where it is on the paddle
            # The goal is to have the ball bounce off the paddle between pi/4 and 3pi/4

            # This ratio variable is between 0 and 1, 0 being all the way at the left
            # of the paddle and 1 being all the way at the right
            ratio = (self.rect.center[0]-block.rect.left)/block.rect.width
            self.angle = (3*math.pi/4) - (ratio*math.pi/2)
            # again we should move the ball so it doesn't infinitely hit the paddle
            #self.bounce()
 	
    
    #This function will change a ball
    def morph(self, size = None, color = None):
        if size:
            #### These commands should be a seperate function to avoid repatition
            self.size = size
            self.image = pygame.Surface([size, size])
            self.image.fill(BLACK)
            
            pygame.draw.circle(self.image, self.color, (int(size/2),int(size/2)), int(size/2))
            self.mask = pygame.mask.from_threshold(self.image, self.color, self.color)
            self.rect = self.image.get_rect(center = self.last_pos)

    #Calculate the euclidian distance between las_pos and a point
    def dist(self,point):
        return math.sqrt(pow(self.last_pos[0] - point[0], 2) + pow(self.last_pos[1] - point[1],2))
        

class Brick(pygame.sprite.Sprite):
    """
    This is a class for the Bricks. They are also Sprites.
    """

    def __init__(self, type, chromakey, pos):
        super().__init__()
        
        #Load the Image
        self.image = pygame.image.load(BRICKS[type]['image']).convert()
        self.image.set_colorkey(chromakey)
        
        #Create the bit mask
        ##### Could not find a way to make the mask work properly with the image
        ##### so I ended up having to use fill
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()
        
        #Run the rect to get the locations.
        self.rect = self.image.get_rect()
        
        #Place these locations
        self.rect.x = pos[0] * 50
        self.rect.y = pos[1] * 25

        self.type = type #Type of brick
        self.score = BRICKS[type]['score'] #Score the brick awards
        self.lives = BRICKS[type]['lives'] #Number of hits to remove it

    def hit(self, score, power_list, all_sprites_list):
        self.lives -= 1
	# Set the alpha based on how many lives the block has
        self.image.set_alpha(255*self.lives/BRICKS[self.type]['lives'])
       
        if self.lives <= 0:
            score += self.score #Add the score
            self.kill() #Removes from all lists

            #This gives two chances to create a powerup from killed brick
            ##### The frequency will need to be tuned ####
            if random.randint(1,10) > 8: #Roll a 10 die higher than 8 to spawn powerup
                power = Bigball(BLACK, self.rect.center)
                power_list.add(power)
                all_sprites_list.add(power)
            elif random.randint(1,10) > 8: #Roll a 10 die higher than 8 to spawn powerup
                power = Multiball(BLACK, self.rect.center)
                power_list.add(power)
                all_sprites_list.add(power)

        return score

class Paddle(pygame.sprite.Sprite):
    """
    This is a class for the Paddles. They are also Sprites.
    """
    left_bound = 0
    right_bound = 0
    top_bound = 0
    bottom_bound = 0
    
    def __init__(self, screen, color, size, pos):
        super().__init__()
        self.x_speed = 0
        self.y_speed = 0
        #Load the Image
        #self.image = pygame.image.load("player.png").convert()
        #self.image.set_colorkey(WHITE)
        #We are using bare surfaces for now.
        
        self.size = size
        self.image = pygame.Surface(size)
        self.image.fill(color)
        #Create a bit mask from the color
        self.mask = pygame.mask.from_threshold(self.image, color, color)
        self.mask.fill()

        #Run the rect to get the locations.
        self.rect = self.image.get_rect(center = pos)
        
        #Maximum movement of the paddle
        self.right_bound = screen.get_width()
        self.top_bound = 500
        self.bottom_bound = screen.get_height()
        

    def slide(self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        
        if self.rect.x >= (self.right_bound - self.size[0]):
            self.rect.x = (self.right_bound - self.size[0])
        if self.rect.y >= (self.bottom_bound - self.size[1]):
            self.rect.y = (self.bottom_bound - self.size[1])
        if self.rect.x <= self.left_bound:
            self.rect.x = self.left_bound
        if self.rect.y <= self.top_bound:
            self.rect.y = self.top_bound


class Powerup(pygame.sprite.Sprite):
    """
    This is a class for powerups . They are also Sprites.
    """
    left_bound = 0
    right_bound = 0
    top_bound = 0
    bottom_bound = 0
    x_speed = 0
    y_speed = 0
    
    def __init__(self, image_file, chromakey, pos):
        super().__init__()
        
        #Load the Image
        self.image = pygame.image.load(image_file).convert()
        self.image.set_colorkey(chromakey)
        #Create bit mask from image
        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()

        #Run the rect to get the locations.
        self.rect = self.image.get_rect(center = pos)
        
        self.y_speed = 3

    def move(self):
        self.rect.y += self.y_speed

class Multiball(Powerup):
    def __init__(self, chromakey, pos):
        super().__init__('multiball.png', chromakey, pos)

    def activate(self, screen, my_paddle, ball_list, all_sprites_list):
        #When the powerup is hit by the paddle it activates

        for i in [math.pi/4,math.pi/2,3*math.pi/4]: #Using three x-speeds
            ball = Gameball(screen, WHITE, 8,5, i, my_paddle) #Create a ball
            ball_list.add(ball)
            all_sprites_list.add(ball)
            ball.launch() #Launch it right away
        
        self.kill() #Removes from all lists

class Bigball(Powerup):
    def __init__(self, chromakey, pos):
        super().__init__('bigball.png', chromakey, pos)

    def activate(self, screen, my_paddle, ball_list, all_sprites_list):
        #When the powerup is hit by the paddle it activates
        for ball in ball_list:
            ball.morph(size = 16) #Increase the size of the ball
    
        self.kill() #Removes from all lists
