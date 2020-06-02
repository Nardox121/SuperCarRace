import pygame, math
from math import copysign
from pygame.math import Vector2
from enum import Enum

class Car:
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

    def update(self, dt):
        self.velocity += (self.acceleration * dt, 0)
        self.velocity.x = max(-self.max_velocity, min(self.velocity.x, self.max_velocity))

        if self.steering:
            turning_radius = self.length / math.sin(math.radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0

        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += math.degrees(angular_velocity) * dt
    
    def move(self, dt, pressed):
        if pressed[pygame.K_UP]:
            self.takeAction(Action.Accelerate, dt)
        elif pressed[pygame.K_DOWN]:
            self.takeAction(Action.Reverse, dt)
        else:
            self.takeAction(Action.Decelerate, dt)

        if pressed[pygame.K_RIGHT]:
            self.takeAction(Action.TurnRight, dt)
        elif pressed[pygame.K_LEFT]:
            self.takeAction(Action.TurnLeft, dt)
        else:
            self.takeAction(Action.GoStraight, dt)

    def takeAction(self, action, dt):
        if action == Action.Accelerate:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += 1 * dt

        elif action == Action.Reverse:
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= 1 * dt

        elif action == Action.Decelerate:
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity.x / dt
        
        elif action == Action.TurnRight:
            self.steering -= 45 * dt
        
        elif action == Action.TurnLeft:
            self.steering += 45 * dt

        elif action == Action.GoStraight:
            self.steering = 0

        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

    # def collision(self, rect, map):
    #     carRec = pygame.Rect(self.position.x * 32, self.position.y * 32, 5, 5)
    #     if(carRec.collidelist(map) > -1):
    #         self.position.x, self.position.y = self.startPosition.x, self.startPosition.y
    #         self.angle = 90
    #         self.velocity = Vector2(0.0, 0.0)

class Action(Enum):
    Accelerate = 1
    Decelerate = 2
    Reverse = 3
    TurnLeft = 4
    TurnRight = 5
    GoStraight = 6
