import pygame
import json
import threading
from classes import *
from settings import WIDTH, HEIGHT

def main():
    #server = Server(SERVER)
    #server.connect()
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 60
    running = True
    player = Player()
    floor = Obstacle([
        Vector((100, 400)), Vector((700, 400)), Vector((700, 500)), Vector((100, 500))
    ])
    map = [floor]

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
        player.logic(keys, delta, map, Vector((0, 2000)))
        player.draw(screen)
        for obs in map:
            obs.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()