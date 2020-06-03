import pygame, math
from math import copysign
from pygame.math import Vector2
from Car import Car, Action
from Map import MapTile
from pygame import draw,color

class CarAI (Car):
    def __init__(self, x, y, angle = 89.9, length = 0.5, max_steering = 15, max_acceleration= 2.5):
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
        angles = [0, 45, -45, +90, -90, -180]
        a = [0]*6
        for i in range(6):
            a[i]=math.tan((self.angle+90+angles[i])/180*math.pi)
        for i in range(6):
            self.distances[i] = self.calculate_dist(a[i], self.angle+angles[i], screen, gameMap)
        for i in range(6):
            self.distances[i] = self.normalize(self.distances[i])
        print(self.distances)

    def calculate_dist(self, a, angle, screen, gameMap):
        if angle<0:
            angle+=1080
        if angle>=360:
            angle=angle%360
        if angle<90 and angle>=0:
            quarter = 2
        elif angle<180 and angle>=90:
            quarter = 3
        elif angle<270 and angle>=180:
            quarter = 4
        else:
            quarter = 1

        x=int(self.position.x*32)
        y=int(self.position.y*32)
        count=0
        if a==0:
            a=0.001
        if quarter == 1 and a<1:
            a=1/a
            while x<len(gameMap) and y<len(gameMap[0]) and gameMap[y][x]!=MapTile.WALL :
                x+=1
                count+=1
                y+=math.floor(count/a)
                if count>=math.ceil(abs(a)):
                    count=0
        elif quarter == 1 and a>=1:
            while x<len(gameMap) and y<len(gameMap) and gameMap[y][x]!=MapTile.WALL :
                x+=1
                count+=1
                y+=math.floor(count/a)
                if count>math.ceil(abs(a)):
                    count=0
        elif quarter == 2 and a>-1:
            a=1/a
            while x<len(gameMap) and y>0 and gameMap[y][x]!=MapTile.WALL :
                y-=1
                count+=1
                x-=math.ceil(count/a)
                if count>math.ceil(abs(a)):
                    count=0
        elif quarter == 2 and a<=-1:
            while x<len(gameMap) and y>0 and gameMap[y][x]!=MapTile.WALL :
                x+=1
                count+=1
                y+=math.ceil(count/a)
                if count>math.ceil(abs(a)):
                    count=0
        elif quarter == 3 and a<1:
            a=1/a
            while x>0 and y>0 and gameMap[y][x]!=MapTile.WALL :
                x-=1
                count+=1
                y-=math.floor(count/a)
                if count>math.ceil(abs(a)):
                    count=0
        elif quarter == 3 and a>=1:
            while x>0 and y>0 and gameMap[y][x]!=MapTile.WALL :
                x-=1
                count+=1
                y-=math.floor(count/a)
                if count>math.ceil(abs(a)):
                    count=0
        elif quarter == 4 and a>-1:
            a=1/a
            while y>0 and x<len(gameMap[0]) and gameMap[y][x]!=MapTile.WALL :
                y+=1
                count+=1
                x-=math.ceil(count/a)
                if count>math.ceil(abs(a)):
                    count=0
        elif quarter == 4 and a<=-1:
            while x>0 and y<len(gameMap[0]) and gameMap[y][x]!=MapTile.WALL :
                x-=1
                count+=1
                y-=math.ceil(count/a)
                if count>math.ceil(abs(a)):
                    count=0
        pygame.draw.circle(screen, pygame.Color(255, 0, 0), (int(x),int(y)), 3)
        return (math.sqrt((self.position.x*32-x)**2+(self.position.y*32-y)**2))

    def normalize(self, value):
        if value < 0:
            value = 0
        if value > 200:
            value = 200
        return value / 200
    

    """def move(self, dt, output):
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
            self.takeAction(Action.GoStraight, dt)"""
