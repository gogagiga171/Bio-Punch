import socket
import json
import math
import pygame
from settings import *

class Server:
    def __init__(self, _server):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (_server, 5555)
        self.player_id = None
        self.game_state = {}

    def connect(self):
        self.socket.connect(self.server_address)

    def receive_updates(self):
        while True:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if data:
                    self.game_state = json.loads(data)
            except:
                break

    def send_message(self, message):
        self.socket.send(message.encode('utf-8'))

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

class Line:
    def __init__(self, a, b):
        if a.x < b.x:
            self.a = Vector(a)
            self.b = Vector(b)
        else:
            self.b = Vector(a)
            self.a = Vector(b)

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

class Obstacle:
    def __init__(self, dots):
        self.lines = [Line(dots[x], dots[x+1]) for x in range(len(dots)-1)]
        self.dots = dots

    def tuple_dots(self):
        td = []
        for dot in self.dots:
            td.append((dot.x, dot.y))
        return td

    def draw(self, screen):
        pygame.draw.polygon(screen, (100, 100, 100), self.tuple_dots())

class Player:
    def __init__(self):
        self.width = 10
        self.height = 25
        self.speed = 300
        self.jump = 500
        self.vel = Vector((0, 0))
        self.pos = Vector((WIDTH/2, HEIGHT/2+self.height/2))
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill((100, 255, 100))
        self.on_ground = False
        self.ground_normal = Vector((0, 1))
        self.ground_line = None

    @property
    def rect_points(self):
        """Возвращает 4 точки прямоугольника персонажа"""
        half_w = self.width / 2
        return [
            Vector((self.pos.x - half_w, self.pos.y)),  # нижний левый
            Vector((self.pos.x + half_w, self.pos.y)),  # нижний правый
            Vector((self.pos.x + half_w, self.pos.y - self.height)),  # верхний правый
            Vector((self.pos.x - half_w, self.pos.y - self.height))  # верхний левый
        ]

    @property
    def bounding_box(self):
        """Минимальная и максимальная точки AABB"""
        half_w = self.width / 2
        return (
            Vector((self.pos.x - half_w, self.pos.y - self.height)),  # min
            Vector((self.pos.x + half_w, self.pos.y))  # max
        )

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.surf, (self.pos.x-self.width/2, self.pos.y - self.height))

    def check_collision(self, line):
        x0, y0 = line.a.x, line.a.y
        x1, y1 = line.b.x, line.b.y

        dx = x1 - x0
        dy = y1 - y0

        left = self.pos.x - self.width / 2
        right = self.pos.x + self.width / 2
        top = self.pos.y - self.height
        bottom = self.pos.y

        t0 = 0.0
        t1 = 1.0

        def clip(p, q):
            nonlocal t0, t1
            if abs(p) < 1e-9:
                return q >= 0
            t = q / p
            if p < 0:
                if t > t1: return False
                if t > t0: t0 = t
            else:
                if t < t0: return False
                if t < t1: t1 = t
            return True

        if not clip(-dx, x0 - left):   return False
        if not clip(dx, right - x0):  return False
        if not clip(-dy, y0 - top):    return False
        if not clip(dy, bottom - y0): return False

        return t0 <= t1

    def check_ground(self, line):
        if line.a.y <= self.pos.y or line.b.y <= self.pos.y:
            self.on_ground = True
            self.ground_line = line
            self.ground_normal = line.vector.perpendicular().normalized()

    def move(self, delta, map):
        old_pos = self.pos
        self.pos += self.vel * delta
        f = False
        for obs in map:
            for l in obs.lines:
                if self.check_collision(l):
                    f = True
                    break
            if f:
                break
        if not f:
            return

        self.pos = old_pos
        delta_seg = delta/((self.vel*delta).length()/0.5)
        vel_seg = self.vel.normalized()*0.5
        delta_left = delta
        f = False
        while delta_left>0:
            self.pos += vel_seg
            for obs in map:
                for l in obs.lines:
                    if self.check_collision(l):
                        self.check_ground(l)
                        self.pos -= vel_seg
                        self.vel = self.vel.projection(l.vector)
                        if self.vel.length()<=0.2:
                            return
                        self.move(delta, map)
                        return
            delta_left -= delta_seg
        return

    def logic(self, inp, delta, map, grav):
        self.vel += grav * delta
        if self.on_ground:
            ground_vec = self.ground_line.vector.normalized()
            if inp["a"] and self.vel.x > -self.speed:
                self.vel -= ground_vec * self.speed * delta * 10
            if inp["d"] and self.vel.x < self.speed:
                self.vel += ground_vec * self.speed * delta * 10
            if inp["w"]:
                self.vel -= self.ground_normal.normalized() * self.jump
                self.on_ground = False
                self.ground_line = None
                self.ground_normal = None
            self.vel -= ground_vec * self.vel.dot(ground_vec) * 10 * delta
        else:
            if inp["a"] and self.vel.x > -self.speed/5:
                self.vel.x -= self.speed * delta * 2
            if inp["d"] and self.vel.x < self.speed/5:
                self.vel.x += self.speed * delta * 2
            if inp["w"]:
                self.vel.y -= self.jump*2*delta

        self.move(delta, map)

    def __str__(self):
        return f"Character(pos={self.pos}, vel={self.vel}, on_ground={self.on_ground})"