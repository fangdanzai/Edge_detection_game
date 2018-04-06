 
import pygame
from pygame.locals import *
import sys
import time
import pyganim
import collections
 
import random
import math

import numpy
print numpy.__path__
import cv2

imageurl = 'home.png'
im = cv2.imread(imageurl)
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,78,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


epsilon = 0.1*cv2.arcLength(contours[0],True)
approx = cv2.approxPolyDP(contours[0],epsilon,True)




def fill(ct,allposn):
    for a in ct:
        for b in a:
            for c in b:
                allposn.append(c)

allctposn = []
fill(contours,allctposn)

def draw(allposn):
    for a in allposn:
        pygame.draw.circle(screen, (0,255,0), (a[0],a[1]), 2, 2)
        

#for O(1) search
ctdict = collections.defaultdict(dict)
for a in allctposn:
    ctdict[a[0]][a[1]] = True
    
#find if an area of object touches any dot saved in the dict
def touchbody(thing,radius):
    origx = int(thing.x)
    origy = int(thing.y+thing.h)
    for x in range(origx-radius,origx+radius):
        for y in range(origy-radius,origy+radius):
            if y in ctdict[x]:
                return True
    return False

## tool functions for geographic use
def finddistance(thing1,thing2):
    return math.sqrt((thing1.x-thing2.x)**2+(thing1.y-thing2.y)**2)

def findXdistance(thing1,thing2):
    return thing1.x-thing2.x

def findYdistance(thing1,thing2):
    return thing1.y-thing2.y


#----pre-processing part-----



 
# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
 
# Call this function so the Pygame library can initialize itself
pygame.init() 
 
 
# This sets the name of the window
pygame.display.set_caption('Game')
 
clock = pygame.time.Clock()

screen = pygame.display.set_mode([800,600])
 
# Before the loop, load the sounds:
#click_sound = pygame.mixer.Sound("laser5.ogg")
 
# Set positions of graphics
background_position = [0, 0]
 
# Load and set up graphics.
background_image = pygame.image.load(imageurl).convert()

bgwidth =  pygame.Surface.get_width(background_image)
bgheight =  pygame.Surface.get_height(background_image)

#The larger image is, the faster pixel-per-second it should be
speedscale = bgwidth/100


# sized screen

screen = pygame.display.set_mode([bgwidth, bgheight])


 
done = False
 
 
groundy = 10

