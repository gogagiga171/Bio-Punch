from collections.abc import Callable
from os import PathLike
import pygame
from classes.Vector import Vector

class AnimationFrame:
    def __init__(self, _file_path:PathLike, _offset:Vector, _code:Callable or None, _player):
        self.image = pygame.image.load(_file_path).convert_alpha()
        k = 20
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w / k), int(h / k)))
        self.offset = _offset
        self.code = _code
        self.player = _player

    def draw(self, pos:Vector, screen:pygame.surface.Surface):
        screen.blit(self.image, (pos.x+self.offset.x, pos.y+self.offset.y))
        self.execute_code()

    def execute_code(self):
        if self.code is Callable:
            self.code(self.player, self.player.enemy)