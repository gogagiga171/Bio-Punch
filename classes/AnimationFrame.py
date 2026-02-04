from collections.abc import Callable

import pygame
from classes.Vector import Vector

class AnimationFrame:
    def __init__(self, _file_path:str, _offset:Vector, _code:Callable):
        self.image = pygame.image.load(_file_path).convert_alpha()
        self.offset = _offset
        self.code = _code

    def draw(self, pos:Vector, screen:pygame.surface.Surface):
        screen.blit(self.image, (pos.x+self.offset.x, pos.y+self.offset.y))
        self.code()

    def execute_code(self):
        self.code()