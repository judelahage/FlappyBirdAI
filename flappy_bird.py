import pygame
import neat
import os
import time
import random

#window dimensions
windowWIDTH = 500
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
    ANIMATIONTIME = 20 #how fast the bird will look like it is flapping its wings
    
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
    
    def jump(self):
        self.vel = -10.5 #velocity is negative becuase 0,0 is the top left of the screen, so in order to move up, there has to be a negative velocity
        self.tickCount  = 0 #tick count trracks when the bird last jumped
        self.height = self.y #we need to store the original height of the bird right before it jumps
        
    def move(self): #records one "move" of a bird in a frame
        self.tickCount +=1 #tick count increases by 1
        displacement = self.vel * self.tickCount + 1.5 * self.tickCount**2 #records the amount of distance that the bird moves in the frame
        
        #we have to implement a terminal velocity however, we don't want the velocity to get infinitely large
        if d >= 16: #if d gets to 16, then we keep it at 16
            d = 16; 

        if(d<0): #if d is negative, meaning were jumping, then that means that we make it more negative so the jumps get stronger and stronger
            d -= 2
            
        self.y += d #the y just hanges by d, and the bird only moves in the y direction, the background and tubes will move in x direction
        
        if d < 0 or self.y < self.height + 50: #basically we have to see, in the middle of the jump, if the bird is currently above the original y coordinate from where it jumped, then it should be tilted up
            if self.tilt < self.MAXROTATION:
                self.tilt = self.MAXROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTVEL
            
    def draw(self, win):
        #we have to track the image count in order to animate the bird
        #so
        self.imgCount += 1
        
        if self.imgCount < self.ANIMATIONTIME: #cycle through images up and down as ANIMATIONTIME goes up
            self.img = self.IMGS[0]
        elif self.imgCount < self.ANIMATIONTIME*2:
            self.img = self.IMGS[1]
        elif self.imgCount < self.ANIMATIONTIME*3:
            self.img = self.IMGS[2]
        elif self.imgCount < self.ANIMATIONTIME*4:
            self.img = self.IMGS[1]
        elif self.imgCount < self.ANIMATIONTIME*4 + 1:
            self.img = self.IMGS[0]
            self.imgCount = 0
        
        #if the bird is tilted downwards we don't want wings to be flapping
        if self.tilt < -80:
            self.img = self.IMGS[1] #we goesshow the image where the wings of the bird are level
            self.imgCount = self.ANIMATIONTIME*2 #resets the imgCount to 2 times the ANIMATION time so that the bird image resets to the correct image in case the tilt changes
        
        rotatedImage = pygame.transform.rotate(self.img, self.tilt) #this stores the rotated image, however this is not rotated around the center
        newRectangle = rotatedImage.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center) #this makes i so that the image is rotated about the center instead
        win.blit(rotatedImage, newRectangle.topleft)
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)



def draw_window(win, bird):
    #win.blit just draws onto the window
    win.blit(BACKGROUNDIMG, (0,0)) #draws background
    bird.draw(win) #draws bird
    pygame.display.update()

def main(): #main method
    startingX = 200
    startingY = 200
    
    bird = Bird(startingX, startingY) #create new bird
    
    win = pygame.display.set_mode((windowWIDTH, windowHEIGHT))
    #the tick rate is too fast which results in the bird nosediving into the ground too fast
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(30) #this delays the rate at which the bird can fall
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ig pygame detects an event that the user quit the game, ie click the x at the top of the window, then we indicate to stop running
                run = False
        #while the game is running, obviously the bird has to move
        bird.move() #bird continually moves, and points downwards as it starts nosediving at a negative velocity since it is not jumping at all to fight gravity
        draw_window(win, bird)
    pygame.quit()
    quit()

main()