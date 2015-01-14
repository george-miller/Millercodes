import pygame
import random
import math

# Initiation procedures
pygame.init()
screen_width = 350
screen_height = 500
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Phoenix")

# This integer is used to seperate initialization from other processes inside the level methods
moveincount = 0

# Create an array of classic enemy positions, many levels will use this as their template
classic_positions = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),
                     (0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0)]

for i in range(5):
    classic_positions[i] = (68 + (i*56), -120)
    classic_positions[i+10] = (68 + (i*56),-55)

for i in range(5):
    classic_positions[i+5] = (40 + (i*56),-90)
    classic_positions[i+15] = (40 + (i*56),-20)   
    
# Initialize a font variable to help with displaying score on the screen
score_text = pygame.font.SysFont('ocraextended',14,False,False)
splash_text = pygame.font.SysFont('ocraextended',18,True,False)

# Initialize sounds
laser_sound = pygame.mixer.Sound("laser.ogg")
bombhit_sound = pygame.mixer.Sound("bombhit.ogg")
pygame.mixer.music.load("techno_loop.ogg")
pygame.mixer.music.play()

# This is our level control variable, it will take us through the game and it's different scenes (-1 indicates gameover)
level = 0

# Initialize sprite groups
enemy_weapon_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
player_weapon_sprites = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


# ---------------- CLASS DEFENITIONS ------------- #
# The engine will call every class's draw and update functions every frame
# Class defenitions for sprites control how they move, update, draw, fire things, and get hit
# The engine controls how they interact

class SpriteSheet():
    """This class was taken from programarcadegames.com to create an easy way to interface with the sprite sheet.
    Using a sprite sheet instead of multiple files makes it more efficient in terms of storage and makes it super
    easy to edit"""
    
    # Initiate by loading up the sprite sheet image
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
        
    # Use given coordinates and width and height to grab an image off the sprite sheet and return it for use as a sprite
    def get_image(self, x, y, width, height):
        # create a surface, copy a part of the spritesheet to that surface, return the surface
        image = pygame.Surface((width, height)).convert()
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        image.set_colorkey((255,255,255))
        return image

# We will use this variable to grab all of our sprites from
# I use a sprite sheet I drew myself, the green lines on the outside of the drawings are to help me make sure
# I'm not giving too much space to a certain sprite
sprite_sheet = SpriteSheet("sheet.png")

class Bomb(pygame.sprite.Sprite):
    """This class represents a simple bomb.  All it does is move down the screen, but it can 
    be used in multiple ways through the damage variable"""
    def __init__(self, x, y, speed, damage):
        # call the super, get the image from the sprite sheet, set variables
        super().__init__()
        self.image = sprite_sheet.get_image(25,20,3,3)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.damage = damage
        
    def draw(self, screen):
        # draw onto the screen
        screen.blit(self.image, (self.rect.x,self.rect.y))
    
    def update(self):
        # Move downwards toward the ship, if you've gone off the screen, delete yourself
        self.rect.y += self.speed
        if self.rect.y > screen_height:
            enemy_weapon_sprites.remove(self)
            all_sprites.remove(self)

class Rocket(pygame.sprite.Sprite):
    """This class represents an enemy rocket.  They can move in any direction and self.angle is in degrees.  South is 
    0 degrees, east is 90 degrees and west is -90 degrees.  Other derivations of angles aren't recommended because they 
    probably won't work"""
    def __init__(self,x,y,angle,speed):
        # call super
        super().__init__()
        # I had to creat a self.image0 because we will modify self.image later to rotate it, and we need to keep 
        # a default image poitning south to rotate from
        self.image0 = sprite_sheet.get_image(55,26,10,14)
        self.image0.set_colorkey((255,255,255))
        self.image = self.image0
        self.rect = self.image0.get_rect()
        # this should be kept between -90 and 90 to produce good results
        # NOTE something weird happens when the angle is 0
        self.angle = angle
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.damage = 1
        # Since the self.rect variable stores integers as its x and y, we must use these two floats to determine
        # position so that we can use decimals. Otherwise the angle calculations will be rounded to whole numbers
        # and result in an unrealistic arc
        self.x = x
        self.y = y
    
    def draw(self,screen):
        # rotate the image and put it into self.image
        # It works, but defenitely makes the rockets look odd soemtimes
        self.image = pygame.transform.rotate(self.image0, self.angle)
        screen.blit(self.image, (self.rect.x,self.rect.y))
    
    def update(self):
        # I seperated the calculations to make sure nothing weird happens.  In the past a lot of weird stuff happens with
        # angle measurements so I wanted to be sure everything was getting an expected value
        # See above self.x defenition for more
        if self.angle > 0:
            self.x += self.speed*math.sin(math.radians(self.angle))
            self.y += self.speed*math.cos(math.radians(self.angle))
        elif self.angle < 0:
            self.x -= self.speed*math.sin(math.radians(-self.angle))
            self.y += self.speed*math.cos(math.radians(-self.angle))
        self.rect.x = self.x
        self.rect.y = self.y
        # If the rocket goes off the screen, delete it
        if (self.rect.x > screen_width or self.rect.x < 0) or (self.rect.y > screen_height or self.rect.y < 0):
            all_sprites.remove(self)
            enemy_weapon_sprites.remove(self)
    
    # This method changes the direction of the rocket toward a point x,y
    def home(self,x,y):
        # If a rocket is above the ship still, change the angle toward the ship
        if self.rect.y < y:
            # Again I seperated the calculations to make sure nothing weird happens
            if self.rect.x < x:
                self.angle = math.degrees(math.atan((x-self.rect.x)/(y-self.rect.y)))
            else:
                self.angle = math.degrees(-math.atan((self.rect.x-x)/(y-self.rect.y)))
        # Don't try anything if the rocket is below the ship
        else:
            pass

