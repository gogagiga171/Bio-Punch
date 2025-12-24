from classes.Vector import Vector
from classes.Punch import Punch, Kick
from classes.Line import Line
from settings import WIDTH, HEIGHT
import pygame
import time

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
        self.kick = Kick()
        self.last_hit = time.time()
        self.recovered_time = time.time()

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
        if time.time() >= self.recovered_time:
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

        punch = {
            "punch": False,
            "kick": False
        }
        if inp["o"]:
            punch["punch"] = self.punch.hit(self, enemy)
        if inp["l"]:
            punch["kick"] = self.kick.hit(self, enemy)
        return punch

    def convert_quick_dict(self):
        d = {
            "pos": self.pos.convert_dict(),
            "vel": self.vel.convert_dict(),
            "orientation": self.orientation,
            "recovered_time": self.recovered_time
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
            "punch": self.punch.convert_dict(),
            "kick": self.kick.convert_dict(),
            "last_hit": self.last_hit,
            "recovered_time": self.recovered_time
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
        if "kick" in d.keys():
            self.kick = Kick().from_dict(d["kick"])
        if "last_hit" in d.keys():
            self.last_hit = float(d["last_hit"])
        if "recovered_time" in d.keys():
            self.recovered_time = float(d["recovered_time"])

    def __str__(self):
        return f"Character(pos={self.pos}, vel={self.vel}, on_ground={self.on_ground})"