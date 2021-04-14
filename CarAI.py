import pygame, math
from math import copysign
from pygame.math import Vector2
from Car import Car, Action
from Map import MapTile
from pygame import draw,color
from bresenham import bresenham

class CarAI (Car):
    def __init__(self, x, y, angle = 90, length = 0.5, max_steering = 15, max_acceleration= 2.5):
        self.startPosition = Vector2(x, y)
        self.position = Vector2(self.startPosition.x, self.startPosition.y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 2.5
        self.brake_deceleration = 3
        self.free_deceleration = 2

        self.acceleration = 0.0
        self.steering = 0.0
        self.distances = [0 for x in range(6)]
        self.dead = False

    def update_dist(self, screen, gameMap):
        angles = [x for x in range(0, 360, 60)]
        for i in range(6):
            self.distances[i] = self.normalize(self.calculate_dist(self.angle + angles[i], screen, gameMap))

    def calculate_dist(self, angle, screen, gameMap):
        # Normalize it to 0-360 range
        angle = round(angle % 360)

        #position of the center point of our car
        x = int(self.position.x*32)
        y = int(self.position.y*32)
        
        dist = 0

        #edge cases where tan returns 0 or is not defined
        if angle == 0 or angle == 360:
            while gameMap[y][x] != MapTile.WALL and dist < 150:
                dist += 1
                x += 1
        elif angle == 90:
            while gameMap[y][x] != MapTile.WALL and dist < 150:
                dist += 1
                y -= 1
        elif angle == 180:
            while gameMap[y][x] != MapTile.WALL and dist < 150:
                dist += 1
                x -= 1
        elif angle == 270:
            while gameMap[y][x] != MapTile.WALL and dist < 150:
                dist += 1
                y += 1
        else:
            a = math.tan(angle / 180 * math.pi)

            points = []
            if 0 < angle < 90:
                points = list(bresenham(x, y, x + 150, round(y - a * 150)))
            elif 90 < angle < 180:
                points = list(bresenham(x, y, x - 150, round(y + a * 150)))
            elif 180 < angle < 270:
                points = list(bresenham(x, y, x - 150, round(y + a * 150)))
            elif 270 < angle < 360:            
                points = list(bresenham(x, y, x + 150, round(y - a * 150)))
            for point in points:
                if dist > 150 or (1024, 600) < point < (0, 0):
                    break
                
                if gameMap[y][x] == MapTile.WALL:
                    break

                x, y = point
                dist = math.sqrt((self.position.x * 32 - x)**2 + (self.position.y * 32 - y)**2)

        pygame.draw.circle(screen, pygame.Color(0, 0, 0), (int(x),int(y)), 3)
        return dist

    def normalize(self, value):
        if value < 0:
            value = 0
        if value > 150:
            value = 150
        return value / 150
    
    def move(self, dt, output):
        par = 0.5
        ######### UP #############
        if output[0] > par:
            self.takeAction(Action.Accelerate, dt)
        ######### DOWN ###########
        elif output[1] > par:
            self.takeAction(Action.Reverse, dt)
        else:
            self.takeAction(Action.Decelerate, dt)

        ######## RIGHT & LEFT #########
        if output[2] > par:
            self.takeAction(Action.TurnRight, dt)
        elif output[3] > par:
            self.takeAction(Action.TurnLeft, dt)
        else:
            self.takeAction(Action.GoStraight, dt)
            
    def checkCollision(self, rect, gameMap):
        if(self.isColliding(rect, gameMap, MapTile.WALL)):
            self.dead = True
            return True
        return False
        
    def isAwarded(self, rect, gameMap):
        if(self.isColliding(rect, gameMap, MapTile.REWARD)):
            return True
        return False
