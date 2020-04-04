import pygame, math

class Car:
    def __init__(self, xpos, ypos, w, h):
        self.car = pygame.Rect(xpos, ypos, 20,20)
        self.speed = 5
        self.screenWidth = w - 20
        self.screenHeight = h - 20

    def moveUp(self):
        if self.car.y > 1:
            self.car.y -= self.speed
        
    def moveDown(self):
        if self.car.y < self.screenHeight:
            self.car.y += self.speed

    def moveRight(self):
        if self.car.x < self.screenWidth:
            self.car.x += self.speed

    def moveLeft(self):
        if self.car.x > 1:
            self.car.x -= self.speed


    def getCar(self):
        return self.car