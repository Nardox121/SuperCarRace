import pygame
import sys
from math import copysign
from Car import Car

width = 1024
height = 500
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
car = Car(10, 10)
clock = pygame.time.Clock()
ticks = 60

car_image = pygame.transform.scale(pygame.image.load("assets/Car.png"), (28, 16))

while True:
    dt = clock.get_time() / 500

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
        if car.velocity.x < 0:
            car.acceleration = car.brake_deceleration
        else:
            car.acceleration += 1 * dt
    elif pressed[pygame.K_DOWN]:
        if car.velocity.x > 0:
            car.acceleration = -car.brake_deceleration
        else:
            car.acceleration -= 1 * dt
    elif pressed[pygame.K_SPACE]:
        if abs(car.velocity.x) > dt * car.brake_deceleration:
            car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
        else:
            car.acceleration = -car.velocity.x / dt
    else:
        if abs(car.velocity.x) > dt * car.free_deceleration:
            car.acceleration = -copysign(car.free_deceleration, car.velocity.x)
        else:
            if dt != 0:
                car.acceleration = -car.velocity.x / dt
    car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

    if pressed[pygame.K_RIGHT]:
        car.steering -= 30 * dt
    elif pressed[pygame.K_LEFT]:
        car.steering += 30 * dt
    else:
        car.steering = 0
    car.steering = max(-car.max_steering, min(car.steering, car.max_steering))
    
    car.update(dt)

    ppu = 32
    screen.fill((80, 85, 80))
    rotated = pygame.transform.rotate(car_image, car.angle)
    rect = rotated.get_rect()
    screen.blit(rotated, car.position * ppu - (rect.width / 2, rect.height / 2))
    #refresh window
    pygame.display.flip()
    clock.tick(ticks)