class Laser(pygame.sprite.Sprite):
    """This class represents the starting weapon of our ship.  It can be used in the future however with more complex weaponry"""
    def __init__(self, x, y, speed,damage):
        laser_sound.play()
        # call super, set variables, get image from spritesheet
        self.image = sprite_sheet.get_image(0,24,1,9)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.damage = damage
        super().__init__()
        
    def draw(self,screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self):
        # update the position with the given speed variable
        self.rect.y -= self.speed
        # NOTE: For more complex weapon systems, make sure you include something like this, so that the players
        # weapons don't hit enemys that are off screen, when the enemies are moving in for example
        if self.rect.y < 0:
            player_weapon_sprites.remove(self)
            all_sprites.remove(self)

class Player(pygame.sprite.Sprite):
    """This class represents the player.  I keep score and health in this class because this makes it easier to create
    two player functionality in the future.  I also keep many other expected values such as speeds and positions."""
    def __init__(self):
        # Simple intiation, setting values to expected defaults
        self.score = 0
        self.health = 10
        self.x_speed = 0
        self.y_speed = 0
        super().__init__()
        self.image = sprite_sheet.get_image(0,0,21,21)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        # This makes the player start at the center of the screen
        self.rect.x = (screen_width/2) - 10
        self.rect.y = screen_height * 5/6
        self.equipped = 1
        
    def draw(self, screen):
        # draw the ship, the health bar, and the score
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, (0,0,0), (5,(5+((screen_height-10) * (10-self.health)/10)),5,self.health*((screen_height-10)/10)))
        screen.blit(score_text.render("Score " + str(self.score),True, (0,0,0)),(screen_width-100,10))
        
        
    def update(self):
        # update the position based on the current speeds, making sure the ship doesn't go off screen
        # NOTE: current speeds are based on key input
        self.rect.x+=self.x_speed
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        elif self.rect.left < 0:
            self.rect.left = 0
        self.rect.y+=self.y_speed
        if self.rect.bottom > 500:
            self.rect.bottom = 500
        elif self.rect.top < 0:
            self.rect.top = 0
            
    def fire(self):
        # Fire a weapon based on what is equipped
        if self.equipped == 1:
            laser = Laser(self.rect.left+(self.rect.width/2), self.rect.y - 6,3,1)
            player_weapon_sprites.add(laser)
            all_sprites.add(laser)
        #elif self.equipped == 2
    
    # This method will be called whenever a sprite in enemy_weapon_sprites collides with the ship    
    def hit(self, damage):
        # Decrease health and if we are dead, send us to the gameover screen
        bombhit_sound.play()
        global level
        self.health -= damage
        if self.health < 1:
            level = -1
    
    # simple method to get the center of the ship
    def get_center(self):
        return (self.rect.x + (self.rect.width/2), self.rect.y + (self.rect.height/2))
    
    # returns the damage of the current weapon, this will be called when determining how much damage to give to a enemy sprite
    # NOTE: This needs to be changed to accomedate weapons with different damage values
    def get_damage(self):
        if self.equipped == 1:
            return 1
        #elif self.equipped == 2:
            #return 2

# Create the player
player = Player()
all_sprites.add(player)

