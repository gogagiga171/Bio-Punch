import time
import pygame
from classes.Vector import Vector
from classes.Player import Player, ServerSidePlayer
import json


class Projectile:
    id: int
    host: Player
    lifetime: float
    start_time: float
    direction: Vector
    speed: float
    pos: Vector
    server: bool

    def __init__(self, _id):
        self.id = _id
        self.start_time = time.time()

    def move(self, delta):
        self.pos += self.direction * self.speed * delta

    def check_collision(self):
        return False

    def affect(self):
        pass

    def draw(self, screen):
        pass

    def logic(self, delta):
        c = False
        if time.time() - self.start_time > self.lifetime:
            return True
        self.move(delta)
        if self.server and self.check_collision():
            c = self.affect()
        return c

    def load_from_dict(self, _dict: dict):
        if "pos" in _dict.keys():
            self.pos = Vector((0, 0)).from_dict(_dict["pos"])
        if "start_time" in _dict.keys():
            self.start_time = float(_dict["start_time"])
        if "direction" in _dict.keys():
            self.direction = Vector((0, 0)).from_dict(_dict["direction"])
        if "speed" in _dict.keys():
            self.speed = float(_dict["speed"])
        if "radius" in _dict.keys():
            self.radius = float(_dict["radius"])
        if "id" in _dict.keys():
            self.id = int(_dict["id"])

    def convert_quick_dict(self):
        _dict = {
            "pos": self.pos.convert_dict(),
            "start_time": self.start_time,
            "direction": self.direction.convert_dict(),
            "speed": self.speed,
            "radius": self.radius,
            "id": self.id
        }
        return _dict

class Bullet(Projectile):
    damage: float
    radius: float
    color: tuple[int, int, int]

    def __init__(self, _direction, _host, _pos, _id):
        super().__init__(_id)
        self.host = _host
        self.lifetime = 0.5
        self.radius = 2.5
        self.direction = _direction
        self.speed = 500
        self.pos = _pos
        self.damage = 10
        self.color = (70, 70, 70)
        self.server = False

    def affect(self):
        self.host.enemy.health -= self.damage
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), self.radius)

class ServerBullet(Bullet):
    host: ServerSidePlayer

    def __init__(self, _direction, _host, _pos, _id):
        super().__init__(_direction, _host, _pos, _id)
        self.server = True

    def check_collision(self):
        enemy = self.host.enemy

        if self.pos.x < enemy.pos.x:
            closest_x = enemy.pos.x
        elif self.pos.x > enemy.pos.x + enemy.width:
            closest_x = enemy.pos.x + enemy.width
        else:
            closest_x = self.pos.x

        if self.pos.y < enemy.pos.y:
            closest_y = enemy.pos.y
        elif self.pos.y > enemy.pos.y + enemy.height:
            closest_y = enemy.pos.y + enemy.height
        else:
            closest_y = self.pos.y

        distance = (self.pos - Vector((closest_x, closest_y))).length()

        return distance < self.radius

    def affect(self): # взаимодействует с целью не в зависимости от положения уже после проверки колизии
        self.host.enemy.health -= self.damage
        data = {
            "name": "projectile_affect",
            "id": self.id
        }
        self.host.socket.send(json.dumps(data).encode("utf-8")+b"\n")
        self.host.enemy.socket.send(json.dumps(data).encode("utf-8") + b"\n")
        return True

def spawn_projectile(projectiles, host, name, _dict):
    names = {
        "Bullet": Bullet
    }

    projectile = names[name](None, host, None, None)
    projectile.load_from_dict(_dict)

    projectiles.append(projectile)