from classes.Player import Player
from classes.upgrades.Upgrade import Upgrade

class UBig(Upgrade):
    title = "танк"
    size_multiplier = 1.5
    speed_multiplier = 0.7
    health_multiplier = 5
    description = "ХП x5, размер x1.5, скорость x0.8"
    comment = "капец жирный"

    def when_applied(self, player:Player):
        Player.height *= self.size_multiplier
        Player.width *= self.size_multiplier
        Player.speed *= self.speed_multiplier
        Player.maxHealth *= self.health_multiplier
        for i in player.animation_set.keys():
            player.animation_set[i].resize(self.size_multiplier)

class USmall(Upgrade):
    title = "мал да удал"
    size_multiplier = 0.8
    speed_multiplier = 3
    health_multiplier = 0.2
    description = "ХП x0.2, размер x0.8, скорость x3"
    comment = "Нурик"

    def when_applied(self, player:Player):
        Player.height *= self.size_multiplier
        Player.width *= self.size_multiplier
        Player.speed *= self.speed_multiplier
        Player.maxHealth *= self.health_multiplier
        for i in player.animation_set.keys():
            player.animation_set[i].resize(self.size_multiplier)