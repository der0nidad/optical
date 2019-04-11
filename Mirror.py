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

    def draw(self, thickened=False):
        if thickened:
            draw_line(self.x1, self.y1, self.x2, self.y2, WHITE, 20)
        else:
            draw_line(self.x1, self.y1, self.x2, self.y2, WHITE, 3)

    def serialize(self):
        return {
            'class': 'Mirror',
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2
        }

    def deserialize(self, data):
        if isinstance(data, dict):
            if data.get('class') != 'Mirror':
                raise ValueError('Incorrect class field value')
            for field in ['x1', 'y1', 'x2', 'y2']:
                if not (isinstance(data.get(field), float) or isinstance(data.get(field), int)):
                    # print(self)
                    # print(data)
                    # print(type(data.get(field)))
                    raise TypeError('Incorrect type of mirror coordinate')
            self.x1 = float(data['x1'])
            self.y1 = float(data['y1'])
            self.x2 = float(data['x2'])
            self.y2 = float(data['y2'])
            self.type = 'flat'
            self.rad = 0

    def calc_equality(self, mirror):
        EPS = 10 ** -9
        return (abs(self.x1 - mirror.x1) < EPS) and (abs(self.x2 - mirror.x2) < EPS) and (abs(
            self.y1 - mirror.y1) < EPS) and (abs(self.y2 - mirror.y2) < EPS) and self.type == mirror.type
