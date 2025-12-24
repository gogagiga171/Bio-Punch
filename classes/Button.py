from classes.Vector import Vector
import pygame

class Button:

    def __init__(self, _pos: Vector, _width: int, _height: int, _text: str, _color=(255, 255, 255), _outline_color=(150, 150, 150)):
        self.pos = _pos
        self.width = _width
        self.height = _height
        self.text = _text
        self.color = _color
        self.outline_color = _outline_color
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.outline_color, self.rect, width=2, border_radius=5)

        font_size = max(20, self.height // 3)
        font = pygame.font.Font(None, font_size)

        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def check_in_button(self, _pos):
        return (self.pos.x < _pos.x < self.pos.x + self.width) and (self.pos.y < _pos.y < self.pos.y + self.height)