import math
import time

import pygame
from settings import HEIGHT, WIDTH

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

class Obstacle:
    def __init__(self, dots):
        self.lines = [Line(dots[x], dots[x+1]) for x in range(len(dots)-1)]
        self.lines.append(Line(dots[0], dots[-1]))
        self.dots = dots

    def tuple_dots(self):
        td = []
        for dot in self.dots:
            td.append((dot.x, dot.y))
        return td

    def draw(self, screen):
        pygame.draw.polygon(screen, (100, 100, 100), self.tuple_dots())

class Player:
    def __init__(self, _x, _y, _orientation):
        self.health = 100
        self.width = 10
        self.height = 25
        self.speed = 300
        self.jump = 500
        self.vel = Vector((0, 0))
        self.pos = Vector((_x, _y))
        self.surf = pygame.Surface((self.width+1, self.height+1))
        self.surf.fill((100, 255, 100))
        self.on_ground = False
        self.ground_normal = Vector((0, 1))
        self.ground_line = None
        self.orientation = _orientation
        self.punch = Punch()
        self.last_hit = time.time()

    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.surf, (self.pos.x-self.width/2, self.pos.y - self.height))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(self.pos.x-10, self.pos.y-self.height-10, self.health/5, 5))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.pos.x-10+self.health/5, self.pos.y-self.height-10, (100-self.health)/5, 5))

    def check_collision(self, line):
        a = self.pos + Vector((-self.width/2, 0))
        b = self.pos + Vector((-self.width/2, -self.height))
        c = self.pos + Vector((self.width / 2, -self.height))
        d = self.pos + Vector((self.width / 2, 0))
        sides = [
            Line(a, b), Line(b, c), Line(c, d), Line(d, a)
        ]
        for l in sides:
            if l.is_colliding(line):
                return True
        return False

    def check_ground(self, line):
        if line.vector.x == 0:
            return
        k = line.vector.y/line.vector.x
        b = line.a.y - line.a.x*k
        if self.pos.y < self.pos.x*k + b + 0.5:
            self.on_ground = True
            self.ground_line = line
            self.ground_normal = line.vector.perpendicular().normalized()

    def move(self, delta, map):
        old_pos = Vector((self.pos.x, self.pos.y))
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
        filtered_lines = []
        for obs in map:
            for l in obs.lines:
                if not self.vel.is_collinear(l.vector):
                    filtered_lines.append(l)
        while delta_left>0:
            self.pos += vel_seg
            for l in filtered_lines:
                if self.check_collision(l):
                    self.check_ground(l)
                    self.pos -= vel_seg
                    self.vel = self.vel.projection(l.vector)
                    if self.vel.length()<=0.2:
                        return
                    self.move(delta_left, map)
                    return
            delta_left -= delta_seg
        return

    def logic(self, inp, delta, map, enemy, grav):
        self.on_ground = False
        self.ground_line = None
        self.ground_normal = None

        if (self.vel*delta).length() > min(self.width, self.height):
            n = int((self.vel*delta).length()//min(self.width, self.height)+1)
            for i in range(n):
                self.move(delta/n, map)
        else:
            self.move(delta, map)

        if self.pos.y > HEIGHT + self.height + 100:
            self.pos.x = WIDTH/2
            self.pos.y = -100

        self.vel += grav * delta
        if time.time() - self.last_hit > 0.2: #todo изменить на чтото типо hit_recovery_time
            if self.on_ground:
                ground_vec = self.ground_line.vector.normalized()
                if abs(ground_vec.angle_deg()) <= 60:
                    if inp["a"] and self.vel.x > -self.speed:
                        self.orientation = "l"
                        self.vel -= ground_vec * self.speed * delta * 10
                    if inp["d"] and self.vel.x < self.speed:
                        self.orientation = "r"
                        self.vel += ground_vec * self.speed * delta * 10
                else:
                    if inp["a"] and self.vel.x > -self.speed:
                        self.orientation = "l"
                        self.vel.x -= self.speed * delta * 4
                    if inp["d"] and self.vel.x < self.speed:
                        self.orientation = "r"
                        self.vel.x += self.speed * delta * 4
                if inp["w"]:
                    self.vel -= self.ground_normal.normalized() * self.jump
            else:
                if inp["a"]:
                    self.orientation = "l"
                    if self.vel.x > -self.speed / 2:
                        self.vel.x -= self.speed * delta * 5
                if inp["d"]:
                    self.orientation = "r"
                    if self.vel.x < self.speed / 5:
                        self.vel.x += self.speed * delta * 5
                if inp["w"]:
                    self.vel.y -= self.jump * 2 * delta

        if self.on_ground and abs(self.ground_line.vector.normalized().angle_deg()) <= 60:
            self.vel -= self.ground_line.vector.normalized() * self.vel.dot(self.ground_line.vector.normalized()) * 10 * delta

        punch = False
        if inp["o"]:
            punch = self.punch.hit(self, enemy)
        return punch

    def convert_quick_dict(self):
        d = {
            "pos": self.pos.convert_dict(),
            "vel": self.vel.convert_dict(),
            "orientation": self.orientation
        }
        return d

    def convert_full_dict(self):
        if self.ground_normal is None:
            gn = None
        else:
            gn = self.ground_normal.convert_dict()
        if self.ground_line is None:
            gl = None
        else:
            gl = self.ground_line.convert_dict()
        d = {
            "health": self.health,
            "width": self.width,
            "height": self.height,
            "speed": self.speed,
            "jump": self.jump,
            "vel": self.vel.convert_dict(),
            "pos": self.pos.convert_dict(),
            "on_ground": self.on_ground,
            "ground_normal": gn,
            "ground_line": gl,
            "orientation": self.orientation,
            "punch": self.punch.convert_dict()
        }
        return d

    def update_from_dict(self, d):
        if "health" in d.keys():
            self.health = int(d["health"])
        if "width" in d.keys():
            self.width = int(d["width"])
        if "height" in d.keys():
            self.height = int(d["height"])
        if "speed" in d.keys():
            self.speed = int(d["speed"])
        if "jump" in d.keys():
            self.jump = int(d["jump"])
        if "vel" in d.keys():
            self.vel = Vector((0, 0)).from_dict(d["vel"])
        if "pos" in d.keys():
            self.pos = Vector((0, 0)).from_dict(d["pos"])
        if "on_ground" in d.keys():
            self.on_ground = bool(d["on_ground"])
        if "ground_normal" in d.keys():
            self.ground_normal = Vector((0, 0)).from_dict(d["ground_normal"])
        if "ground_line" in d.keys():
            self.ground_line = Line(Vector((0, 0)), Vector((0, 0))).from_dict(d["ground_line"])
        if "orientation" in d.keys():
            self.orientation = d["orientation"]
        if "punch" in d.keys():
            self.punch = Punch().from_dict(d["punch"])

    def __str__(self):
        return f"Character(pos={self.pos}, vel={self.vel}, on_ground={self.on_ground})"

class Punch:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.damage = 5
        self.knock_back = Vector((100, -100))
        self.reload = 0.2

    def rel_pos(self, p_width, p_height, p_orientation, p_pos):
        if p_orientation == "l":
            return Vector((p_pos.x-p_width/2-self.width, p_pos.y - p_height))
        if p_orientation == "r":
            return Vector((p_pos.x+p_width/2, p_pos.y - p_height))

    def check_col(self, player, enemy, offset=Vector((0, 0))):
        p_pos = player.pos + offset
        r_pos = self.rel_pos(player.width, player.height, player.orientation, p_pos)
        e_pos = Vector((enemy.pos.x - enemy.width/2, enemy.pos.y - enemy.height))
        if (r_pos.x+self.width < e_pos.x or e_pos.x+enemy.width < r_pos.x) or (r_pos.y+self.height < e_pos.y or e_pos.y+enemy.height < r_pos.y):
            return False
        return True

    def check_reload(self, player):
        return time.time()-player.last_hit > self.reload

    def hit(self, player, enemy, offset=Vector((0, 0))):
        if player.vel.x > 100:
            player.vel.x += -100
        if player.vel.x < -100:
            player.vel.x += 100
        if self.check_reload(player):
            player.last_hit = time.time()
            if self.check_col(player, enemy, offset):
                if player.orientation == "r":
                    enemy.vel += self.knock_back
                else:
                    enemy.vel.y += self.knock_back.y
                    enemy.vel.x -= self.knock_back.x
                enemy.health -= self.damage
                enemy.last_hit = time.time()+0.5
                return True
        return False

    def server_hit(self, player, enemy, ping):
        offset = -player.vel * ping
        if self.check_col(player, enemy, offset) and self.check_reload(player):
            if player.orientation == "r":
                enemy.vel += self.knock_back
            else:
                enemy.vel.y += self.knock_back.y
                enemy.vel.x -= self.knock_back.x
            player.last_hit = time.time()
            return True
        return False

    def draw_hitbox(self, player, screen):
        r_pos = self.rel_pos(player.width, player.height, player.orientation, player.pos)
        pygame.draw.rect(screen, (255, 0, 0), pygame.rect.Rect(r_pos.x, r_pos.y, self.width, self.height))

    def from_dict(self, d):
        self.height = d["height"]
        self.width = d["width"]
        self.reload = d["reload"]
        self.knock_back = Vector((0, 0)).from_dict(d["knock_back"])

    def convert_dict(self):
        d = {
            "height": self.height,
            "width": self.width,
            "reload": self.reload,
            "knock_back": self.knock_back
        }
        return d

class Button:

    def __init__(self, _pos: Vector, _width: int, _height: int, _text: str, _color=(255, 255, 255), _outline_color=(150, 150, 150)):
        self.pos = _pos
        self.width = _width
        self.height = _height
        self.text = _text
        self.color = _color
        self.outline_color = _outline_color
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.outline_color, self.rect, width=2, border_radius=5)

        font_size = max(20, self.height // 3)
        font = pygame.font.Font(None, font_size)

        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def check_in_button(self, _pos):
        return (self.pos.x < _pos.x < self.pos.x + self.width) and (self.pos.y < _pos.y < self.pos.y + self.height)