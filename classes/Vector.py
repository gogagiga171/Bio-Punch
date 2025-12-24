import math

class Vector:
    def __init__(self, _v):
        self.x = _v[0]
        self.y = _v[1]

    def __add__(self, other):
        return Vector((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Vector((self.x - other.x, self.y - other.y))

    def __mul__(self, scalar):
        return Vector((self.x * scalar, self.y * scalar))

    def __truediv__(self, scalar):
        return Vector((self.x / scalar, self.y / scalar))

    def __getitem__(self, item):
        if item==0:
            return self.x
        else:
            return self.y

    def __neg__(self):
        return Vector((-self.x, -self.y))

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalized(self):
        length = self.length()
        if length == 0:
            return Vector((0, 0))
        return Vector((self.x / length, self.y / length))

    def perpendicular(self):
        return Vector((-self.y, self.x))

    def projection(self, onto):
        """Проекция вектора self на вектор onto"""
        onto_norm = onto.normalized()
        dot = self.dot(onto_norm)
        return onto_norm * dot

    def rejection(self, onto):
        """Перпендикулярная составляющая (отклонение)"""
        return self - self.projection(onto)

    def __str__(self):
        return f"Vector({self.x:.2f}, {self.y:.2f})"

    def __repr__(self):
        return str(self)

    def to_tuple(self):
        return (self.x, self.y)

    def angle_deg(self):
        return math.degrees(math.atan2(self.y, self.x))

    def is_collinear(self, other, eps=1e-6):
        return abs(self.cross(other)) <= eps

    def convert_dict(self):
        d = {
            "x": self.x,
            "y": self.y
        }
        return d

    def from_dict(self, d):
        if d is None:
            return None
        self.x = d["x"]
        self.y = d["y"]
        return self

    def copy(self):
        return Vector((self.x, self.y))