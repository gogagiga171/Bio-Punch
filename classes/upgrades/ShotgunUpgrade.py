import math
import random
import json
from classes.upgrades.Upgrade import Upgrade, ServerUpgrade
from classes.Projectiles import ServerBullet
from classes.Player import Player
from classes.Vector import Vector

class SUShotgun(ServerUpgrade):
    min_bullet_count = 3
    max_bullet_count = 4
    min_bullet_angle = -math.pi / 3
    max_bullet_angle = math.pi / 3
    bullet_damage = 10
    bullet_lifetime = 0.5
    bullet_speed = 500
    radius = 2.5

    def load_from_dict(self, _dict):
        if "min_bullet_count" in _dict.keys():
            self.min_bullet_count = _dict["min_bullet_count"]
        if "max_bullet_count" in _dict.keys():
            self.max_bullet_count = _dict["max_bullet_count"]
        if "min_bullet_angle" in _dict.keys():
            self.min_bullet_angle = _dict["min_bullet_angle"]
        if "max_bullet_angle" in _dict.keys():
            self.max_bullet_angle = _dict["max_bullet_angle"]
        if "bullet_damage" in _dict.keys():
            self.bullet_damage = _dict["bullet_damage"]
        if "bullet_lifetime" in _dict.keys():
            self.bullet_lifetime = _dict["bullet_lifetime"]
        if "bullet_speed" in _dict.keys():
            self.bullet_speed = _dict["bullet_speed"]
        if "radius" in _dict.keys():
            self.radius = _dict["radius"]

    def trigger(self, player: Player, projectiles):
        count = random.randint(self.min_bullet_count, self.max_bullet_count)
        for _ in range(count):
            x_offset = player.width/2
            direction = Vector((0, 0))
            direction.from_angle_and_distance(random.uniform(self.min_bullet_angle, self.max_bullet_angle), 1)
            if player.orientation == "l":
                direction *= -1
                x_offset *= -1
            position = player.pos + Vector((x_offset, -player.height/2))

            max_id = 0
            for i in projectiles:
                if i.id > max_id:
                    max_id = i.id

            bullet = ServerBullet(direction, player, position, max_id+1)
            bullet.damage = self.bullet_damage
            bullet.speed = self.bullet_speed
            bullet.lifetime = self.bullet_lifetime
            bullet.radius = self.radius
            projectiles.append(bullet)

            data = {
                "name": "projectile_spawn",
                "projectile_name": "Bullet",
                "data": bullet.convert_quick_dict(),
                "host": player.n
            }
            player.socket.send(json.dumps(data).encode("utf-8")+b"\n")
            player.enemy.socket.send(json.dumps(data).encode("utf-8") + b"\n")

class UShotgun(Upgrade):
    triggerable = True
    image_name = "UShotgun.png"
    title = "Дробовик"
    min_bullet_count = 3
    max_bullet_count = 4
    min_bullet_angle = -math.pi/3
    max_bullet_angle = math.pi/3
    bullet_damage = 10
    bullet_lifetime = 0.5
    bullet_speed = 500
    radius = 2.5
    description = "выстреливает 3-4 снаряда вперёд в случайном направлении"
    comment = "идеально чтобы организовать пакость"

    def convert_dict(self):
        _dict = {
            "min_bullet_count": self.min_bullet_count,
            "max_bullet_count": self.max_bullet_count,
            "min_bullet_angle": self.min_bullet_angle,
            "max_bullet_angle": self.max_bullet_angle,
            "bullet_damage": self.bullet_damage,
            "bullet_lifetime": self.bullet_lifetime,
            "bullet_speed": self.bullet_speed,
            "radius": self.radius
        }
        return _dict

    def trigger(self, player: Player, projectiles):
        data = {
            "name": "upgrade_triggered",
            "upgrade_name": "Shotgun",
            "data": self.convert_dict()
        }

        player.socket.send(json.dumps(data).encode("utf-8")+b"\n")