import pygame
import neat
import os
import time
import random
pygame.font.init()

#vars
GEN = 0
windowWIDTH = 500
windowHEIGHT = 800
gameVel = 5 #global speed at which the background and pipes will move at
birdStartingX = 230 #bird starting x coord
birdStartingY = 350 #bird starting y coord
pipeGAP = 700 #gap in between pipes

#loading the three bird images so it looks liek there is animation of it flapping wings
BIRDIMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPEIMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASEIMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BACKGROUNDIMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STATFONT = pygame.font.SysFont("comicsans", 50) #sets the font


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
        if displacement >= 16: #if d gets to 16, then we keep it at 16
            displacement = 16; 

        if(displacement<0): #if d is negative, meaning were jumping, then that means that we make it more negative so the jumps get stronger and stronger
            displacement -= 2
            
        self.y += displacement #the y just hanges by d, and the bird only moves in the y direction, the background and tubes will move in x direction
        
        if displacement < 0 or self.y < self.height + 50: #basically we have to see, in the middle of the jump, if the bird is currently above the original y coordinate from where it jumped, then it should be tilted up
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

class Pipe:
    GAP = 200 #there is a 200 pixel gap in between each pipe
    
    def __init__(self, x): #y coord is random
        self.x = x
        self.height = 0
        self.top = 0 #top of each pipe is default at 0
        self.bottom = 0 #bottom of each pipe is default at zero, it is important to track top and bottom so we know where it is drawn for collisions
        self.PIPE_TOP = pygame.transform.flip(PIPEIMG, False, True) #the image of a top pipe is the image we have in the folder flipped
        self.PIPE_BOTTOM = PIPEIMG #the image of a bottom pipe is just the image we have in the folder
        self.passed = False #tracks if the pipe was passed or not
        self.set_height() #defines where the top and bottom of the pipe and their gap
    
    def set_height(self):
        self.height = random.randrange(50,450) #the height of each pipe is a random number
        self.top = self.height - self.PIPE_TOP.get_height() #the top of the pipe is going to have to be the height position of the pipe minus the actual height of the pipe image in order to get the correct y coordinate placement for pipe
        self.bottom = self.height + self.GAP #the bottom of he pipe is going to have to be the 
        
    def move(self): #the pipe just moves to the left at the rate specified in game vel
        self.x -= gameVel
    
    def draw(self, win):
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        win.blit(self.PIPE_TOP, (self.x, self.top))
        
    def collide(self, bird):
        birdMask = bird.get_mask() #bird mask is basically a hitbox for the bird, it acts as an array which sotres all the pixels of the bird png file which are not transparent
        topMask = pygame.mask.from_surface(self.PIPE_TOP) #mask for top pipe
        bottomMask = pygame.mask.from_surface(self.PIPE_BOTTOM) #mask for bottom pipe
        topOffset = (self.x - bird.x, self.top - round(bird.y)) #offset is distance from bird to pipe
        bottomOffset = (self.x - bird.x, self.bottom - round(bird.y)) #distance from bird to bottom pipe
        
        #now we need to find the point of collision if the masks collide
        
        bPoint = birdMask.overlap(bottomMask, bottomOffset) #gets the point of collision of the birdmask and the bottompipe mask, returns None if not colliding
        tPoint = birdMask.overlap(topMask, topOffset) #gets the point of collision of the birdmask and the top pipe mask, returns None if not colliding
        
        if bPoint or tPoint: #if one of these has a collision, then
            return True #return true that yes there is a collision
        
        return False #otherwise return false

class Base:
    WIDTH = BASEIMG.get_width()
    IMG = BASEIMG
    
    #dont need to define x since it is going to be moving to the left
    def __init__(self, y):
        self.y = y
        self.x1 = 0 #x1 is the x coord of the first copy of the base image
        self.x2 = self.WIDTH #x2 is the x coord of the second copy of the base image
    
    def move(self):
        self.x1 -= gameVel
        self.x2 -= gameVel
        
        if self.x1 < -self.WIDTH: #if the x coord of the beginning of the bg image is less then it has to get rotated out
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 < -self.WIDTH: #same thing for this one
            self.x2 = self.x1 + self.WIDTH
            
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y)) #draw the first copy of the image
        win.blit(self.IMG, (self.x2, self.y)) #draw the second copy of the iamge
            
            
