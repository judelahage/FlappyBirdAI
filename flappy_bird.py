import pygame
import neat
import os
import time
import random

#window dimensions
windowWIDTH = 600
windowHEIGHT = 800

#loading the three bird images so it looks liek there is animation of it flapping wings
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPEIMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASEIMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BACKGROUNDIMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

