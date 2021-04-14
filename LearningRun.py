import pygame
import sys
from math import copysign
from Car import Car
from CarAI import CarAI
from Map import Map
from AI import run

width = 1024
height = 600
pygame.display.set_caption("SuperCarRace")
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
ticks = 60

winner_net = run("assets/config.txt")
