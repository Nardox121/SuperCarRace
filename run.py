import pygame, sys

screen = pygame.display.set_mode((512, 512))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()