class Enemy(pygame.sprite.Sprite):
    """This class is a parent of all enemy classes, combining features that all enemies have"""
   
    # Simple initiation constructor, since all enemies have position and speed
    def __init__(self,x,y,x_speed,y_speed):
        super().__init__()
        self.random = 0
        self.update_count = 0
        self.x_speed = x_speed
        self.y_speed = y_speed
        # default enemy image is a simple alien
        self.image = sprite_sheet.get_image(25,0,18,15)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 2
        
    # This method creates the classic space invaders movement
    # This method should be overridden with more complex enemy classes like bosses or higher level enemies
    # Down, Up, Left, Right repeat
    def update(self):
        self.random = random.random()
        
        if self.random > .99:
            self.bomb_drop()
        
        # We only want to start doing the movement after we have moved in completely
        if moveincount > 174:
            # A simple if elif else statement is used with modulous to determine when to switch directions
            if self.update_count%80 < 20:
                self.rect.y+=self.y_speed
            elif self.update_count%80 < 40:
                self.rect.x+=self.x_speed
            elif self.update_count%80 < 60:
                self.rect.y-=self.y_speed
            else:
                self.rect.x-=self.x_speed
            #Increment the count so the update changes direction
            self.update_count+= 1
    
    def draw(self, screen):
        screen.blit(self.image,(self.rect.x,self.rect.y))
        
    # This will be called randomly in the update function
    def bomb_drop(self):
        # create a bomb at self's position and drop it
        bomb = Bomb(self.rect.left+(self.rect.width/2) - 1, self.rect.y + 3,3,1)
        enemy_weapon_sprites.add(bomb)
        all_sprites.add(bomb)
    
    # This method wil be called when a thing in player_weapon_sprites collides with a thing in enemy_sprites
    def hit(self, damage):
        # decrease health, if self is dead, remove it from the lists
        self.health -= damage
        if self.health < 1:
            enemy_sprites.remove(self)
            all_sprites.remove(self)
            player.score+=1


class Boss1(Enemy):
    """This class represents the first boss.  He moves left and right and fires rockets (which are a little buggy)"""
    def __init__(self, x, y, x_speed,y_speed):
        # call super, get sprite, set variables
        super().__init__(x,y,x_speed,y_speed)
        self.image = sprite_sheet.get_image(52,0,60,23)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 50
    
    # This method creates rockets and fires them in an arc below the boss
    def fire_rockets(self):
        for i in range(6):
            # create a rocket, setting the angle to form an arc
            rocket = Rocket(float(self.rect.x + (self.rect.width/2)), float(self.rect.y + (self.rect.height/2)), (i*15)-44, 3)
            enemy_weapon_sprites.add(rocket)
            all_sprites.add(rocket)
            
        
    def update(self):
        # If we have moved into the scene, start firing rockets and moving back and forth
        global moveincount
        if moveincount > 109:
            moveincount+=1
            
            # chance to fire rockets in an arc
            if moveincount % 60 == 0:
                self.fire_rockets()
            # chance to call home() on every rocket in enemy_weapon_sprites
            if moveincount % 87 == 0:
                for thing in enemy_weapon_sprites:
                    thing.home(player.get_center()[0], player.get_center()[1])
            # move left and right        
            self.rect.x += self.x_speed
            if self.rect.right > 310 or self.rect.left < 40:
                self.x_speed *= -1
        
# ---------------- LEVELS ----------------------------
# These method represent levels, they are controlled by the 
# level integer.  This way one can leave the engine to do the
# updating, drawing, and event handling while the level methods
# do the creation of enemies.  These could be thought of as the 
# 'scenes' of the game


# This is our level 0 method, called every frame
def splashscreen(screen):
    global level
    # Write some text, and if the player goes close to the start button, start the game by incrementing level
    screen.blit(splash_text.render("ALERT!", True, (255,0,0)), (130,10))
    screen.blit(splash_text.render("Your Colony is Under Atack!", True, (255,0,0)), (20,50))
    screen.blit(splash_text.render("Use arrow keys to move", True, (255,0,0)), (30,70))
    screen.blit(splash_text.render("and a to attack", True, (255,0,0)), (50,90))
    screen.blit(splash_text.render("Move to Start to start", True, (255,0,0)), (35,110))
    screen.blit(splash_text.render("Start", True, (0,255,0)), (130,200))
    if player.rect.y < 230:
        if player.rect.x > 130 and player.rect.x < 200:
            level+=1

# This is our level 3 method, called every frame
def winner(screen):
    global level
    # Write 'you win' and if the player wants to reset, he can go into the reset button and things will be reset
    screen.blit(splash_text.render("YOU WIN", True, (0,0,255)), (120,100))
    screen.blit(splash_text.render("Reset", True, (0,255,0)), (130,200))
    if player.rect.y < 230:
        # if he wants to reset, we must reset a bunch of the lists and varialbes so that none of the awesome animation that
        # is still happening actually becomes real when you reset        
        if player.rect.x > 130 and player.rect.x < 200:
            for thing in enemy_sprites:
                enemy_sprites.remove(thing)
                all_sprites.remove(thing)
            for thing in enemy_weapon_sprites:
                enemy_weapon_sprites.remove(thing)
                all_sprites.remove(thing)
            player.health = 10
            moveincount = 0
            level= 1

