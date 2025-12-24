from classes.Line import Line
import pygame

class Obstacle:
    def __init__(self, dots):
        self.lines = [Line(dots[x], dots[x+1]) for x in range(len(dots)-1)]
        self.lines.append(Line(dots[0], dots[-1]))
        self.dots = dots

    def tuple_dots(self):
        td = []
        for dot in self.dots:
            td.append((dot.x, dot.y))
        return td

    def draw(self, screen):
        pygame.draw.polygon(screen, (100, 100, 100), self.tuple_dots())