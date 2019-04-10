from arcade import draw_line
from arcade.color import WHITE


class Mirror:
    def __init__(self, x1, y1, x2, y2, typ, rad):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.type = typ  # if type in ['flat', 'curve']
        self.rad = rad  # TODO дописать проверку соответствия радиуса и типа зеркала

    def __str__(self):
        return """Mirror object x1: {0}, y1: {1}, x2: {2}, y2: {3}""".format(self.x1, self.y1, self.x2, self.y2)

    def draw(self):
        draw_line(self.x1, self.y1, self.x2, self.y2, WHITE, 3)