# this is our level -1 method, for when the player dies        
def gameover(screen):
    # grab these two variables from the global
    global moveincount
    global level
    # Write some text, ask if he wants to quit or try again
    screen.blit(splash_text.render("GAME OVER", True, (255,0,0)), (120,100))
    screen.blit(splash_text.render("Try Again?", True, (0,255,0)), (70,200))
    screen.blit(splash_text.render("Quit", True, (0,0,0)), (230,200))
    if player.rect.y < 230:
        # if he wants to try again, we must reset a bunch of the lists and varialbes so that none of the awesome animation that
        # is still happening actually becomes real when you try again
        if player.rect.x > 70 and player.rect.x < 130:
            for thing in enemy_sprites:
                enemy_sprites.remove(thing)
                all_sprites.remove(thing)
            for thing in enemy_weapon_sprites:
                enemy_weapon_sprites.remove(thing)
                all_sprites.remove(thing)
            player.health = 10
            moveincount = 0
            level= 1
        # quit if he wants to
        elif player.rect.x > 200:
            pygame.quit()

# This is our level 1, just a classic bunch of mobs for you to blast at        
def level1():
    global moveincount
    global level
    # If we haven't died
    if player.health > 0:
        # initiate when moveincount is 0 by creating a bunch of enemies and giving them positions from the classic_postiions array
        if moveincount == 0:
            moveincount+=1
            for i in range(20):
                enemy = Enemy(classic_positions[i][0],classic_positions[i][1],1,1)
                enemy_sprites.add(enemy)
                all_sprites.add(enemy)
        # This part moves the sprites smoothly into the scene from the top
        elif moveincount < 175:
            for thing in enemy_sprites:
                thing.rect.y += 1
            moveincount+=1
        # When we have killed everything, advance to the next level
        else:
            if len(enemy_sprites) < 1:
                moveincount = 0
                level+=1
            
        
    # If we died send us to gameover        
    else:
        moveincount = 0
        level = -1
          
# This level is the boss using the Boss1 class
def level2():
    global moveincount
    global level
    # If we are alive
    if player.health > 0:
        # Initialize the boss when moveincount is 0
        if moveincount == 0:
            moveincount+=1
            boss = Boss1(50,-30,1,1)
            enemy_sprites.add(boss)
            all_sprites.add(boss)
        # Move the boss into the scene
        elif moveincount < 110:
            for thing in enemy_sprites:
                thing.rect.y+=thing.y_speed
            moveincount+=1
        # wait for him to die, then go to the winner screen
        else:
            if len(enemy_sprites) < 1:
                moveincount = 0
                level+=1
            
        
    # if we died send us to the gameover screen
    else:
        moveincount = 0
        level = -1    


# Varialbles to help the game engine
done = False
clock = pygame.time.Clock()


# --------------- GAME ENGINE ------------------------

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # adjust the speeds of the ship based on what is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.x_speed -= 3
            if event.key == pygame.K_RIGHT:
                player.x_speed += 3
            if event.key == pygame.K_UP:
                player.y_speed -= 3
            if event.key == pygame.K_DOWN:
                player.y_speed += 3
            # fire when we press 'a'
            if event.key == pygame.K_a:
                player.fire()
        # adjust the speeds of the ships when keys are released    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.x_speed += 3
            if event.key == pygame.K_RIGHT:
                player.x_speed -= 3
            if event.key == pygame.K_UP:
                player.y_speed += 3
            if event.key == pygame.K_DOWN:
                player.y_speed -= 3
    
    
    # We must do this first because the splash screen and gameover method draw things
    screen.fill((255,255,255))
    
    
    #GAME LOGIC
    if level == 0:
        splashscreen(screen)
    elif level == 1:
        level1()
    elif level == 2:
        level2()
    elif level == 3:
        winner(screen)
    else:
        gameover(screen)
        
    
    # update everything
    for thing in all_sprites:
        thing.update()
    
    # get collisions between players weapons and enemy sprites
    enemy_hit_list = pygame.sprite.groupcollide(enemy_sprites, player_weapon_sprites, False,True )
    # give damage to things that are hit
    for thing in enemy_hit_list:
        thing.hit(player.get_damage())
    # get collisions between the player and the enemy weapons
    player_hit_list = pygame.sprite.spritecollide(player, enemy_weapon_sprites, True)
    # Hit the player with damage when collided
    for thing in player_hit_list:
        player.hit(thing.damage)
    
    #DRAWING
           
    
    
    # draw everything
    for thing in all_sprites:
        thing.draw(screen)    
            
    pygame.display.flip()
    
    clock.tick(60)  

    
pygame.quit()


