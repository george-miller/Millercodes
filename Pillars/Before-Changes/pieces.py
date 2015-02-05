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
    x_speed = 0
    y_speed = 0
    
    last_pos = (0,0) #Will be used to improve accuracy on hit events
    
    launched = False #If the ball has been launched
    
    def __init__(self, screen, color, size, speed, paddle):
        #We will pass in the color and size of the ball.
        
        #First we call the parent constructor
        super().__init__()
        
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

        self.holdpaddle(paddle) #Place the ball at its initial position
        
        #Set the edges of the screen
        self.right_bound = screen.get_width() 
        self.bottom_bound = screen.get_height()

        self.x_speed = speed[0]
        self.y_speed = speed[1]
        
    def launch(self):
        self.launched = True
    
    def holdpaddle(self, paddle):
        #Move the ball directly above the paddle
        self.rect.center = (paddle.rect.center[0], paddle.rect.center[1] - paddle.rect.height/2 - 10)
        
    #Methods for the class. We are going to create a method for the ball to bounce, rather than putting it in the game logic.
    # (We are doing this in case we want other shit to bounce in later levels.)
    def bounce(self):
        if self.launched:
            if self.rect.x >= self.right_bound or self.rect.x <= self.left_bound:
                self.x_speed *= -1
            if self.rect.y <= self.top_bound:
                self.y_speed *= -1
                
            if self.rect.y >= self.bottom_bound:
                self.kill() #Removes the ball from all lists
            
            self.last_pos = (self.rect.center[0], self.rect.center[1])
            
            #Move the ball
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed

    def hit(self, block, type = ''):
        #This is the first pixel where the bit masks are touching
        point = pygame.sprite.collide_mask(block,self)

        if point:
            #Find the distance from each side of the block hit
            list = [('left', point[0]),
                    ('right', block.image.get_width() - point[0]),
                    ('top', point[1]),
                    ('bottom', block.image.get_height() - point[1])
                    ]
            
            #Sort the list to find the shortest distance
            #### This would ideally be the actual side the ball is hitting
            list = sorted(list, key=lambda x: x[1])
                
            if list[0][0] in ['top']: #If it is closest to the top
                if self.y_speed > 0:
                    self.y_speed *= -1
                #Keep the ball outside a moving paddle
                if type == 'paddle':self.rect.bottom = block.rect.top
                    
            elif list[0][0] in ['bottom']: #If it is closest to the bottom
                if self.y_speed < 0:
                    self.y_speed *= -1
                #Keep the ball outside a moving paddle
                if type == 'paddle':self.rect.top = block.rect.bottom
                    
            elif list[0][0] in ['left']: #If it is closest to the left
                if self.x_speed > 0:
                    self.x_speed *= -1
                #Keep the ball outside a moving paddle
                if type == 'paddle':self.rect.right = block.rect.left
                    
            elif list[0][0] in ['right']: #If it is closest to the right
                if self.x_speed < 0:
                    self.x_speed *= -1
                #Keep the ball outside a moving paddle
                if type == 'paddle':self.rect.left = block.rect.right
            
            if type == 'paddle' and list[0][0] == 'top':
                #Add up/remove to 10% the horizontal velocity depending on where the paddle is hit
                side_percent = (point[0] - (block.image.get_width()/2)) / block.image.get_width() / 5

                self.x_speed += abs(self.x_speed) * side_percent
            
            return list[0][0]

        return  None
    
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
        ### IN THE FUTURE CHANGE OPACITY OF BRICK RELATIVE TO ITS TOTAL LIVES ####

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
    x_speed = 0
    y_speed = 0
    
    def __init__(self, screen, color, size, pos):
        super().__init__()

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

        for i in [5,-1,3]: #Using three x-speeds
            ball = Gameball(screen, WHITE, 8, (i,-5), my_paddle) #Create a ball
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
