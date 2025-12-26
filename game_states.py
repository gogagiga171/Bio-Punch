import pygame
import json
import threading
from classes.Vector import Vector

def menu(start_button, running, connect, screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            m_pos = Vector(pygame.mouse.get_pos())
            if start_button.check_in_button(m_pos):
                threading.Thread(target=connect).start()

    start_button.draw(screen=screen)
    return running

def loading(game_state, HEIGHT, WIDTH, screen, running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    font_size = max(20, WIDTH // 10)
    font = pygame.font.Font(None, font_size)

    text_surface = font.render(game_state, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(text_surface, text_rect)
    return running

def game(player1, player2, pl1_inp, pl2_inp, delta, screen, s, running, map, N):
    pg_keys = pygame.key.get_pressed()
    keys = {
        "a": pg_keys[pygame.K_a],
        "d": pg_keys[pygame.K_d],
        "w": pg_keys[pygame.K_w],
        "i": pg_keys[pygame.K_i],
        "o": False,
        "l": False
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                keys["o"] = True
            if event.key == pygame.K_l:
                keys["l"] = True

    if N == 1:
        punch = player1.logic(keys, delta, map, player2, Vector((0, 2000)))
        player2.logic(pl2_inp, delta, map, player1, Vector((0, 2000)))
        if keys != pl1_inp:
            pl1_inp = keys
            data = {
                "name": "inp",
                "inp": pl1_inp,
                "punch": punch
            }
            s.send(json.dumps(data).encode("utf-8") + b"\n")
    else:
        player1.logic(pl1_inp, delta, map, player2, Vector((0, 2000)))
        punch = player2.logic(keys, delta, map, player1, Vector((0, 2000)))
        if keys != pl2_inp:
            pl2_inp = keys
            data = {
                "name": "inp",
                "inp": pl2_inp,
                "punch": punch
            }
            s.send(json.dumps(data).encode("utf-8") + b"\n")

    player1.draw(screen)
    player2.draw(screen)
    for obs in map:
        obs.draw(screen)

    return running, pl1_inp, pl2_inp