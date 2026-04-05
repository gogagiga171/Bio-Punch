import pygame
import json
import threading
from classes.Vector import Vector
from settings import GRAVITY

def auto_lining(text, font, width, x, y, screen):
    splited = text.split()
    texts = [splited[0]]

    for i in splited[1:]:
        if len(texts[-1]) + len(i) < width:
            texts[-1] += " " + i
        else:
            texts.append(i)

    for i, line in enumerate(texts):
        surface = font.render(line, True, (0, 0, 0))
        screen.blit(surface, (x, y + i * font.get_height()))

def menu(start_button, running, connect, screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if start_button.hovered:
                threading.Thread(target=connect).start()
    m_pos = Vector(pygame.mouse.get_pos())
    start_button.check_in_button(m_pos)
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
        "k": pg_keys[pygame.K_k],
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
        player1.logic(keys, delta, map, player2, GRAVITY)
        player2.logic(pl2_inp, delta, map, player1, GRAVITY)
        if keys != pl1_inp:
            pl1_inp = keys
            data = {
                "name": "inp",
                "inp": pl1_inp
            }
            s.send(json.dumps(data).encode("utf-8") + b"\n")
    else:
        player1.logic(pl1_inp, delta, map, player2, GRAVITY)
        player2.logic(keys, delta, map, player1, GRAVITY)
        if keys != pl2_inp:
            pl2_inp = keys
            data = {
                "name": "inp",
                "inp": pl2_inp
            }
            s.send(json.dumps(data).encode("utf-8") + b"\n")

    player1.draw(screen)
    player2.draw(screen)
    for obs in map:
        obs.draw(screen)

    if player1.health <= 0:
        game_state = "card_choosing"
        looser = 1
    elif player2.health <= 0:
        game_state = "card_choosing"
        looser = 2
    else:
        game_state = "game"
        looser = None

    return running, pl1_inp, pl2_inp, game_state, looser

def card_choosing(screen, s, cards_list, player1, player2, N, loser, running, WIDTH, HEIGHT, card_button_1, card_button_2, card_button_3, hovered_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP and N == loser:
            if card_button_1.hovered:
                pass
            if card_button_2.hovered:
                pass
            if card_button_3.hovered:
                pass

    m_pos = Vector(pygame.mouse.get_pos())
    if N == loser:
        card_button_1.check_in_button(m_pos)
        card_button_2.check_in_button(m_pos)
        card_button_3.check_in_button(m_pos)
        if card_button_1.hovered:
            if hovered_button != 1:
                hovered_button = 1
                data = {
                    "name": "hovered_button_changed",
                    "hovered_button": hovered_button
                }
                s.send(json.dumps(data).encode("utf-8") + b"\n")
        elif card_button_2.hovered:
            if hovered_button != 2:
                hovered_button = 2
                data = {
                    "name": "hovered_button_changed",
                    "hovered_button": hovered_button
                }
                s.send(json.dumps(data).encode("utf-8") + b"\n")
        elif card_button_3.hovered:
            if hovered_button != 3:
                hovered_button = 3
                data = {
                    "name": "hovered_button_changed",
                    "hovered_button": hovered_button
                }
                s.send(json.dumps(data).encode("utf-8") + b"\n")
        else:
            if hovered_button != 0:
                hovered_button = 0
                data = {
                    "name": "hovered_button_changed",
                    "hovered_button": hovered_button
                }
                s.send(json.dumps(data).encode("utf-8") + b"\n")
    else:
        card_button_1.hovered = False
        card_button_2.hovered = False
        card_button_3.hovered = False
        if hovered_button == 1:
            card_button_1.hovered = True
        if hovered_button == 2:
            card_button_2.hovered = True
        if hovered_button == 3:
            card_button_3.hovered = True

    for i in range(3):
        spl = (WIDTH - 600) / 4
        x = spl*(i+1) + 200*i
        y = 40
        pygame.draw.rect(screen, (0, 195, 255), (x-spl/3, 25, 200 + 2*spl/3, 500))
        pygame.draw.rect(screen, (255, 255, 255), (x-10, 255, 220 , 50))
        pygame.draw.rect(screen, (255, 255, 255), (x-10, 310, 220, 50))
        pygame.draw.rect(screen, (255, 255, 255), (x-10, 365, 220, 100))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 200, 200))
        screen.blit(cards_list[i].image, (x, y))
        title_font_size = 30
        font_size = 20
        title_font = pygame.font.Font(None, title_font_size)
        font = pygame.font.Font(None, font_size)
        card_button_1.draw(screen)
        card_button_2.draw(screen)
        card_button_3.draw(screen)
        auto_lining(cards_list[i].title, title_font, 20, x-5, 260, screen)
        auto_lining(cards_list[i].comment, font, 30, x-5, 315, screen)
        auto_lining(cards_list[i].description, font, 30, x-5, 370, screen)

    if N == loser:
        text = "Твой выбор"
    else:
        text = "Выбор противника"

    font_size = 50
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(WIDTH / 2, 550))
    screen.blit(text_surface, text_rect)

    return running, hovered_button