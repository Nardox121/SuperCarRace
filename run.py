import pygame, sys
from Car import Car

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((512, 500))
car = Car(10,10)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            
    pressedKeys = pygame.key.get_pressed()

    if pressedKeys[pygame.K_RIGHT]:
        car.moveRight()
    if pressedKeys[pygame.K_LEFT]:
        car.moveLeft()
    if pressedKeys[pygame.K_UP]:
        car.moveUp()
    if pressedKeys[pygame.K_DOWN]:
        car.moveDown()


    screen.fill((0,0,0))
    pygame.draw.rect(screen, (245,25,25), car.getCar())
    pygame.display.flip()
    clock.tick(60)