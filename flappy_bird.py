import pygame
import neat
import os
import time
import random

#window dimensions
windowWIDTH = 600
windowHEIGHT = 800

#loading the three bird images so it looks liek there is animation of it flapping wings
BIRDIMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPEIMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASEIMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BACKGROUNDIMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRDIMGS
    MAXROTATION = 25 #degrees, so that when the bird moves up, it looks like it is tilting up towards the sky
    ROTVEL = 20
    ANIMATIONTIME = 5 #how fast the bird will look like it is flapping its wings
    
    #initialize bird
    def __init__(self, x, y): #the bird has x and y coords
        self.x = x
        self.y = y
        self.tilt = 0 #default zero because the bird is flat once it starts moving, it will rotate later
        self.tickCount = 0
        self.vel = 0
        self.height = self.y #height is just the y coord
        self.imgCount = 0 #this is for knowing which image in the animation the bird is currently showing
        self.img = self.IMGS[0] #this sets the first default image of the bird to be the first one in the list of animation images
    
    
    