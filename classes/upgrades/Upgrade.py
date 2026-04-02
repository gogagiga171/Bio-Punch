from classes.Player import Player
from pygame import Surface
import pygame

class Upgrade:
    title: str
    image: Surface
    image_path = "resources/upgrades/"
    image_name: str
    description: str
    comment: str

    def __init__(self):
        self.image = pygame.image.load(self.image_path + self.image_name).convert_alpha()
        w, h = self.image.get_size()
        size = 1/2
        self.image = pygame.transform.scale(self.image, (int(w * size), int(h * size)))

    def when_applied(self, player:Player):
        pass

    def logic(self, player:Player):
        pass