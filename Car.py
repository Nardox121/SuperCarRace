import pygame, math

class Car:
    def __init__(self, xpos, ypos):
        self.car = pygame.Rect(xpos, ypos, 20, 20)

    def moveUp(self):
        self.car.y -= 2
        
    def moveDown(self):
        self.car.y += 2

    def moveRight(self):
        self.car.x += 2

    def moveLeft(self):
        self.car.x -= 2


    def getCar(self):
        return self.car