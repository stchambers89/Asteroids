"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
import arcade
from ship import Ship
from bullet import Bullet
from large_rock import RockLarge



# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2


class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)

        self.held_keys = set()
        self.score = 0
        self.explode = 0

        # Create: Ship, list of bullets, list of rocks w/ 5 large
        self.ship = Ship()
        self.bullets = []
        self.asteroids = []
        for i in range(INITIAL_ROCK_COUNT):
            large_asteroid = RockLarge()
            self.asteroids.append(large_asteroid)

    # Copy and paste from skeet program to make it a bit more fun
    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=12, color=arcade.color.WHITE)

    # Congrats if you win
    def draw_game_win(self):
        game_text = "YOU WIN! Score: {}".format(self.score)
        start_x = SCREEN_WIDTH / 4
        start_y = SCREEN_HEIGHT * .43
        arcade.draw_text(game_text, start_x=start_x, start_y=start_y, font_size=30, color=arcade.color.WHITE)

    # If you loose...
    def draw_game_loose(self):
        game_text = "YOU CRASHED... \n GAME OVER!"
        start_x = SCREEN_WIDTH * .32
        start_y = SCREEN_HEIGHT * .43
        arcade.draw_text(game_text, start_x=start_x, start_y=start_y, font_size=30, color=arcade.color.WHITE)

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        # clear the screen to begin drawing
        arcade.start_render()
        self.draw_score()

        # Conditionals for what ending credits will say
        if self.ship.is_alive() and len(self.asteroids) == 0:
            self.draw_game_win()
        elif not self.ship.is_alive() and len(self.asteroids) >= 1:
            self.draw_game_loose()

        # Make sure we can see the ship
        self.ship.draw()

        # Look at all em rocks
        for item in self.asteroids:
            item.draw()

        #PewPewLife
        for item in self.bullets:
            item.draw()

    def update(self, delta_time):
        """
        Update each objects in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_collisions()

        # Advance and remove asteroids as needed
        for item in self.asteroids:
            item.advance()
            if not item.is_alive():
                self.asteroids.remove(item)

        # advance and remove bullets as needed
        for item in self.bullets:
            item.advance()
            if not item.is_alive():
                self.bullets.remove(item)

        # Extra will draw ship when alive, or explosion when crashed
        if self.ship.is_alive():
            self.ship.advance()
            self.ship.texture = arcade.load_texture("images/ship_resize1.png")
        elif not self.ship.is_alive():
            self.explode += 1
            self.update_explode(self.explode)

    # Changes the ship png depending on how long it's been dead for
    def update_explode(self, timer):
        if timer <= 20:
            self.ship.texture = arcade.load_texture("images/explode_1.png")
        elif timer <= 40:
            self.ship.texture = arcade.load_texture("images/explode_2.png")
        elif timer <= 60:
            self.ship.texture = arcade.load_texture("images/explode_3.png")
        elif timer <= 85:
            self.ship.texture = arcade.load_texture("images/explode_4.png")
        elif timer <= 100:
            self.ship.texture = arcade.load_texture("images/explode_5.png")
        elif timer < 120:
            self.ship.texture = arcade.load_texture("images/explode_6.png")


    def check_collisions(self):
        """
        Checks to see if bullets have hit targets &
        updates score.
        Pulled from the Skeet assignment and then modified to work here
        """
        for asteroid in self.asteroids:
            # Checking to see if an asteroid will hit our ship
            if self.ship.alive and asteroid.alive:
                ship_too_close = self.ship.radius + asteroid.radius
                if (abs(self.ship.center.x - asteroid.center.x) < ship_too_close
                        and abs(self.ship.center.y - asteroid.center.y) < ship_too_close):
                    # Ship go boom
                    self.ship.alive = False

            # Did bullet hit asteroid
            for bullet in self.bullets:  # Make sure they are both alive before checking for a collision
                if bullet.alive and asteroid.alive:
                    too_close = bullet.radius + asteroid.radius

                    if (abs(bullet.center.x - asteroid.center.x) < too_close and
                            abs(bullet.center.y - asteroid.center.y) < too_close):

                        # its a hit!
                        bullet.hit()
                        self.score += asteroid.hit()
                        # Split the asteroid add new smaller asteroids to the list
                        # add at end: self.asteroids[length:] = asteroid.split(self.ship.center.x, self.ship.center.y)
                        # not sure if this is better but it just seems cleaner in my mind than adding stuff to the front
                        # EDIT: More research shows underlying data structure is a c-array of pointers,
                        # so front or back doesn't really matter. Changed code for simplification
                        self.asteroids[:0] = (asteroid.split(self.ship.center.x, self.ship.center.y))

        # Now, check for anything that is dead, and remove it
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.right()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust_up()

        if arcade.key.DOWN in self.held_keys:
            self.ship.thrust_down()

        # Machine gun mode...
        if arcade.key.SPACE in self.held_keys:
            bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y)
            bullet.fire()
            self.bullets.append(bullet)

    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            # create bullet in accordance to where the ship is
            if key == arcade.key.SPACE:
                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y)
                bullet.fire()
                self.bullets.append(bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()