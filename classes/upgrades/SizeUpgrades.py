from classes.Player import Player, ServerSidePlayer
from classes.upgrades.Upgrade import Upgrade, ServerUpgrade

class SUBig(ServerUpgrade):
    size_multiplier = 1.5
    speed_multiplier = 0.9
    health_multiplier = 5

    def when_applied(self, player:Player|ServerSidePlayer):
        player.height *= self.size_multiplier
        player.width *= self.size_multiplier
        player.speed *= self.speed_multiplier
        player.maxHealth *= self.health_multiplier

class SUSmall(ServerUpgrade):
    size_multiplier = 0.8
    speed_multiplier = 1.25
    health_multiplier = 0.2

    def when_applied(self, player:Player):
        player.height *= self.size_multiplier
        player.width *= self.size_multiplier
        player.speed *= self.speed_multiplier
        player.maxHealth *= self.health_multiplier

class UBig(Upgrade):
    image_name = "UBig.png"
    title = "танк"
    size_multiplier = 1.5
    speed_multiplier = 0.7
    health_multiplier = 5
    description = "ХП x5, размер x1.5, скорость x0.8"
    comment = "капец жирный"

    def when_applied(self, player:Player):
        player.height *= self.size_multiplier
        player.width *= self.size_multiplier
        player.speed *= self.speed_multiplier
        player.maxHealth *= self.health_multiplier
        for i in player.animation_set.keys():
            player.animation_set[i].resize(self.size_multiplier)

class USmall(Upgrade):
    image_name = "USmall.png"
    title = "мал да удал"
    size_multiplier = 0.8
    speed_multiplier = 3
    health_multiplier = 0.2
    description = "ХП x0.2, размер x0.8, скорость x3"
    comment = "Нурик"

    def when_applied(self, player:Player):
        player.height *= self.size_multiplier
        player.width *= self.size_multiplier
        player.speed *= self.speed_multiplier
        player.maxHealth *= self.health_multiplier
        for i in player.animation_set.keys():
            player.animation_set[i].resize(self.size_multiplier)