from arcade import draw_line
from arcade.color import BRIGHT_GREEN


class Segment:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return 'Segment ' + str(self.x1) + ' ' + str(self.y1) + ' ' + str(self.x2) + ' ' + str(self.y2)

    def draw(self):
        draw_line(self.x1, self.y1, self.x2, self.y2, BRIGHT_GREEN, 1)

    def serialize(self):
        return {
            'class': 'Segment',
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2
        }

    def deserialize(self, data):
        if isinstance(data, dict):
            if data.get('class') != 'Segment':
                raise ValueError('Incorrect class field value')
            for field in ['x1', 'y1', 'x2', 'y2']:
                if not (isinstance(data.get(field), float) or isinstance(data.get(field), int)):
                    print(self)
                    print(data)
                    print(type(data.get(field)))
                    raise TypeError('Incorrect type of segment coordinate')
            self.x1 = data['x1']
            self.y1 = data['y1']
            self.x2 = data['x2']
            self.y2 = data['y2']
