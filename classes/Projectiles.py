import time
import pygame
from Vector import Vector


class Projectile:
    lifetime: float
    start_time: float
    direction: Vector
    speed: float
    pos: Vector

    def __init__(self):
        self.start_time = time.time()

    def move(self, delta):
        self.pos += self.direction * self.speed * delta

    def check_collision(self, player):
        return False

    def affect(self, player):
        pass

    def draw(self, screen):
        pass

    def logic(self, delta, players):
        if time.time() - self.start_time > self.lifetime:
            return True
        self.move(delta)
        for player in players:
            if self.check_collision(player):
                self.affect(player)
        return False

class Bullet(Projectile):
    damage: float
    radius: float
    color: tuple[int, int, int]

    def __init__(self, _direction, _pos):
        super().__init__()
        self.lifetime = 0.5
        self.radius = 2.5
        self.direction = _direction
        self.speed = 500
        self.pos = _pos
        self.damage = 10
        self.color = (70, 70, 70)

    def check_collision(self, player):
        if player.pos.x < self.pos.x:
            closest_x = player.pos.x
        elif player.pos.x+player.width > self.pos.x:
            closest_x = player.pos.x + player.width
        else:
            closest_x = self.pos.x

        if player.pos.y < self.pos.y:
            closest_y = player.pos.y
        elif player.pos.y+player.height > self.pos.y:
            closest_y = player.pos.y + player.height
        else:
            closest_y = self.pos.y

        distance = (self.pos - Vector((closest_x, closest_y))).length()

        return distance < self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), self.radius)

    def affect(self, player):
        player.health -= self.damage
        self.lifetime = 0