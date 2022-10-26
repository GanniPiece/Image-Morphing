

from PyQt5.QtCore import QPoint
import numpy as np

class Vector:

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Vector):
            self.direction = args[0].direction
        elif len(args) == 1 and isinstance(args[0], Line):
            self.direction = (args[0].Q - args[0].P).direction
        elif len(args) == 1 and isinstance(args[0], Direction):
            self.direction = args[0]
        elif len(args) == 2 and isinstance(args[0], Point):
            self.direction = args[1] - args[0]
        elif len(args) == 2 and (isinstance(args[0], float) or isinstance(args[0], int)):
            self.direction = Direction(args[0], args[1])
        else:
            raise f"unsupported type"
        
        self.magnitude = self.length()

    def __str__(self):
        return f"d={self.direction}, m={self.magnitude}"

    def __mul__(self, m):
        # scale
        if isinstance(m, float) or isinstance(m, int):
            return Vector(self.direction * m)
        # inner dot
        elif isinstance(m, Vector):
            return (self.direction.x * m.direction.x) + (self.direction.y * m.direction.y)
        else:
            raise "unsupported type for vector multiplication"
    
    def __add__(self, other):
        return Vector(self.direction + other.direction)

    def __sub__(self, other):
        return Vector(self.direction - other.direction)

    def __truediv__(self, div):
        return Vector(self.direction / div)
    
    def length(self):
        return np.sqrt((self.direction.x * self.direction.x) + (self.direction.y * self.direction.y))

    def perpendicular(self):
        return Vector(Direction(self.direction.y, -self.direction.x))


class Line:
    def __init__(self, s, e):
        self.P = s
        self.Q = e

    def show(self):
        return f"line  {str(self.P)}  {str(self.Q)}"
    def __str__(self):
        return f"line  {str(self.P)}  {str(self.Q)}"
    def __add__(self, other):
        return Line(self.P + other.P, self.Q + other.Q)
    def __mul__(self, mul):
        return Line(self.P * mul, self.Q * mul)
    def __truediv__(self, div):
        return Line(self.P / div, self.Q / div)
    def length(self):
        return np.sqrt(pow(self.P.x - self.Q.x, 2) + pow(self.P.y - self.Q.y, 2))
    def dist(self, X, u, v):
        if u > 1:
            return (X - self.Q).length()
        elif u < 0:
            return (X - self.P).length()
        else:
            # return abs((self.P - X) * Vector(self).perpendicular() / self.length())
            return abs(v)

class Point:
    def __init__(self, x: float, y: float, p: QPoint = None):
        if p:
            self.x = p.x()
            self.y = p.y()
        else:
            self.x = x
            self.y = y

    def __str__(self):
        return f"{self.x} {self.y}"

    def __mul__(self, m):
        return Point(self.x * m, self.y * m)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __add__(self, other):
        if isinstance(other, Point):
            return Point((self.x + other.x), (self.y + other.y))
        elif isinstance(other, Vector):
            return Point((self.x + other.direction.x), (self.y + other.direction.y))

    def __truediv__(self, div):
        return Point(self.x / div, self.y / div)

    def __lt__(self, point):
        if self.x >= point.x or self.y >= point.y:
            return False
        return True
    
    def __le__(self, point):
        if self.x > point.x or self.y > point.y:
            return False
        return True
    
    def __gt__(self, point):
        if self.x <= point.x or self.y <= point.y:
            return False
        return True

    def __ge__(self, point):
        if self.x < point.x or self.y < point.y:
            return False
        return True

    def shift_x(self, shift):
        self.x += shift
        return self

    def shift_y(self, shift):
        self.y += shift

class Direction:
    def __init__(self, *args):
        if len(args) == 2 and isinstance(args[0], Point):
            self.x = args[1].x - args[0].x
            self.y = args[1].y - args[1].y
        elif len(args) == 2 and (isinstance(args[0], float) or isinstance(args[0], int)):
            self.x = args[0]
            self.y = args[1]
        else:
            raise "unsupported input type"
    def __truediv__(self, div):
        return Direction(self.x / div, self.y / div)

    def __mul__(self, m):
        return Direction(self.x * m, self.y * m)

    def __add__(self, add):
        return Direction(self.x + add.x, self.y + add.y)

    def __sub__(self, sub):
        return Direction(self.x - sub.x, self.y - sub.y)