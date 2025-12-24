from classes.Vector import Vector

class Line:
    def __init__(self, a, b):
        if a.x <= b.x:
            self.a = Vector(a)
            self.b = Vector(b)
        else:
            self.a = Vector(b)
            self.b = Vector(a)

    @property
    def vector(self):
        return self.b - self.a

    @property
    def normal(self):
        return self.vector.perpendicular().normalize()

    @property
    def length(self):
        return self.vector.length()

    def closest_point(self, point):
        """Находит ближайшую точку на линии к заданной точке"""
        ap = point - self.a
        ab = self.vector

        if self.length == 0:
            return self.a

        t = max(0, min(1, ap.dot(ab) / (self.length * self.length)))
        return self.a + ab * t

    def is_colliding(self, line):
        v1 = (self.a - line.a).cross(self.a - self.b)
        v2 = (self.a - line.b).cross(self.a - self.b)
        if v1*v2>0:
            return False
        v3 = (line.a - self.a).cross(line.a - line.b)
        v4 = (line.a - self.b).cross(line.a - line.b)
        if v3*v4>0:
            return False
        return True

    def convert_dict(self):
        d = {
            "a": self.a.convert_dict(),
            "b": self.b.convert_dict()
        }
        return d

    def from_dict(self, d):
        if d is None:
            return None
        self.a = Vector((0, 0)).from_dict(d["a"])
        self.b = Vector((0, 0)).from_dict(d["b"])
        return self

    def __str__(self):
        return f"Line(a={self.a}, b={self.b})"