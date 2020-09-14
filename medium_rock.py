from asteroid import Asteroid
from small_rock import RockSmall
import random
import math
import arcade

ROCK_MED_RADIUS = 5


class RockMed(Asteroid):

    def __init__(self):
        super().__init__("images/rock_med.png")
        self.radius = ROCK_MED_RADIUS


    def advance(self):
        self.wrap()  # Check every time advance is called to reduce code redundancy
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        self.angle += 0.25

    def hit(self):
        self.alive = False
        return 18

    def split(self, ship_x, ship_y):
        """
        Splits the large asteroid into 2 medium and 1 small asteroid.
        it returns the new asteroids in a list
        """

        new_asteroids = []

        # create small rock #1
        new_rock1 = RockSmall()
        new_rock1.center.x = self.center.x
        new_rock1.center.y = self.center.y
        new_rock1.velocity.dx = self.velocity.dx
        new_rock1.velocity.dy = self.velocity.dy + 2
        new_asteroids.append(new_rock1)

        # small rock #3 in opposite direction
        new_rock2 = RockSmall()
        new_rock2.center.x = self.center.x
        new_rock2.center.y = self.center.y
        new_rock2.velocity.dx = self.velocity.dx
        new_rock2.velocity.dy = self.velocity.dy - 2
        new_asteroids.append(new_rock2)

        return new_asteroids