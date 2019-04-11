from arcade import draw_circle_filled
from arcade.color import RED

import Mirror
import Segment
from utils import *


class RayLine:
    def __init__(self, x, y, x2, y2, mirrors, line_num, win_circle):
        self.last_mirror = None
        self.segment_list = []
        self.x_0 = x
        self.y_0 = y
        self.vx = x2 - x
        self.vy = y2 - y
        self.count = line_num
        self.mirrors = mirrors
        self.win_circle = win_circle  # кортеж (x0, y0, rad) или None

    def __str__(self):
        return """RayLine object. x_0: {0}, y_0: {1}, \
        vx: {2}, vy: {3}, last_mirror: {4}, count: {5}""".format(self.x_0, self.y_0, self.vx, self.vy,
                                                                 str(self.last_mirror), self.count)

    #   Считает путь луча
    def calc_ray(self, mirrors):
        x1 = self.x_0
        y1 = self.y_0
        last_mirror = None
        while self.count > 0:
            inters_mirrors = []
            fl = False
            print('count', self.count)
            for mirror in mirrors:
                if mirror is not last_mirror:
                    # print(x1, y1, x1 + self.vx, y1 + self.vy, mirror.x1, mirror.y1, mirror.x2, mirror.y2)
                    prs, x, y = intersect(x1, y1, x1 + self.vx * 400, y1 + self.vy * 400, mirror.x1, mirror.y1,
                                          mirror.x2, mirror.y2)
                    # print(prs, x, y)
                    if prs:
                        # find closest mirror
                        distance = math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)
                        inters_mirrors.append((distance, mirror))
                        inters_mirrors.sort(key=lambda s: s[0])
                        print(inters_mirrors)
            for mirror in mirrors:
                if mirror is not last_mirror:
                    # print(x1, y1, x1 + self.vx, y1 + self.vy, mirror.x1, mirror.y1, mirror.x2, mirror.y2)
                    prs, x, y = intersect(x1, y1, x1 + self.vx * 400, y1 + self.vy * 400, mirror.x1, mirror.y1,
                                          mirror.x2, mirror.y2)
                    # print(prs, x, y)
                    if prs:
                        # find closest mirror

                        ray = Segment.Segment(x1, y1, x, y)
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
                ray = Segment.Segment(x1, y1, x1 + self.vx * 3000, y1 + self.vy * 3000)
                self.segment_list.append(ray)
                print(ray, '|', len(self.segment_list))
                return
                # self.count = 0

    # добавляет одинотрезок к лучу: от зеркала до зеркала. мы принимаем последние координаты и последний вектор скорости
    # находим следующую точку пересечения с зеркалом(кстати, многоугольник-то замкнутый), считаем новый вектор скорости
    # сохраняем всё это дело. добавляем сегмент в список сегментов.
    def calc_ray_step(self, mirrors):
        inters_mirrors = []
        for mirror in mirrors:
            if mirror is not self.last_mirror:
                # print(x1, y1, x1 + self.vx, y1 + self.vy, mirror.x1, mirror.y1, mirror.x2, mirror.y2)
                prs, x, y = intersect(self.x_0, self.y_0, self.x_0 + self.vx * 1000, self.y_0 + self.vy * 1000,
                                      mirror.x1, mirror.y1, mirror.x2, mirror.y2)
                # print(prs, x, y)
                if prs:
                    # find closest mirror
                    distance = math.sqrt((self.x_0 - x) ** 2 + (self.y_0 - y) ** 2)
                    # print('DISTANCEE', distance)
                    if distance >= EPS:  # разберись в природе этого костыля плес
                        inters_mirrors.append((distance, mirror, x, y))
                        inters_mirrors.sort(key=lambda s: s[0])
                    # for i in inters_mirrors:
                    #     print(i[1], end=':::')
                    # print()
                    # print(inters_mirrors)
        curr_mirror = inters_mirrors[0] if inters_mirrors and inters_mirrors[0][1] is not self.last_mirror else None
        if curr_mirror and self.count > 0:
            # print('EQU MIRRORS ', curr_mirror[1], self.last_mirror, self.last_mirror == curr_mirror[1])
            x, y = curr_mirror[2], curr_mirror[3]
            ray = Segment.Segment(self.x_0, self.y_0, x, y)
            self.segment_list.append(ray)
            ai_x, ai_y = reflect(self.x_0, self.y_0, x, y, curr_mirror[1])

            if self.win_circle:
                print('win_c', self.win_circle)
                # print((str(y - self.y_0).ljust(5) + 'x + ' + str(self.x_0 - x).ljust(5) + ' + ' + str(
                #     (self.y_0 * x) - (self.x_0 * y)).ljust(5)))
                # C new = C + A * x_0 + B * y_0 (здесь x0 и y0 - центр окружности победы)
                A = (y - self.y_0)
                B = (self.x_0 - x)
                ln_w = math.sqrt(A * A + B * B)
                C_new = self.y_0 * x - self.x_0 * y + A * self.win_circle[0] + B * self.win_circle[1]

                x_w = - (A * C_new) / ln_w
                y_w = - (B * C_new) / ln_w
                ln_r = math.sqrt(x_w * x_w + y_w * y_w)
                print('a', A, 'B', B, 'cnew', C_new, 'x_w', x_w, 'y_w', y_w, 'rad', ln_r)
                if ln_r < self.win_circle[2] ** 2 * 10:
                    print('YOU WIM!!!')
                    # return True

            self.vx = ai_x
            self.vy = ai_y
            self.x_0 = x
            self.y_0 = y
            self.last_mirror = curr_mirror[1]
            # print(self)
        else:
            print("Ой")
            print(self)
            print(inters_mirrors)
        self.count -= 1
        return False

    def draw(self):
        draw_circle_filled(self.x_0, self.y_0, 5, RED)
        for ray in self.segment_list:
            ray.draw()

    def serialize(self):
        return {
            'last_mirror': self.last_mirror.serialize(),
            'segment_list': [segment.serialize() for segment in self.segment_list],
            'x_0': self.x_0,
            'y_0': self.y_0,
            'vx': self.vx,
            'vy': self.vy,
            'count': self.count
        }

    def deserialize(self, data):
        # TODO Add validation
        self.x_0 = data.get('x_0')
        self.y_0 = data.get('y_0')
        self.vx = data.get('vx')
        self.vy = data.get('vy')
        self.count = data.get('count')

        m_l = data.get('mirrors')
        if m_l:
            mrs = []
            for m_data in m_l:
                mir = Mirror.Mirror(0, 0, 0, 0, 'flat', 0)
                mir.deserialize(m_data)
                mrs.append(mir)
            self.mirrors = mrs
        m_data = data.get('last_mirror')
        if m_data is not None:
            mir = Mirror.Mirror(0, 0, 0, 0, 'flat', 0)
            mir.deserialize(m_data)
            self.last_mirror = mir
        else:
            self.last_mirror = None

        s_l = data.get('segment_list')
        segments = []
        for s in s_l:
            seg = Segment.Segment(0, 0, 0, 0)
            seg.deserialize(s)
            segments.append(seg)
        self.segment_list = segments
        # print('So, so', self)