#abstract class for all characters, environment variables are global variables 
class thing(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.jumping = 0
        
        self.left_sprite = []
        self.right_sprite = []
        
        self.w = 100
        self.h = 100
        
        self.g = 0
        
        self.facing = 'right'
        
        self.gifindex = 0
        
        self.speed = 1.5*speedscale
        
        
    def refresh(self):
        # Copy image to screen:
        #screen.blit(self.sprite, [self.x, self.y])
        self.gifindex += 0.2
        if self.gifindex >= len(self.left_sprite):
            self.gifindex = 0
        if self.facing == 'left':
            screen.blit(self.left_sprite[int(self.gifindex)], [self.x, self.y])
        else:
            screen.blit(self.right_sprite[int(self.gifindex)], [self.x, self.y])
            
            
    def move(self,direction,speed = None):
        if speed == None:
            speed = self.speed
            
        if direction == 'left' and self.x>0:
            self.x -= speed
        elif direction == 'right' and self.x+self.w*0.9<bgwidth:
            self.x += speed
        elif direction == 'up' and self.y>0:
            self.y -= speed
        elif direction == 'down' and self.y+self.h*0.9<bgheight and (not touchbody(self, int(self.w*0.1)) or self.jumping!=0):
            self.y += speed
        else:
            return False
        
        return True
    
    def down(self):
        self.y += 10 
    
    def teleport(self,x,y):
        self.x = x
        self.y = y
    
    def jump(self):
        self.jumping = 120
        
    #make time flows
    def tick(self):
        self.g += 0.5
        ##GRAVITY (AUTO-MOVE)
        canmove = self.move('down',self.g*speedscale)
        if canmove == False:
            self.g = 1
        
        ##JUMP (SEMI-AUTO)
        if self.jumping > 0:
            if self.g <= 12:
                self.move('up',12*speedscale)
                self.jumping -= 1
            else:
                self.jumping = 0
                self.g = 1
                        

#does Python really have inheritance? yes
class player(thing):
    def __init__(self):
        thing.__init__(self)
        
        self.desiredwidth = bgwidth/11
        self.desiredheight = self.desiredwidth*1.5
        
        image = pygame.image.load('gameimages/crono_left_run.000.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))
        
        image = pygame.image.load('gameimages/crono_left_run.001.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))
        
        image = pygame.image.load('gameimages/crono_left_run.002.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))
        
        image = pygame.image.load('gameimages/crono_left_run.003.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))
        
        image = pygame.image.load('gameimages/crono_left_run.004.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))
        
        image = pygame.image.load('gameimages/crono_left_run.005.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))
        
        self.left_stand = pygame.image.load('gameimages/crono_left.gif')
        self.left_stand = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        
        self.right_stand = pygame.transform.flip(self.left_stand, True, False)

        
        self.w = pygame.Surface.get_width(image)
        self.h = pygame.Surface.get_height(image)
        
    def refresh(self):
        # Copy image to screen:
        #screen.blit(self.sprite, [self.x, self.y])
        self.gifindex += 0.2
        if self.gifindex >= len(self.left_sprite):
            self.gifindex = 0
        if self.facing == 'left_running':
            screen.blit(self.left_sprite[int(self.gifindex)], [self.x, self.y])
        elif self.facing == 'right_running':
            screen.blit(self.right_sprite[int(self.gifindex)], [self.x, self.y])
        elif self.facing == 'left':
            screen.blit(self.left_stand, [self.x, self.y])
        else:
            screen.blit(self.right_stand, [self.x, self.y])
        

class enemy(thing):
    def __init__(self):
        thing.__init__(self)
        
        self.speed = 0.5*speedscale
        
        self.desiredwidth = bgwidth/20
        self.desiredheight = self.desiredwidth
        
        image = pygame.image.load('gameimages/enemy1.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))
        
        image = pygame.image.load('gameimages/enemy2.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))
        
        image = pygame.image.load('gameimages/enemy3.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))
        
        image = pygame.image.load('gameimages/enemy4.gif')
        image = pygame.transform.scale(image, (int(self.desiredwidth), int(self.desiredheight)))
        self.left_sprite.append(image)
        self.right_sprite.append(pygame.transform.flip(image, True, False))


        self.w = pygame.Surface.get_width(image)
        self.h = pygame.Surface.get_height(image)
        
    def stupidai(self,player):
        #print self.jumping
        if self.jumping == 0:
            if abs(findXdistance(self,player)) < 20: 
                if findYdistance(self, player) > 0:
                    self.jump()
                else:
                    self.down()
            else:
                if findXdistance(self,player) > 0:
                    self.move('left')
                else:
                    self.move('right')
            


class enemies():
    def __init__(self):
        self.allenemies = []
        
    def generateenemies(self):
        
        enemy1 = enemy()
        enemy1.teleport(random.randrange(0,bgwidth),random.randrange(0,bgheight))
    
        self.allenemies.append(enemy1)
        
    def refresh(self):
        for a in self.allenemies:
            a.refresh()
            
    def movements(self,player):
        for a in self.allenemies:
            a.tick()
            a.stupidai(player)
    def jumpall(self):
        for a in self.allenemies:
            a.jump()

    
player = player()
enemies = enemies()
enemies.generateenemies()
enemies.generateenemies()


# main
lastkey = ''
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Copy image to screen:
    screen.blit(background_image, background_position)

    
    
    #MOUSE
    player_position = pygame.mouse.get_pos()
    (pressed1,pressed2,pressed3) = pygame.mouse.get_pressed()
    if pressed1==1:
        player.teleport(player_position[0], player_position[1])
 
    ##KEY
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_LEFT]:
        player.facing = 'left_running'
        player.move('left')
        lastkey = 'left'
    if pressed[pygame.K_RIGHT]:
        player.facing = 'right_running'
        player.move('right')
        lastkey = 'right'
    if pressed[pygame.K_UP]:
        player.move('up')
    if pressed[pygame.K_DOWN]:
        player.down()
    if pressed[pygame.K_SPACE]:
        player.jump()
    if pressed[pygame.K_w]:
        enemies.jumpall()
        
    
    if event.type == pygame.KEYUP and player.jumping == 0:
        if not (pressed[pygame.K_RIGHT] or pressed[pygame.K_LEFT]):
            if lastkey == 'right':
                player.facing = 'right'
                lastkey = ''
            if lastkey == 'left':
                player.facing = 'left'
                lastkey = ''
            
    player.tick()
    
    enemies.movements(player)
    
    #REDRAW
    player.refresh()
    
    enemies.refresh()
 
 
 
 
    draw(allctposn)
 
    pygame.display.update()
 
    clock.tick(60)
 
pygame.quit()