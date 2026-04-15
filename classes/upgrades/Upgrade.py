from classes.Player import Player
from pygame import Surface
import pygame

class ServerUpgrade:

    def __init__(self):
        pass

    def when_applied(self, player: Player):
        pass

    def logic(self, player: Player):
        pass

    def trigger(self, player: Player):
        pass

class Upgrade (ServerUpgrade):
    image: Surface
    image_path = "resources/upgrades/"
    image_name: str

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(self.image_path + self.image_name).convert_alpha()
        w, h = self.image.get_size()
        size = 1/2
        self.image = pygame.transform.scale(self.image, (int(w * size), int(h * size)))