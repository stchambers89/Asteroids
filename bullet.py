import arcade
import math
from flying_object import FlyingObject

BULLET_RADIUS = 30
BULLET_LIFE = 60
BULLET_SPEED = 10


class Bullet(FlyingObject):
    def __init__(self, ship_angle, x, y):

        super().__init__("images/laser.png")
        self.radius = BULLET_RADIUS
        self.life = BULLET_LIFE
        self.speed = BULLET_SPEED
        self.angle = ship_angle
        self.center.x = x
        self.center.y = y

    # thank you for the video on this one, it helped out greatly.
    # but to keep the code a bit more clean I rotated the image
    def fire(self):
        self.velocity.dx -= math.sin(math.radians(self.angle)) * BULLET_SPEED
        self.velocity.dy += math.cos(math.radians(self.angle)) * BULLET_SPEED

    # decrease life so bullets die eventually
    def advance(self):
        super().advance()
        self.life = self.life - 1

        if self.life == 0:
            self.alive = False

    def hit(self):
        self.alive = False
