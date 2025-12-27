import pygame
from settings import WIDTH, HEIGHT
from map import load_map
from settings import GRAVITY

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 60
running = True
player, dummy, map = load_map()
while running:
    delta = clock.tick(fps)/1000
    screen.fill((255, 255, 255))

    pg_keys = pygame.key.get_pressed()
    keys = {
        "a": pg_keys[pygame.K_a],
        "d": pg_keys[pygame.K_d],
        "w": pg_keys[pygame.K_w],
        "i": pg_keys[pygame.K_i],
        "k": pg_keys[pygame.K_k],
        "o": False,
        "l": False
    }
    d_keys = {
        "a": False,
        "d": False,
        "w": False,
        "i": False,
        "k": False,
        "o": False,
        "l": False
    }

    for event in pygame.event.get():
        if event.type ==  pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                keys["o"] = True
            if event.key == pygame.K_l:
                keys["l"] = True


    player.logic(keys, delta, map, dummy, GRAVITY)
    dummy.logic(d_keys, delta, map, player, GRAVITY)

    if dummy.health <= 0 or player.health <= 0:
        player, dummy, map = load_map()

    player.draw(screen)
    if player.crouch:
        player.crouch_punch.draw_hitbox(player, screen)
        player.crouch_kick.draw_hitbox(player, screen)
    else:
        player.punch.draw_hitbox(player, screen)
        player.kick.draw_hitbox(player, screen)
    dummy.draw(screen)
    for obs in map:
        obs.draw(screen)
    pygame.display.flip()