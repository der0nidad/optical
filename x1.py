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
NUMBER_OF_MIRRORS = 1  # 200
SPEED_COEF = 0.03
EPS = 10 ** (-9)


class Mirror:
    def __init__(self, x1, y1, x2, y2, type, rad):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.type = type  # if type in ['flat', 'curve']
        self.rad = rad  # TODO дописать проверку соответствия радиуса и типа зеркала

    def draw(self):
        # if type == 'flat':
        arcade.draw_line(self.x1, self.y1, self.x2, self.y2, arcade.color.WHITE, 3)


class RayElem:

    def __init__(self, x, y, radius, width, height, angle, delta_x, delta_y,
                 delta_angle, color, mirrors):
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
        self.mirrors = mirrors

    def check_reflection(self, new_x, new_y, mirror):

        prs, x, y = intersect(self.x, self.y, new_x, new_y, mirror.x1, mirror.y1, mirror.x2, mirror.y2)
        if prs:
            print(x, y)
            # print("УРААА ПЕРЕССЕСЕСЕШЕНЬЕ")
            pass

    def reflect(self, new_x, new_y, mirror): # надо найти ближайший луч, точку пересечения и отразить.
        pass

    def move(self):
        # curr_time = timeit.default_timer()
        # delta_t = float(curr_time - self.last_time)
        # self.last_time = curr_time
        delta_t = 1
        new_x = self.x + self.delta_x * delta_t
        new_y = self.y + self.delta_y * delta_t
        for mirror in self.mirrors:
            self.check_reflection(new_x, new_y, mirror)
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

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        # arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
        #                              self.color, self.angle)


def intersect_1(a, b, c, d):
    if a > b:
        b, a = a, b
    if c > d:
        c, d = d, c
    return max(a, c) <= min(b, d)


def area(x1, y1, x2, y2, x3, y3):
    return (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)


def check_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    return intersect_1(x1, x2, x3, x4) \
           and intersect_1(y1, y2, y3, y4) \
           and area(x1, y1, x2, y2, x3, y3) * area(x1, y1, x2, y2, x4, y4) <= 0 \
           and area(x3, y3, x4, y4, x1, y1) * area(x3, y3, x4, y4, x2, y2) <= 0


def det(a, b, c, d):
    return a * d - b * c


def between(a, b, c,):
    return min(a, b) <= c + EPS and c <= max(a, b) + EPS


def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    A1, B1= y1 - y2, x2 - x1
    C1 = -A1 * x1 - B1 * y1
    A2, B2 = y3 - y4, x4 - x3
    C2 = -A2 * x3 - B2 * y3
    zn = det(A1, B1, A2, B2)
    if zn:
        x = -det(C1, B1, C2, B2) * 1. / zn
        y = - det(A1, C1, A2, C2) * 1. / zn
        return between(x1, x2, x) and between(y1, y2, y) and between(x3, x4, x) and between(y3, y4, y), x, y
    else:
        return det(A1, C1, A2, C2) == 0 and \
               det(B1, C1, B2, C2) == 0 and \
               intersect_1(x1, x2, x3, x4) and\
               intersect_1(y1, y2, y3, y4), None, None

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


class Ellipse(RayElem):

    def draw(self):
        arcade.draw_ellipse_filled(self.x, self.y, self.width, self.height,
                                   self.color, self.angle)


class Rectangle(RayElem):

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
                                     self.color, self.angle)


class Ray_temp(RayElem):

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)
        # arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height,
        #                              self.color, self.angle)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.shape_list = None
        self.mirror_list = None
        self.ray_creation_flag = False
        self.ray_coords_x = None
        self.ray_coords_y = None

    def get_mirrors(self):
        return self.mirror_list

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.shape_list = []
        self.mirror_list = []

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
        mirror = Mirror(50, 50, 75, 400, 'flat', 0)
        self.mirror_list.append(mirror)
        mirror = Mirror(75, 400, 100, 40, 'flat', 0)
        self.mirror_list.append(mirror)
        mirror = Mirror(450, 450, 530, 500, 'flat', 0)
        self.mirror_list.append(mirror)
        mirror = Mirror(530, 500, 600, 480, 'flat', 0)
        self.mirror_list.append(mirror)
        mirror = Mirror(600, 480, 450, 450, 'flat', 0)
        self.mirror_list.append(mirror)
        mirror = Mirror(750, 80, 650, 200, 'flat', 0)
        self.mirror_list.append(mirror)
        mirror = Mirror(600, 20, 750, 80, 'flat', 0)
        self.mirror_list.append(mirror)

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
        for mirror in self.mirror_list:
            mirror.draw()
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        # arcade.window_commands.pause

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

                ray = RayElem(self.ray_coords_x + math.sin(angle) * i, self.ray_coords_y + math.cos(angle) * i, radius,
                              self.ray_coords_x + 2 * radius,
                              self.ray_coords_y + 2 * radius, angle, diff_x, diff_y, 0, (red, green, blue, alpha),
                              self.mirror_list)
                self.shape_list.append(ray)
            self.ray_creation_flag = False
        else:
            self.ray_creation_flag = True
            self.ray_coords_x = x
            self.ray_coords_y = y
        print(x, y)

    def on_key_press(self, symbol: int, modifiers: int):
        print(symbol, modifiers)
        if symbol == 112:
            arcade.pause(2)


def main():
    window = MyGame()
    window.setup()
    arcade.set_background_color(arcade.color.BLACK)

    arcade.run()


if __name__ == "__main__":
    main()
