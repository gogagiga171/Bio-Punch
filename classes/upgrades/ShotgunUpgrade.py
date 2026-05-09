import math
import random
from classes.upgrades.Upgrade import Upgrade
from classes.Projectiles import Bullet
from classes.Player import Player
from classes.Vector import Vector

class UShotgun(Upgrade):
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

    def trigger(self, player: Player, projectiles):
        count = random.randint(self.min_bullet_count, self.max_bullet_count)
        for _ in range(count):
            x_offset = Player.width/2
            direction = Vector((0, 0))
            direction.from_angle_and_distance(random.random()/(self.max_bullet_count-self.min_bullet_angle) + self.min_bullet_count, 1)
            if Player.orientation == "l":
                direction *= -1
                x_offset *= -1
            position = Player.pos + Vector((x_offset, -Player.height/2))
            bullet = Bullet(direction, position)
            bullet.damage = self.bullet_damage
            bullet.speed = self.bullet_speed
            bullet.lifetime = self.bullet_lifetime
            bullet.radius = self.radius
            projectiles.append(bullet)