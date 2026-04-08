from classes.Player import Player
from classes.upgrades.Upgrade import Upgrade, ServerUpgrade
from classes.Effects import Poison

class SUPoisonPunch(ServerUpgrade):
    punch_effect = Poison
    damage_multiplier = 0.5

    def when_applied(self, player:Player):
        player.punch_effects.append(self.punch_effect)
        player.punch.damage *= self.damage_multiplier
        player.kick.damage *= self.damage_multiplier
        player.crouch_punch.damage *= self.damage_multiplier
        player.crouch_kick.damage *= self.damage_multiplier
        player.flight_punch.damage *= self.damage_multiplier
        player.flight_kick.damage *= self.damage_multiplier

class SUDisease(ServerUpgrade):
    punch_effect = Poison
    health_multiplier = 0.5

    def when_applied(self, player:Player):
        player.punch_effects.append(self.punch_effect)
        player.maxHealth *= self.health_multiplier

class UPoisonPunch(Upgrade):
    image_name = "UPoisonPunch.png"
    title = "Отравленый удар"
    description = "При ударе накладывает отравление. Дамаг от удара x0.5"
    comment = "Неприятный тип"
    punch_effect = Poison
    damage_multiplier = 0.5

    def when_applied(self, player:Player):
        player.punch_effects.append(self.punch_effect)
        player.punch.damage *= self.damage_multiplier
        player.kick.damage *= self.damage_multiplier
        player.crouch_punch.damage *= self.damage_multiplier
        player.crouch_kick.damage *= self.damage_multiplier
        player.flight_punch.damage *= self.damage_multiplier
        player.flight_kick.damage *= self.damage_multiplier

class UDisease(Upgrade):
    image_name = "UDisease.png"
    title = "Коронавирус"
    description = "При ударе накладывает отравление. ХП x0.5"
    comment = "контрится медицинской маской"
    punch_effect = Poison
    health_multiplier = 0.5

    def when_applied(self, player:Player):
        player.punch_effects.append(self.punch_effect)
        player.maxHealth *= self.health_multiplier