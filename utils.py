import math

EPS = 10 ** (-9)


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
