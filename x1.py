"""
This simple animation example shows how to use classes to animate
multiple objects on the screen at the same time.

Because this is redraws the shapes from scratch each frame, this is SLOW
and inefficient.

Using buffered drawing commands (Vertex Buffer Objects) is a bit more complex,
but faster.

See http://arcade.academy/examples/index.html#shape-lists for some examples.

Also, any Sprite class put in a SpriteList and drawn with the SpriteList will
be drawn using Vertex Buffer Objects for better performance.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.shapes
"""
import math
import random
import timeit

import arcade

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Shapes!"

RECT_WIDTH = 50
RECT_HEIGHT = 50

NUMBER_OF_SHAPES = 0  # 200
SPEED_COEF = 0.03



class Shape:

    def __init__(self, x, y, radius, width, height, angle, delta_x, delta_y,
                 delta_angle, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.width = width
        self.height = height
        self.angle = angle
        self.delta_x = delta_x * SPEED_COEF
        self.delta_y = delta_y * SPEED_COEF
        self.delta_angle = delta_angle
        self.color = color
        self.last_time = timeit.default_timer()

    def move(self):
        # curr_time = timeit.default_timer()
        # delta_t = float(curr_time - self.last_time)
        # self.last_time = curr_time
        delta_t = 1
        new_x = self.x + self.delta_x * delta_t
        new_y = self.y + self.delta_y * delta_t
        if new_x > SCREEN_WIDTH:
            self.delta_x *= -1
            self.x = 2 * SCREEN_WIDTH - new_x
        elif new_x < 0:
            self.delta_x *= -1
            self.x = -new_x
        else:
            self.x = new_x
        if new_y > SCREEN_HEIGHT:
            self.delta_y *= -1
            self.y = 2 * SCREEN_HEIGHT + self.delta_y - self.y
        elif new_y < 0:
            self.delta_y *= -1
            self.y = - new_y
        else:
            self.y = new_y

        # self.x += self.delta_x
        # self.y += self.delta_y
        # self.angle += self.delta_angle




    # def move(self):
    # new_x = self.x + self.delta_x
    # new_y = self.y + self.delta_y
    # if new_x > SCREEN_HEIGHT:
    #     self.x = SCREEN_HEIGHT - self.delta_x
    #     self.angle += 90
    # else:
    #     self.x += self.delta_x
    # if new_y > SCREEN_WIDTH:
    #     self.y = SCREEN_WIDTH - self.delta_y
    #     self.angle += 90
    #
    # else:
    #     self.y += self.delta_y
    #
    # self.angle += self.delta_angle
    # self.angle = self.angle % 160
class Ellipse(Shape):

    def draw(self):
        arcade.draw_ellipse_filled(self.x, self.y, self.width, self.height,
                                   self.color, self.angle)


class Rectangle(Shape):

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
                                     self.color, self.angle)


class Ray(Shape):

    def draw(self):
        arcade.draw_circle_filled(self.x , self.y , self.radius, self.color)
        # arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
        #                              self.color, self.angle)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.shape_list = None
        self.ray_creation_flag = False
        self.ray_coords_x = None
        self.ray_coords_y = None

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.shape_list = []

        for i in range(NUMBER_OF_SHAPES):
            x = random.randrange(0, SCREEN_WIDTH)
            y = random.randrange(0, SCREEN_HEIGHT)
            width = random.randrange(10, 30)
            height = random.randrange(10, 30)
            angle = random.randrange(0, 360)

            d_x = random.randrange(-3, 4)
            d_y = random.randrange(-3, 4)
            d_angle = random.randrange(-3, 4)

            red = random.randrange(256)
            green = random.randrange(256)
            blue = random.randrange(256)
            alpha = random.randrange(256)

            shape_type = random.randrange(2)

            if shape_type == 0:
                shape = Rectangle(x, y, width, height, angle, d_x, d_y,
                                  d_angle, (red, green, blue, alpha))
            else:
                shape = Ellipse(x, y, width, height, angle, d_x, d_y,
                                d_angle, (red, green, blue, alpha))
            self.shape_list.append(shape)

    def update(self, dt):
        """ Move everything """

        for shape in self.shape_list:
            shape.move()

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        for shape in self.shape_list:
            shape.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        if self.ray_creation_flag:
            # print('!!', self.ray_creation_flag, self.ray_coords_x, self.ray_coords_y)
            # sys.exit(0)

            for i in range(0, 100, 2):
                treshold = 150
                red = random.randrange(56) + treshold
                green = random.randrange(56) + treshold
                blue = random.randrange(56) + treshold
                alpha = random.randrange(56) + treshold
                diff_x = x - self.ray_coords_x
                diff_y = y - self.ray_coords_y
                angle = math.atan2(diff_x, diff_y)
                # diff_x *= 0.3
                # diff_y *= 0.3
                radius = 5
                print('DIFы', diff_x, diff_y, angle)

                # ray = Ray(self.ray_coords_x, self.ray_coords_y, width, height, angle, diff_x, diff_y,
                #           0, (red, green, blue, alpha))

                ray = Ray(self.ray_coords_x + math.sin(angle) * i , self.ray_coords_y + math.cos(angle) * i, radius, self.ray_coords_x +2 * radius,
                          self.ray_coords_y + 2 * radius, angle, diff_x, diff_y, 0, (red, green, blue, alpha))
                self.shape_list.append(ray)
            self.ray_creation_flag = False
        else:
            self.ray_creation_flag = True
            self.ray_coords_x = x
            self.ray_coords_y = y
        print(x, y)


def main():
    window = MyGame()
    window.setup()
    arcade.set_background_color(arcade.color.BLACK)

    arcade.run()


if __name__ == "__main__":
    main()