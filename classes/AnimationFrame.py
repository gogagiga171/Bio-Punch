from collections.abc import Callable
from os import PathLike
import pygame
from classes.Vector import Vector
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.Player import Player

class AnimationFrame:
    image: pygame.Surface
    w: float
    h: float
    offset: Vector
    code: Callable | None
    player: "Player"

    def __init__(self, _file_path:PathLike, _offset:Vector, size:float, _code:Callable | None, _player: "Player"):
        self.image = pygame.image.load(_file_path).convert_alpha()
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(w * size), int(h * size)))
        self.offset = _offset
        self.code = _code
        self.player = _player

    def draw(self, pos:Vector, screen:pygame.surface.Surface):
        screen.blit(self.image, (pos.x+self.offset.x, pos.y+self.offset.y))

    def execute_code(self):
        if not self.code is None:
            self.code()