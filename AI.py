import random
import os
import time
import neat
import pygame
import sys
from math import copysign
from Car import Car
from CarAI import CarAI
from Map import Map

def eval_genomes(genomes, config):
    """
    runs the simulation of the current population of
    birds and sets their fitness based on the distance they
    reach in the game.
    """
    
    width = 1024
    height = 600
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    ticks = 60
    path1 = "assets/Map.bmp"
    path2 = "assets/RewardMap.bmp"
    gameMap = Map(path1, path2)

    car_image = pygame.transform.scale(pygame.image.load("assets/Car.png"), (28, 16))
    
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    cars = []
    rects = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(CarAI(4.5, 9))
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

        for x, car in enumerate(cars):  # give each car a fitness of 0.1 for each frame it stays alive
            ge[x].fitness += 0.1
            #output to tablica z 4 wyjściami który klawisz kliknąć
            output = nets[cars.index(car)].activate((car.distances + [car.velocity.x ,car.velocity.y]))
            
        #### v odejmowanie punktów za stanie w miejscu lol v ####
            if output < [0.5, 0.5, 0.5, 0.5]:
                ge[x].fitness -= 3
            
            # OUTPUT -> [up, down, right, left]
            car.move(dt, output)
            car.update(dt)
            #print(ge[x].fitness)

        ##  v tu ma być dodawanie fitnessu tylko nie wiem za co v    
        '''if True:
            # can add this line to give more reward for passing through a pipe (not required)
            for genome in ge:
                genome.fitness += 5
        '''
        ##  v zabijanie nierobów v  ##
        for genome in ge:
            if genome.fitness < -10:
                cars[ge.index(genome)].dead = True
            else:
                genome.fitness += 0.1

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
                if(car.checkCollision(rect, gameMap.map)):
                    ge[cars.index(car)].fitness -= 3
                elif(car.isAwarded(rect,gameMap.map)):
                    ge[cars.index(car)].fitness += 2
                screen.blit(rotated, car.position * 32 - (int(rect.width / 2), int(rect.height / 2)))   

        #refresh window
        pygame.display.flip()
        clock.tick(ticks)

        # break if score gets large enough
        '''if score > 20:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break'''


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 50)
    #stats.save("result.txt")
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

