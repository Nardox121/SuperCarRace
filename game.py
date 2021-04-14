import pygame
import sys
from math import copysign
from Car import Car
from CarAI import CarAI
from Map import Map
import neat


def withoutAI():
    width = 1024
    height = 600
    pygame.display.set_caption("SuperCarRace")
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    ticks = 60

    path = "assets/Map.bmp"
    path2 = "assets/RewardMap.bmp"
    gameMap = Map(path, path2)
    car = Car(4.5, 9)
    car_image = pygame.transform.scale(pygame.image.load("assets/Car.png"), (28, 16))

    while True:
        dt = clock.get_time() / 300
        gameMap.refresh(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        pressed = pygame.key.get_pressed()

        car.move(dt, pressed)
        car.update(dt)
        
        gameMap.refresh(screen)
        #car.update_dist(screen, gameMap.map)
        rotated = pygame.transform.rotate(car_image, car.angle)
        rect = rotated.get_rect()
        car.checkCollision(rect, gameMap.map)
        screen.blit(rotated, car.position * 32 - (int(rect.width / 2), int(rect.height / 2)))
        
        #refresh window
        pygame.display.flip()
        clock.tick(ticks)



def withAI(genomes, config):
    width = 1024
    height = 600
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    ticks = 60
    path1 = "assets/Map3.bmp"
    path2 = "assets/RewardMap3.bmp"
    gameMap = Map(path1, path2)

    car_image = pygame.transform.scale(pygame.image.load("assets/Car2.png"), (28, 16))
    player_image = pygame.transform.scale(pygame.image.load("assets/Car.png"), (28, 16))
    
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    cars = []
    rects = []
    ge = []

    player = Car(3, 10)

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(CarAI(3.5, 10))
        rotated = pygame.transform.rotate(car_image, cars[0].angle)
        rects.append(rotated.get_rect())
        ge.append(genome)
        

    clock = pygame.time.Clock()

    run = True
    while run and len(cars) > 0:
        clock.tick(ticks)
        dt = clock.get_time() / 300

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                breakpoint

        for x, car in enumerate(cars):  
            #output to tablica z 4 wyjściami który klawisz kliknąć
            output = nets[cars.index(car)].activate((car.distances + [car.velocity.x ,car.velocity.y]))
            
            # OUTPUT -> [up, down, right, left]
            car.move(dt, output)
            car.update(dt)
            #print(ge[x].fitness)

        ##  v tu ma być całe rysowanie mapy v
        gameMap.refresh(screen)
        for (car, rect) in zip(cars, rects):
            if car.dead:# jeśli auto umarło
                nets.pop(cars.index(car))
                ge.pop(cars.index(car))
                rects.pop(cars.index(car))
                cars.pop(cars.index(car))
            else:
                car.update_dist(screen, gameMap.map)
                rotated = pygame.transform.rotate(car_image, car.angle)
                rects[cars.index(car)] = rotated.get_rect()
                car.checkCollision(rect, gameMap.map)
                car.isAwarded(rect,gameMap.map)
                screen.blit(rotated, car.position * 32 - (int(rect.width / 2), int(rect.height / 2)))   
        
        # v rysowanie playera v # 
        pressed = pygame.key.get_pressed()

        player.move(dt, pressed)
        player.update(dt)
        
        rotated_player = pygame.transform.rotate(player_image, player.angle)
        rect_player = rotated_player.get_rect()
        player.checkCollision(rect_player, gameMap.map)
        screen.blit(rotated_player, player.position * 32 - (int(rect_player.width / 2), int(rect_player.height / 2)))   

        #refresh window
        pygame.display.flip()
        clock.tick(ticks)

