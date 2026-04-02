import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.Player import Player

class Effect:
    duration: float
    start: float
    player: "Player"

    def __init__(self, player: "Player"):
        self.player = player
        self.start = time.time()

    def process(self):
        if time.time() - self.start >= self.duration:
            return True
        return False

class Poison(Effect):
    duration = 3
    damage = 10
    last_damage: float
    reload = 1


    def __init__(self, player: "Player"):
        self.last_damage = time.time()
        super().__init__(player)

    def process(self):
        if time.time() - self.last_damage >= self.reload:
            Player.health -= self.damage
        super().process()