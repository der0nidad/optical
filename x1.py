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
LINE_NUM = 30


class Mirror:
    def __init__(self, x1, y1, x2, y2, typ, rad):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.type = typ  # if type in ['flat', 'curve']
        self.rad = rad  # TODO дописать проверку соответствия радиуса и типа зеркала

    def draw(self):
        # if type == 'flat':
        arcade.draw_line(self.x1, self.y1, self.x2, self.y2, arcade.color.WHITE, 3)


class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return 'Segment ' + str(self.x1) + ' ' + str(self.y1) + ' ' + str(self.x2) + ' ' + str(self.y2)

    def draw(self):
        arcade.draw_line(self.x1, self.y1, self.x2, self.y2, arcade.color.BRIGHT_GREEN, 1)


def reflect(x1, y1, x, y, mirror):
    norm_x = mirror.y1 - mirror.y2
    norm_y = mirror.x2 - mirror.x1
    ai_x = x - x1
    ai_y = y - y1
    s = (2 * ai_x * norm_x + ai_y * norm_y) / (norm_x * norm_x + norm_y * norm_y)
    norm_x *= -s
    norm_y *= -s
    ai_x += norm_x
    ai_y += norm_y
    len_ai = math.sqrt(ai_x ** 2 + ai_y ** 2)
    return ai_x / len_ai, ai_y / len_ai


# класс содержит текущий вектор скорости и список уже имеющихся лучей
class RayLine:
    def __init__(self, x, y, vx, vy, mirrors):
        self.segment_list = []
        self.vx = vx - x
        self.vy = vy - y
        self.count = LINE_NUM
        self.mirrors = mirrors
        # self.calc_ray(x, y, self.mirrors)

    #   Добавляет луч в список. Обновляет текущий вектор скорости луча
    def calc_ray(self, x0, y0, mirrors):
        x1 = x0
        y1 = y0
        last_mirror = None
        while self.count > 0:
            fl = False
            print('count', self.count)
            for mirror in mirrors:
                print('--')
                if mirror is not last_mirror:
                    print(last_mirror)
                    # print(x1, y1, x1 + self.vx, y1 + self.vy, mirror.x1, mirror.y1, mirror.x2, mirror.y2)
                    prs, x, y = intersect(x1, y1, x1 + self.vx * 300, y1 + self.vy * 300, mirror.x1, mirror.y1,
                                          mirror.x2, mirror.y2)
                    print(prs, x, y)
                    if prs:
                        ray = Segment(x1, y1, x, y)
                        self.segment_list.append(ray)

                        ai_x, ai_y = reflect(x1, y1, x, y, mirror)
                        self.vx = ai_x
                        self.vy = ai_y

                        x1 = x
                        y1 = y
                        last_mirror = mirror
                        fl = True
                        self.count -= 1
                        break
            if not fl:
                ray = Segment(x1, y1, x1 + self.vx * 300, y1 + self.vy * 300)
                self.segment_list.append(ray)
                print(ray, '|', len(self.segment_list))
                return
                # self.count = 0

    def draw(self):
        for ray in self.segment_list:
            ray.draw()


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
            norm_x = mirror.y1 - mirror.y2
            norm_y = mirror.x2 - mirror.x1
            ai_x = x - self.x
            ai_y = y - self.y
            print('d', (self.delta_x, self.delta_y), self.delta_x / self.delta_y, 'n', (ai_x, ai_y), ai_x / ai_y)
            s = (2 * ai_x * norm_x + ai_y * norm_y) / (norm_x * norm_x + norm_y * norm_y)
            norm_x *= -s
            norm_y *= -s
            ai_x += norm_x
            ai_y += norm_y
            new_x = x + ai_x
            new_y = y + ai_y

            len_ai = math.sqrt(ai_x ** 2 + ai_y ** 2)
            v_x = ai_x / len_ai
            v_y = ai_y / len_ai
            print('okd sp', self.delta_x, self.delta_y, 'new_sp', v_x, v_y)
            # self.delta_x = v_x
            # self.delta_y = v_y
            print(self.x, self.y, '*', x, y, '*', ai_x, ai_y, '*', new_x, new_y, self.delta_y)
            self.delta_y *= -1
        return new_x, new_y

        # print('norm', norm_x, norm_y, 'ai', ai)
        # print(x, y)
        # print("УРААА ПЕРЕССЕСЕСЕШЕНЬЕ")

    def reflect(self, new_x, new_y, mirror):  # надо найти ближайший луч, точку пересечения и отразить.
        pass

    def move(self):
        # curr_time = timeit.default_timer()
        # delta_t = float(curr_time - self.last_time)
        # self.last_time = curr_time
        delta_t = 1
        new_x = self.x + self.delta_x * delta_t
        new_y = self.y + self.delta_y * delta_t
        for mirror in self.mirrors:
            if check_intersect(self.x, self.y, new_x, new_y, mirror.x1, mirror.y1, mirror.x2, mirror.y2):
                new_x, new_y = self.check_reflection(new_x, new_y, mirror)
        # for mirror in self.mirrors:
        #     self.check_reflection(new_x, new_y, mirror)

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


def between(a, b, c, ):
    return min(a, b) <= c + EPS and c <= max(a, b) + EPS


def intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    A1, B1 = y1 - y2, x2 - x1
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
               intersect_1(x1, x2, x3, x4) and \
               intersect_1(y1, y2, y3, y4), None, None


class Ray_temp(RayElem):
    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.radius, self.color)

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.shape_list = None
        self.mirror_list = None
        self.ray_creation_flag = False
        self.ray_coords_x = None
        self.ray_coords_y = None
        self.ray = RayLine(620, 80, 1000, 60, self.mirror_list)

    def get_mirrors(self):
        return self.mirror_list

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.shape_list = []
        self.mirror_list = []
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

        mirror = Mirror(600, 20, 650, 200, 'flat', 0)
        self.mirror_list.append(mirror)
        mirror = Mirror(600, 20, 750, 80, 'flat', 0)
        self.mirror_list.append(mirror)
        mirror = Mirror(750, 80, 650, 200, 'flat', 0)
        self.mirror_list.append(mirror)
        self.ray.calc_ray(620, 80, self.get_mirrors())

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
        self.ray.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """

        if self.ray_creation_flag:
            for i in range(0, 2, 2):
                treshold = 150
                red = random.randrange(56) + treshold
                green = random.randrange(56) + treshold
                blue = random.randrange(56) + treshold
                alpha = random.randrange(56) + treshold
                diff_x = x - self.ray_coords_x
                diff_y = y - self.ray_coords_y
                angle = math.atan2(diff_x, diff_y)
                radius = 5
                print('DIFы', diff_x, diff_y, angle)
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
