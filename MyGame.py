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

import Mirror
import RayLine

# Set up the constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Optical!"

RECT_WIDTH = 50
RECT_HEIGHT = 50

NUMBER_OF_SHAPES = 0  # 200
NUMBER_OF_MIRRORS = 1  # 200
SPEED_COEF = 0.03

LINE_NUM = 300


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.mirror_list = None
        self.ray = None
        self.prev_coords_y = None
        self.prev_coords_x = None
        self.filename = 'Optical'
        self.win_circle = None

        self.ray_creation_flag = False
        self.mirror_creation_flag = False
        self.click_flag = False
        self.continious_flag = False
        self.win_flag = False
        self.win_click_flag = False
        self.mirror_delete_flag = False

    def get_mirrors(self):
        return self.mirror_list

    def setup(self):
        """ Set up the game and initialize the variables. """
        self.mirror_list = []
        coord_list = [(50, 50, 75, 400), (75, 400, 100, 40), (400, 20, 450, 500), (750, 80, 400, 20),
                      # (100, 60, 750, 60)
                      (450, 500, 750, 80)]
        for c in coord_list:
            mirror = Mirror.Mirror(c[0], c[1], c[2], c[3], 'flat', 0)
            self.mirror_list.append(mirror)
        if self.ray:
            self.ray.calc_ray(self.get_mirrors())

        self.win_circle = (507, 245, 20)

    # def update(self, dt):
    #     """ Move everything """
    #     pass

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        if self.win_flag:
            arcade.draw_text("You win. Contact with us to get your prize",
                             SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, arcade.color.WHITE, 14, width=200,
                             align="center")

        else:
            for mirror in self.mirror_list:
                mirror.draw(self.mirror_delete_flag)
            if self.ray:
                self.ray.draw()
            if self.win_circle:
                arcade.draw_circle_filled(self.win_circle[0], self.win_circle[1], self.win_circle[2],
                                          arcade.color.BRANDEIS_BLUE)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        # ro = abs(A * x0 + B * y0 + C) / math.sqrt(A * A + B * B)
        # arcade.window_commands.pause

        if self.click_flag:
            if self.mirror_creation_flag:
                mirror = Mirror.Mirror(self.prev_coords_x, self.prev_coords_y, x, y, 'flat', 0)
                self.mirror_list.append(mirror)
                self.prev_coords_x = x
                self.prev_coords_y = y
                if self.continious_flag:
                    self.click_flag = True
                else:
                    self.click_flag = False
            elif self.ray_creation_flag:
                self.ray = RayLine.RayLine(self.prev_coords_x, self.prev_coords_y, x, y, self.mirror_list, LINE_NUM,
                                           self.win_circle)
                # self.ray.calc_ray(self.mirror_list)
                self.click_flag = False
        else:
            if self.win_click_flag:
                self.win_circle = (x, y, 20)
            elif self.continious_flag:
                mirror = Mirror.Mirror(self.prev_coords_x, self.prev_coords_y, x, y, 'flat', 0)
                self.mirror_list.append(mirror)
            elif self.mirror_delete_flag:
                for ind, m in enumerate(self.mirror_list):
                    A = m.y2 - m.y1  # y2 - y1
                    B = m.x1 - m.x2  # x1 - x2
                    C = m.y1 * m.x2 - m.x1 * m.y2  # y1 * x2 - x1 * y2
                    distance = abs(A * x + B * y + C) / math.sqrt(A * A + B * B)
                    # print('DIST', distance, ind)
                    if distance < 4: # magic constant
                        self.mirror_list = self.mirror_list[:ind] + self.mirror_list[ind+1:]
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
            self.win_click_flag = False
            self.mirror_delete_flag = False
        elif symbol == 100:  # d
            self.mirror_delete_flag = True
            self.mirror_creation_flag = False
            self.win_click_flag = False
            self.ray_creation_flag = False
        elif symbol == 101:  # e
            pass
        elif symbol == 114:  # r
            self.ray_creation_flag = True
            self.click_flag = False
            self.continious_flag = False
            self.mirror_creation_flag = False
            self.win_click_flag = False
            self.mirror_delete_flag = False
        elif symbol == 111:  # o - непрерывное создание зеркал
            self.continious_flag = not self.continious_flag
            print('Continious flag current value:', self.continious_flag)
        elif symbol == 97:  # a - delete all
            self.mirror_list = []
            self.ray = None
            self.ray_creation_flag = False
            self.click_flag = False
            self.continious_flag = False
            self.mirror_creation_flag = False
            self.win_click_flag = False
            self.mirror_delete_flag = False
        elif symbol == 115:  # s - save to json
            json_content = self.serialize()
            self.save_to_file(str(self.filename) + '.json', json_content)
        elif symbol == 108:  # l - load from json. rewrite current room
            self.load_from_file(self.filename+'.json')
        elif symbol == 113:  # q - exit
            print('bye')
            sys.exit(0)
        elif symbol == 117:  # u
            self.win_flag = True
        elif symbol == 110:  # n
            if self.ray:
                # self.win_flag = \
                self.ray.calc_ray_step(self.get_mirrors())
        elif symbol == 102:  # f
            if self.ray:
                arcade.draw_circle_filled(self.ray.x_0, self.ray.y_0, 5, arcade.color.RED)
        elif symbol == 119:  # w
            # создать круг победы
            self.win_click_flag = True
            self.ray_creation_flag = False
            self.mirror_creation_flag = False
            self.click_flag = False

    # что нужно, чтобы описать комнату и происходящее в ней:
    # список зеркал, луч(список сегментов, текущее положение, текущая скорость),
    #  состояние флагов и мб старых координат. мб константы - высота и ширина экрана

    def serialize(self):
        res = {
            'mirrors': [mirror.serialize() for mirror in self.get_mirrors()],
            # 'window_width': SCREEN_WIDTH,
            # 'window_height': SCREEN_HEIGHT,
            # 'window_title': SCREEN_TITLE,
            'prev_coords_x': self.prev_coords_x,
            'prev_coords_y': self.prev_coords_y,
            'ray_creation_flag': self.ray_creation_flag,
            'mirror_creation_flag': self.mirror_creation_flag,
            'click_flag': self.click_flag,
            'continious_flag': self.continious_flag
        }
        if self.ray:
            res['ray'] = self.ray.serialize()

        return res

    def deserialize(self, data):
        if not isinstance(data, dict):
            raise TypeError('Incorrect type of MyGame dict')
        m_l = data.get('mirrors')
        if m_l:
            mrs = []
        for m_data in m_l:
            mir = Mirror.Mirror(0, 0, 0, 0, 'flat', 0)
            mir.deserialize(m_data)
            mrs.append(mir)
        self.mirror_list = mrs

        self.prev_coords_x = data.get('prev_coords_x', 0)
        self.prev_coords_y = data.get('prev_coords_y', 0)
        self.ray_creation_flag = data.get('ray_creation_flag', False)
        self.mirror_creation_flag = data.get('mirror_creation_flag', False)
        self.click_flag = data.get('click_flag', False)
        self.continious_flag = data.get('continious_flag', False)

        if data.get('ray'):
            self.ray = RayLine.RayLine(0,0,0,0,None, 0, None)
            self.ray.deserialize(data['ray'])



    def save_to_file(self, filename, json_content):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(json_content, f, ensure_ascii=False )
        print('saved')

    def load_from_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            json_content = json.load(f)
            self.deserialize(json_content)
            print('loaded', json_content)


def main():
    window = MyGame()
    window.setup()
    arcade.set_background_color(arcade.color.BLACK)

    arcade.run()


if __name__ == "__main__":
    main()
