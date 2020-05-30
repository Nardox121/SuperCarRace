import pygame, math
from math import copysign
from pygame.math import Vector2

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
    
    def move(self, dt, pressed, map):
        if pressed[pygame.K_UP]:
            ###############################################################################
            if self.collision(self.position, map) or self.collision(Vector2(self.position.x - 0.5, self.position.y), map):
                if self.velocity.x < 0:
                    self.acceleration = self.brake_deceleration
                else:
                    self.acceleration += 1 * dt
            else:
                self.position = Vector2(self.startPosition.x, self.startPosition.y)
        elif pressed[pygame.K_DOWN]:
            ##########################################################################
            if self.collision(Vector2(self.position.x, self.position.y-self.length), map) or self.collision(Vector2(self.position.x - 0.5, self.position.y-self.length), map):
                if self.velocity.x > 0:
                    self.acceleration = -self.brake_deceleration
                else:
                    self.acceleration -= 1 * dt
            else:
                self.position = Vector2(self.startPosition.x, self.startPosition.y)
        elif pressed[pygame.K_SPACE]:
            if abs(self.velocity.x) > dt * self.brake_deceleration:
                self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
            else:
                self.acceleration = -self.velocity.x / dt
        else:
            ########################################################################################
            if (self.collision(Vector2(self.position.x, self.position.y-self.length), map) or self.collision(Vector2(self.position.x, self.position.y-self.length), map)):
                if abs(self.velocity.x) > dt * self.free_deceleration:
                    self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
                else:
                    if dt != 0:
                        self.acceleration = -self.velocity.x / dt
            else:
                self.position = Vector2(self.startPosition.x, self.startPosition.y)

                        
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

        if pressed[pygame.K_RIGHT]:
            self.steering -= 30 * dt
        elif pressed[pygame.K_LEFT]:
            self.steering += 30 * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

    def collision(self, corner, map):
        tmpCorner = (int(corner.x * 32), int(corner.y * 32))
        
        if tmpCorner in map:
            print(self.length)
            return False
        else:
            return True
