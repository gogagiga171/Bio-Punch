import pygame
from settings import WIDTH, HEIGHT
from map import map
from classes import Player, Obstacle, Line, Vector

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 60
running = True
player = Player(350, 350)
dummy = Player(450, 350)
while running:
    delta = clock.tick(fps)/1000
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            running = False
    pg_keys = pygame.key.get_pressed()
    keys = {
        "a": pg_keys[pygame.K_a],
        "d": pg_keys[pygame.K_d],
        "w": pg_keys[pygame.K_w]
    }
    d_keys = {
        "a": False,
        "d": False,
        "w": False
    }

    player.logic(keys, delta, map, Vector((0, 2000)))
    dummy.logic(d_keys, delta, map, Vector((0, 2000)))

    player.draw(screen)
    dummy.draw(screen)
    for obs in map:
        obs.draw(screen)
    pygame.display.flip()