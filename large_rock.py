from asteroid import Asteroid
import random
import math
from medium_rock import RockMed
from small_rock import RockSmall
import arcade

ROCK_SMALL_RADIUS = 2
ROCK_MED_RADIUS = 5
ROCK_LARGE_RADIUS = 15
ROCK_LARGE_SPEED = 1.5


class RockLarge(Asteroid):

    def __init__(self):
        super().__init__("images/rock_large.png")
        self.center.x = random.randint(1, 50)
        self.center.y = random.randint(1, 150)
        self.direction = random.randint(1, 50)
        self.speed = ROCK_LARGE_SPEED
        self.radius = ROCK_LARGE_RADIUS

        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.direction)) * self.speed

    def advance(self):
        self.wrap()  # Check every time advance is called to reduce code redundancy
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        self.angle += 0.25

    def hit(self):
        self.alive = False
        return 14

    def split(self, ship_x, ship_y):
        """
        Splits the large asteroid into 2 medium and 1 small asteroid.
        it returns the new asteroids in a list
        """

        # Tried to look into default/non-default constructors like how you can
        # override in C++. Doesn't look like python likes that. So we just declare
        # each rock and set attributes off of the current/destroyed rock

        # Blank list to add new rocks to
        new_asteroids = []

        # Rock 1 - medium
        new_rock1 = RockMed()
        new_rock1.center.x = self.center.x
        new_rock1.center.y = self.center.y
        new_rock1.velocity.dx = self.velocity.dx
        new_rock1.velocity.dy = self.velocity.dy + 2
        new_asteroids.append(new_rock1)

        # Rock 2 - medium, but change direction
        new_rock2 = RockMed()
        new_rock2.center.x = self.center.x
        new_rock2.center.y = self.center.y
        new_rock2.velocity.dx = self.velocity.dx
        new_rock2.velocity.dy = self.velocity.dy - 2
        new_asteroids.append(new_rock2)

        # Small rock
        new_rock3 = RockSmall()
        new_rock3.center.x = self.center.x
        new_rock3.center.y = self.center.y
        new_rock3.velocity.dy = self.velocity.dy

        # Make sure small rock shoots out the "back"
        # based off ship location
        # Lowered small rock velocity
        if self.center.x > ship_x:
            new_rock3.velocity.dx = self.velocity.dx + 3.5
        else:
            new_rock3.velocity.dx = self.velocity.dx - 3.5

        # Now that direction is decided, add to list
        new_asteroids.append(new_rock3)
        return new_asteroids
