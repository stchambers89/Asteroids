from point import Point
from velocity import Velocity
from abc import ABC
import arcade


SHIP_RADIUS = 30
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class FlyingObject(ABC):

    """Base class for all "flying" objects, this includes all
       attributes/methods that are common between bullets and targets
       constructor expects the image the object will be depicted as.
       this cuts down on redunant code. """

    def __init__(self, image):

        # Status
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True

        # Movement
        self.speed = 1
        self.angle = 1.0
        self.direction = 1

        # Dimensions/View
        self.img = image
        self.texture = arcade.load_texture(self.img)
        self.height = self.texture.height
        self.width = self.texture.width
        self.radius = SHIP_RADIUS

    # Move according to last vector + next
    def advance(self):
        self.wrap()  # Check every time advance is called to reduce code redundancy
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy

    def is_alive(self):
        return self.alive

    # How to draw. For some reason my transparency on my monitor is off.
    # I had to change the draw so I could see.
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height,
                                      self.texture, self.angle, 75)

    def wrap(self):
        """if flying object goes off screen add it to opposite side:
        Right to left, up top to bottom ect."""
        if self.center.x > SCREEN_WIDTH:
            self.center.x -= SCREEN_WIDTH

        if self.center.x < 0:
            self.center.x += SCREEN_WIDTH

        if self.center.y > SCREEN_HEIGHT:
            self.center.y -= SCREEN_HEIGHT

        if self.center.y < 0:
            self.center.y += SCREEN_HEIGHT
