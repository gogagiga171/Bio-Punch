
class Block:
    block: bool
    damage_resist: float
    knock_back_resist: float
    stun_resist: float

    def __init__(self):
        self.block = False
        self.damage_resist = 0.8
        self.knock_back_resist = 0.5
        self.stun_resist = 0.5