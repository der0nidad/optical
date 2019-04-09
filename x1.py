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
import json
import math
import sys

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


def reflect(x1, y1, x, y, mirror):
    norm_x = mirror.y1 - mirror.y2
    norm_y = mirror.x2 - mirror.x1
    len_norm = math.sqrt(norm_x ** 2 + norm_y ** 2)
    norm_x /= len_norm
    norm_y /= len_norm
    ai_x = x - x1
    ai_y = y - y1
    s = 2 * (ai_x * norm_x + ai_y * norm_y) / (norm_x * norm_x + norm_y * norm_y)
    norm_x *= s
    norm_y *= s
    ai_x -= norm_x
    ai_y -= norm_y
    len_ai = math.sqrt(ai_x ** 2 + ai_y ** 2)
    return ai_x / len_ai, ai_y / len_ai


def intersect_1(a, b, c, d):
    if a > b:
        b, a = a, b
    if c > d:
        c, d = d, c
    return max(a, c) <= min(b, d)


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


class Mirror:
    def __init__(self, x1, y1, x2, y2, typ, rad):
        # if x1 <= x2:
        #     self.x1 = x1
        #     self.x2 = x2
        # else:
        #     self.x1 = x2
        #     self.x2 = x1
        # if y1 <= y2:
        #     self.y1 = y1
        #     self.y2 = y2
        # else:
        #     self.y1 = y2
        #     self.y2 = y1
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.type = typ  # if type in ['flat', 'curve']
        self.rad = rad  # TODO дописать проверку соответствия радиуса и типа зеркала

    def draw(self):
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


# класс содержит текущий вектор скорости и список уже имеющихся лучей
class RayLine:
    def __init__(self, x, y, x2, y2, mirrors):
        self.segment_list = []
        self.x_0 = x
        self.y_0 = y
        self.vx = x2 - x
        self.vy = y2 - y
        self.count = LINE_NUM
        self.mirrors = mirrors

    #   Считает путь луча
    def calc_ray(self, mirrors):
        x1 = self.x_0
        y1 = self.y_0
        last_mirror = None
        while self.count > 0:
            fl = False
            print('count', self.count)
            for mirror in mirrors:
                if mirror is not last_mirror:
                    # print(x1, y1, x1 + self.vx, y1 + self.vy, mirror.x1, mirror.y1, mirror.x2, mirror.y2)
                    prs, x, y = intersect(x1, y1, x1 + self.vx * 400, y1 + self.vy * 400, mirror.x1, mirror.y1,
                                          mirror.x2, mirror.y2)
                    # print(prs, x, y)
                    if prs:
                        print(last_mirror, last_mirror == mirror)

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
                ray = Segment(x1, y1, x1 + self.vx * 3000, y1 + self.vy * 3000)
                self.segment_list.append(ray)
                print(ray, '|', len(self.segment_list))
                return
                # self.count = 0

    def draw(self):
        for ray in self.segment_list:
            ray.draw()


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.shape_list = None
        self.mirror_list = None
        self.ray_creation_flag = False
        self.mirror_creation_flag = False
        self.click_flag = False
        self.continious_flag = False
        self.prev_coords_x = None
        self.prev_coords_y = None
        self.filename = 'Optical'
        self.ray = RayLine(620, 180, 200, -700, self.mirror_list)

    def get_mirrors(self):
        return self.mirror_list

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.shape_list = []
        self.mirror_list = []
        coord_list = [(50, 50, 75, 400), (75, 400, 100, 40), (400, 20, 450, 500), (750, 80, 400, 20),
                      # (100, 60, 750, 60)
                      (450, 500, 750, 80)]
        for c in coord_list:
            mirror = Mirror(c[0], c[1], c[2], c[3], 'flat', 0)
            self.mirror_list.append(mirror)
        if self.ray:
            self.ray.calc_ray(self.get_mirrors())

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
        if self.ray:
            self.ray.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        # arcade.window_commands.pause

        if self.click_flag:
            if self.mirror_creation_flag:
                mirror = Mirror(self.prev_coords_x, self.prev_coords_y, x, y, 'flat', 0)
                self.mirror_list.append(mirror)
                self.prev_coords_x = x
                self.prev_coords_y = y
                if self.continious_flag:
                    self.click_flag = True
                else:
                    self.click_flag = False
            elif self.ray_creation_flag:
                self.ray = RayLine(self.prev_coords_x, self.prev_coords_y, x, y, self.mirror_list)
                self.ray.calc_ray(self.mirror_list)
                self.click_flag = False
        else:
            if self.continious_flag:
                mirror = Mirror(self.prev_coords_x, self.prev_coords_y, x, y, 'flat', 0)
                self.mirror_list.append(mirror)
            self.click_flag = True
            self.prev_coords_x = x
            self.prev_coords_y = y
        # print(x, y)

    def on_key_press(self, symbol: int, modifiers: int):
        print(symbol, modifiers)
        if symbol == 112:  # p
            arcade.pause(2)
        elif symbol == 109:  # m
            self.click_flag = False
            self.mirror_creation_flag = True
            self.ray_creation_flag = False
        elif symbol == 100:  # d
            pass
        elif symbol == 101:  # e
            pass
        elif symbol == 114:  # r
            self.click_flag = False
            self.continious_flag = False
            self.ray_creation_flag = True
            self.mirror_creation_flag = False
        elif symbol == 111:  # o - непрерывное создание зеркал
            self.continious_flag = not self.continious_flag
            print('Continious flag current value:', self.continious_flag)
        elif symbol == 97:  # a - delete all
            self.mirror_list = []
            self.ray = None
        elif symbol == 115:  # s - save to json
            json_content = self.serialize()
            self.save_to_file(str(self.filename) + '.json', json_content)
        elif symbol == 108:  # l - load from json. rewrite current room
            pass
        elif symbol == 113:  # q - exit
            print('bye')
            sys.exit(0)

    def serialize(self):
        return {'cool_game_key': 'ты пидор'}

    def save_to_file(self, filename, json_content):
        with open(filename, 'w') as f:
            json.dump(json_content, f)
        print('saved')


def main():
    window = MyGame()
    window.setup()
    arcade.set_background_color(arcade.color.BLACK)

    arcade.run()


if __name__ == "__main__":
    main()
