from classes.Vector import Vector
import time
import pygame

class Punch:
    def __init__(self):
        self.width = 20
        self.height = 10
        self.damage = 5
        self.enemy_knock_back = Vector((100, -100))
        self.player_knock_back = Vector((-20, -20))
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
        return time.time() > player.reload_time

    def hit(self, player, enemy, offset=Vector((0, 0))):
        if player.vel.x > 100:
            player.vel.x += -100
        if player.vel.x < -100:
            player.vel.x += 100
        player.recovered_time = time.time()+self.recovery_time
        if self.check_reload(player):
            player.reload_time = time.time() + self.reload
            if self.check_col(player, enemy, offset):
                if enemy.block.block:
                    if player.orientation == "r":
                        enemy.vel += self.enemy_knock_back * (1 - enemy.block.knock_back_resist)
                        player.vel += self.player_knock_back
                    else:
                        enemy.vel.y += self.enemy_knock_back.y * (1 - enemy.block.knock_back_resist)
                        enemy.vel.x -= self.enemy_knock_back.x * (1 - enemy.block.knock_back_resist)
                        player.vel.y += self.player_knock_back.y
                        player.vel.x -= self.player_knock_back.x
                    enemy.health -= self.damage * (1 - enemy.block.damage_resist)
                    enemy.reload_time = time.time() + self.stun * (1 - enemy.block.stun_resist)
                    enemy.recovered_time = time.time() + self.stun * (1 - enemy.block.stun_resist)
                else:
                    if player.orientation == "r":
                        enemy.vel += self.enemy_knock_back
                        player.vel += self.player_knock_back
                    else:
                        enemy.vel.y += self.enemy_knock_back.y
                        enemy.vel.x -= self.enemy_knock_back.x
                        player.vel.y += self.player_knock_back.y
                        player.vel.x -= self.player_knock_back.x
                    enemy.health -= self.damage
                    enemy.reload_time = time.time() + self.stun
                    enemy.recovered_time = time.time() + self.stun
                return True
        return False

    def server_hit(self, player, enemy, ping):
        offset = -player.vel * ping
        if player.vel.x > 100:
            player.vel.x += -100
        if player.vel.x < -100:
            player.vel.x += 100
        player.recovered_time = time.time() + self.recovery_time
        if self.check_reload(player):
            player.reload_time = time.time() + self.reload
            if self.check_col(player, enemy, offset):
                if enemy.block.block:
                    if player.orientation == "r":
                        enemy.vel += self.enemy_knock_back * (1 - enemy.block.knock_back_resist)
                    else:
                        enemy.vel.y += self.enemy_knock_back.y * (1 - enemy.block.knock_back_resist)
                        enemy.vel.x -= self.enemy_knock_back.x * (1 - enemy.block.knock_back_resist)
                    enemy.health -= self.damage*(1-enemy.block.damage_resist)
                    enemy.reload_time = time.time() + self.stun*(1-enemy.block.stun_resist)
                    enemy.recovered_time = time.time() + self.stun*(1-enemy.block.stun_resist)
                else:
                    if player.orientation == "r":
                        enemy.vel += self.enemy_knock_back
                    else:
                        enemy.vel.y += self.enemy_knock_back.y
                        enemy.vel.x -= self.enemy_knock_back.x
                    enemy.health -= self.damage
                    enemy.reload_time = time.time() + self.stun
                    enemy.recovered_time = time.time() + self.stun
                return True
        return False

    def draw_hitbox(self, player, screen, color=(255, 0, 0)):
        r_pos = self.rel_pos(player.width, player.height, player.orientation, player.pos)
        pygame.draw.rect(screen, color, pygame.rect.Rect(r_pos.x, r_pos.y, self.width, self.height))

    def from_dict(self, d):
        self.height = d["height"]
        self.width = d["width"]
        self.reload = d["reload"]
        self.enemy_knock_back = Vector((0, 0)).from_dict(d["enemy_knock_back"])
        self.player_knock_back = Vector((0, 0)).from_dict(d["player_knock_back"])

    def convert_dict(self):
        d = {
            "height": self.height,
            "width": self.width,
            "reload": self.reload,
            "enemy_knock_back": self.enemy_knock_back.convert_dict(),
            "player_knock_back": self.player_knock_back.convert_dict()
        }
        return d

class Kick(Punch):
    def __init__(self):
        super().__init__()
        self.height = 10
        self.damage = 2
        self.reload = 0.3
        self.recovery_time = 0.3
        self.stun = 0.4
        self.knock_back = Vector((300, -100))

    def rel_pos(self, p_width, p_height, p_orientation, p_pos):
        if p_orientation == "l":
            return Vector((p_pos.x - p_width / 2 - self.width, p_pos.y - self.height))
        if p_orientation == "r":
            return Vector((p_pos.x + p_width / 2, p_pos.y - self.height))

    def draw_hitbox(self, player, screen, color=(255, 255, 0)):
        super().draw_hitbox(player, screen, color)

class CrouchPunch(Punch):
    def __init__(self):
        super().__init__()
        self.width=10
        self.height=30
        self.damage=2
        self.enemy_knock_back = Vector((20, -500))
        self.player_knock_back = Vector((0, -450))
        self.stun = 0.4

    def rel_pos(self, p_width, p_height, p_orientation, p_pos):
        if p_orientation == "l":
            return Vector((p_pos.x - p_width / 2 - self.width, p_pos.y - p_height - (self.height-25/2)))
        if p_orientation == "r":
            return Vector((p_pos.x + p_width / 2, p_pos.y - p_height - (self.height-25/2)))

class CrouchKick(Kick):
    def __init__(self):
        super().__init__()
        self.height = 7
        self.damage = 1
        self.knock_back = Vector((50, 0))
        self.stun = 1
        self.player_knock_back = Vector((-5, 0))

class FlightPunch(Punch):
    def __init__(self):
        super().__init__()
        self.height = 35
        self.width = 35
        self.damage = 4
        self.enemy_knock_back = Vector((30, -70))
        self.player_knock_back = Vector((10, -70))
        self.stun = 0.3
        self.reload = 0.1
        self.recovery_time = 0.1

    def rel_pos(self, p_width, p_height, p_orientation, p_pos):
        if p_orientation == "l":
            return Vector((p_pos.x-p_width/2-self.width, p_pos.y - p_height - 5))
        if p_orientation == "r":
            return Vector((p_pos.x+p_width/2, p_pos.y - p_height - 5))

class FlightKick(Kick):
    def __init__(self):
        super().__init__()
        self.height = 35
        self.width = 20
        self.damage = 8
        self.enemy_knock_back = Vector((100, 300))
        self.player_knock_back = Vector((-20, -10))
        self.stun = 1.3
        self.recovery_time = 0.1
        self.reload = 0.5

    def rel_pos(self, p_width, p_height, p_orientation, p_pos):
        if p_orientation == "l":
            return Vector((p_pos.x-p_width/2-self.width, p_pos.y - p_height - 5))
        if p_orientation == "r":
            return Vector((p_pos.x+p_width/2, p_pos.y - p_height - 5))