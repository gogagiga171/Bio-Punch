from classes.Player import Player
from classes.upgrades.Upgrade import Upgrade
from classes.Effects import Poison

class UPoisonPunch(Upgrade):
    image_name = "UPoisonPunch.png"
    title = "Отравленый удар"
    description = "При ударе накладывает отравление. Дамаг от удара x0.5"
    comment = "Неприятный тип"
    punch_effect = Poison
    damage_multiplier = 0.5

    def when_applied(self, player:Player):
        Player.punch_effects.append(self.punch_effect)
        Player.punch.damage *= self.damage_multiplier
        Player.kick.damage *= self.damage_multiplier
        Player.crouch_punch.damage *= self.damage_multiplier
        Player.crouch_kick.damage *= self.damage_multiplier
        Player.flight_punch.damage *= self.damage_multiplier
        Player.flight_kick.damage *= self.damage_multiplier

class UDisease(Upgrade):
    image_name = "UDisease.png"
    title = "Коронавирус"
    description = "При ударе накладывает отравление. ХП x0.5"
    comment = "контрится медицинской маской"
    punch_effect = Poison
    health_multiplier = 0.5

    def when_applied(self, player:Player):
        Player.punch_effects.append(self.punch_effect)
        Player.maxHealth *= self.health_multiplier