def draw_window(win, birds, pipes, base, score, gen):
    #win.blit just draws onto the window
    win.blit(BACKGROUNDIMG, (0,0)) #draws background
    for pipe in pipes:
        pipe.draw(win)
        
    for bird in birds:
        bird.draw(win)
    text = STATFONT.render("Score: " + str(score), 1,(255, 255, 255))
    win.blit(text, (windowWIDTH - 10 - text.get_width(), 10))
    
    text = STATFONT.render("Gen: " + str(GEN), 1,(255, 255, 255))
    win.blit(text, (10, 10))
    
    base.draw(win)
    pygame.display.update()

def main(genomes, config): #main method
    global GEN
    GEN += 1
    nets = [] #keep track of the neural network for the birds
    ge = [] #keep track of genomes
    birds = [] #create new bird
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config) #set up the neural network
        nets.append(net) #append it to the list
        birds.append(Bird(birdStartingX, birdStartingY)) #then append a new bird object to the list
        g.fitness = 0 #the starting fitness for every genome is zero
        ge.append(g) #add the genome to the list


    baseLevel = windowHEIGHT - 70
    base = Base(baseLevel)
    pipes = [Pipe(pipeGAP)]
    win = pygame.display.set_mode((windowWIDTH, windowHEIGHT))
    #the tick rate is too fast which results in the bird nosediving into the ground too fast
    clock = pygame.time.Clock()
    score = 0 #stores the current score of the player, obviously AI is playing
    run = True
    
    while run:
        clock.tick(30) #this delays the rate at which the bird can fall
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #ig pygame detects an event that the user quit the game, ie click the x at the top of the window, then we indicate to stop running
                run = False
                pygame.quit()
                quit()
        #we have to make the birds move accordingly to the neural network
        pipeInd = 0 #indicator for which pipe the bird should be looking at
        if len(birds) > 0: #if there are birds left in the list
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width(): #if there is more than one pipe and the bird has passed the current pipe
                pipeInd = 1 #look at the next pipe
        else:
            run = False
            break        
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1 #give the bird just a tad bit of fitness for moving forward, only give a little since the loop is executing 30 times a second
            
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipeInd].height), abs(bird.y-pipes[pipeInd].bottom))) #activates the neural network and passes the value to the function to see if we pass the threshhold we want in order to say a bird should jump or not
            if output[0] > 0.5:
                bird.jump()
            
        base.move() #base continually moves
        rem = [] #list of removed pipes
        addPipe = False
        for pipe in pipes: #pipes have to move too
            for x, bird in enumerate(birds): #loop through the birds in an enumerated list so that you can get the index 
                if pipe.collide(bird): #first check if pipe collides
                    ge[x].fitness -= 1 #every tiome a bird hits a pipe, it is going to have 1 remoed from its fitness score
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    
                if not pipe.passed and pipe.x < bird.x: #if the pipe has not been passed and the bird crosses the x coord of the pipe, then we update the status of the pipe to passed
                    pipe.passed = True
                    addPipe = True #determines whether we should add another pipe if the current one was passed
            
        
            if pipe.x + pipe.PIPE_TOP.get_width() < 0: #check if pipe is completely off the screen
                rem.append(pipe)   #remove pipe
            pipe.move()
        
        if addPipe: #if we have to add another pipe
            score +=1
            for g in ge:
                g.fitness += 5 #increment fitness by 5 if the bird scores so that the birds that make it through are pushed forward
            pipes.append(Pipe(pipeGAP)) #new pipe gets added to the list of pipes so that new pipes keep showing up
        
        for pipe in rem: #eliminate any pipes tat got sent to the remove list
            pipes.remove(pipe)
        
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= baseLevel or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        draw_window(win, birds, pipes, base, score, GEN)

def run(configPath):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, configPath) #setting all the properties from the config file
    genCount = 50
    pop = neat.Population(config) #stores a newly generated population based on the config we gave neat
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    
    winner = pop.run(main,genCount) #runs main for however many generations we want

if __name__ == "__main__":
    localDir = os.path.dirname(__file__) #gets the local directory we are in
    configPath = os.path.join(localDir, "config-feedforward.txt") #gets the config file path from our directory
    run(configPath)
    