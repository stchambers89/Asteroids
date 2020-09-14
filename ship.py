from flying_object import FlyingObject
import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

import math
SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30


class Ship(FlyingObject):

    def __init__(self):
        super().__init__("images/ship_resize1.png")
        self.angle = 1
        self.center.x = (SCREEN_WIDTH/2)
        self.center.y = (SCREEN_HEIGHT/2)
        self.radius = SHIP_RADIUS

    # Movement Methods
    def left(self):
        self.angle += SHIP_TURN_AMOUNT

    def right(self):
        self.angle -= SHIP_TURN_AMOUNT

    # could use conditional, but I like the way this looks, here's up, and here's down
    def thrust_up(self):
        self.velocity.dx -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    def thrust_down(self):
        self.velocity.dx += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT