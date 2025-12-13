import pygame
import socket
import json
import threading
import math

message_delta = 1/20
SERVER = ""
WIDTH = 800
HEIGHT = 600

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
        onto_norm = onto.normalize()
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
        self.a = Vector(a)
        self.b = Vector(b)

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

    def aabb_segment_sat(self, pos, w, h, a, b):
        minb = Vector((pos.x - w / 2, pos.y - h))
        maxb = Vector((pos.x + w / 2, pos.y))

        axes = [
            Vector((1, 0)),
            Vector((0, 1)),
            (b - a).normalized(),
            (b - a).perpendicular().normalized()
        ]

        min_overlap = float('inf')
        best_axis = None

        corners = [
            minb,
            Vector((maxb.x, minb.y)),
            maxb,
            Vector((minb.x, maxb.y))
        ]

        for axis in axes:
            box_proj = [c.dot(axis) for c in corners]
            seg_proj = [a.dot(axis), b.dot(axis)]

            overlap = min(max(box_proj), max(seg_proj)) - max(min(box_proj), min(seg_proj))
            if overlap <= 0:
                return None

            if overlap < min_overlap:
                min_overlap = overlap
                best_axis = axis

        center = (minb + maxb) * 0.5
        line_center = (a + b) * 0.5
        if (center - line_center).dot(best_axis) < 0:
            best_axis = -best_axis

        return best_axis * min_overlap

    def move(self, inp, delta, map, grav): #todo самому переделать этот ИИ слоп
        # 1. гравитация
        self.vel += grav * delta
        self.on_ground = False

        # 2. движение по X
        self.pos.x += self.vel.x * delta
        for obj in map:
            for line in obj.lines:
                a, b = line.a, line.b
                line_vec = b - a
                normal = line_vec.perpendicular().normalized()

                # ближайшая точка на линии к персонажу
                closest = line.closest_point(Vector((self.pos.x, self.pos.y - self.height / 2)))

                dx = self.pos.x - closest.x
                dy = (self.pos.y - self.height / 2) - closest.y

                # проверка AABB (ширина/высота)
                if abs(dx) <= self.width / 2 and abs(dy) <= self.height / 2:
                    # вытаскиваем по нормали линии
                    penetration = Vector((dx, dy)).dot(normal)
                    self.pos += normal * penetration
                    # проекция скорости на линию
                    self.vel -= normal * self.vel.dot(normal)

        # 3. движение по Y
        self.pos.y += self.vel.y * delta
        for obj in map:
            for line in obj.lines:
                a, b = line.a, line.b
                line_vec = b - a
                normal = line_vec.perpendicular().normalized()
                closest = line.closest_point(Vector((self.pos.x, self.pos.y - self.height / 2)))

                dx = self.pos.x - closest.x
                dy = (self.pos.y - self.height / 2) - closest.y

                if abs(dx) <= self.width / 2 and abs(dy) <= self.height / 2:
                    penetration = Vector((dx, dy)).dot(normal)
                    self.pos += normal * penetration
                    self.vel -= normal * self.vel.dot(normal)

                    # определяем землю
                    if normal.dot(Vector((0, 1))) > 0.5:
                        self.on_ground = True
                        self.ground_normal = normal
                        self.ground_line = line

        # 4. управление на земле
        if self.on_ground and inp:
            line_dir = (self.ground_line.b - self.ground_line.a).normalized()
            if inp.get('a'):
                self.vel -= line_dir * self.speed * delta * 5
            if inp.get('d'):
                self.vel += line_dir * self.speed * delta * 5
            if inp.get('w'):
                self.vel.y -= self.jump

            # трение вдоль линии
            self.vel -= line_dir * self.vel.dot(line_dir) * 0.2

    def __str__(self):
        return f"Character(pos={self.pos}, vel={self.vel}, on_ground={self.on_ground})"


def main():
    #server = Server(SERVER)
    #server.connect()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 60
    running = True
    player = Player()
    floor = Obstacle([
        Vector((100, 400)), Vector((700, 400)), Vector((700, 500)), Vector((100, 500))
    ])
    map = [floor]

    while running:
        delta = clock.tick(fps)/1000
        screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type ==  pygame.QUIT:
                running = False

        pg_keys = pygame.key.get_pressed()
        keys = {
            "a": pg_keys[pygame.K_a],
            "d": pg_keys[pygame.K_d],
            "w": pg_keys[pygame.K_w]
        }
        player.move(keys, delta, map, Vector((0, 500)))
        player.draw(screen)
        for obs in map:
            obs.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()