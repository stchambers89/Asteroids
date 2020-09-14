from flying_object import FlyingObject
from abc import ABC, abstractmethod

ROCK_MED_RADIUS = 5
ROCK_LARGE_RADIUS = 15
ROCK_LARGE_SPEED = 1.5


class Asteroid(FlyingObject):

    # Important to have image passed in both constructors.
    # The parent needs the image, but it is not defined here,
    # so we tell it that they will find the img path in the next child class.
    def __init__(self, image):
        super().__init__(image)
        self.radius = ROCK_LARGE_RADIUS

    @abstractmethod
    def hit(self):
        pass
