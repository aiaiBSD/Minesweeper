import pygame, sys
from pygame.locals import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode((1000, 650))
pygame.display.set_caption('Alpha Raccoon')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MIX1 = (30, 60, 90, 255)
MIX2 = (100, 200, 100, 150)
MIX3 = (200, 100, 200, 75)
DISPLAYSURF.fill(WHITE)
raccoonImg = pygame.image.load('AlphaRaccoon.jpg')
DISPLAYSURF.blit(raccoonImg, (150, 100))
TRANSPARENTSURFACE = DISPLAYSURF.convert_alpha()
pygame.draw.line(TRANSPARENTSURFACE, MIX1, (100, 60), (200, 60), 5)
pygame.draw.circle(TRANSPARENTSURFACE, MIX2, (400, 600), 50, 5)
pygame.draw.polygon(TRANSPARENTSURFACE, MIX3, ((600, 400),  (650, 400), (650, 350), (600, 350)), 5)
pygame.draw.line(TRANSPARENTSURFACE, RED, (100, 160), (300, 260), 5)
pygame.draw.polygon(TRANSPARENTSURFACE, BLACK, ((500, 0), (650, 300), (780, 500), (550, 400), (400, 350)), 5)
DISPLAYSURF.blit(TRANSPARENTSURFACE, (0, 0))
pygame.mixer.music.load('airhorn.mp3')
pygame.mixer.music.play(-1, 0.0)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()