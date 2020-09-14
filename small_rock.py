from asteroid import Asteroid

ROCK_SMALL_RADIUS = 2


class RockSmall(Asteroid):

    def __init__(self):
        super().__init__("images/rock_small.png")
        self.radius = ROCK_SMALL_RADIUS

    def advance(self):
        self.wrap()  # Check every time advance is called to reduce code redundancy
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        self.angle += 0.25

    def hit(self):
        """Kills rock and returns points"""
        self.alive = False
        return 30

    def split(self, ship_x, ship_y):
        new_asteroids = []
        return new_asteroids