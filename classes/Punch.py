from classes.Vector import Vector
import time
import pygame

class Punch:
    def __init__(self):
        self.width = 20
        self.height = 20
        self.damage = 5
        self.knock_back = Vector((100, -100))
        self.reload = 0.2
        self.recovery_time = 0.2
        self.stun = 0.3

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
        player.recovered_time = time.time()+self.recovery_time
        if self.check_reload(player):
            player.last_hit = time.time()
            if self.check_col(player, enemy, offset):
                if player.orientation == "r":
                    enemy.vel += self.knock_back
                else:
                    enemy.vel.y += self.knock_back.y
                    enemy.vel.x -= self.knock_back.x
                enemy.health -= self.damage
                enemy.last_hit = self.stun
                enemy.recovered_time = time.time() + self.stun
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

    def draw_hitbox(self, player, screen, color=(255, 0, 0)):
        r_pos = self.rel_pos(player.width, player.height, player.orientation, player.pos)
        pygame.draw.rect(screen, color, pygame.rect.Rect(r_pos.x, r_pos.y, self.width, self.height))

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

class Kick(Punch):
    def __init__(self):
        super().__init__()
        self.height = 10
        self.damage = 2
        self.reload = 0.3
        self.recovery_time = 0.3
        self.stun = 0.5

    def rel_pos(self, p_width, p_height, p_orientation, p_pos):
        if p_orientation == "l":
            return Vector((p_pos.x - p_width / 2 - self.width, p_pos.y - self.height))
        if p_orientation == "r":
            return Vector((p_pos.x + p_width / 2, p_pos.y - self.height))

    def draw_hitbox(self, player, screen, color=(255, 255, 0)):
        super().draw_hitbox(player, screen, color)