import pygame
from settings import SERVER, SERVER_NOTE
import json
import threading
from classes.Button import Button
from classes.Vector import Vector
from classes.Player import Player
from settings import WIDTH, HEIGHT
from map import load_map
import socket
from game_states import game, loading, menu, card_choosing
from cards_randomizer import load_cards

class HoveredButton:
    a = 0

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_button = Button(Vector((200, 400)), 400, 100, "start game") #todo изменить магические числа
y = 470
card_button_1 = Button(Vector((50, y)), 200, 50, "choose", _hovered_color=(255, 136, 0), _outline_width=6)
card_button_2 = Button(Vector((300, y)), 200, 50, "choose", _hovered_color=(255, 136, 0), _outline_width=6)
card_button_3 = Button(Vector((550, y)), 200, 50, "choose", _hovered_color=(255, 136, 0), _outline_width=6)
clock = pygame.time.Clock()
fps = 60
running = True
cards_list = []
loser = None
hovered_button = HoveredButton

pl1_inp = {"a":False, "d":False, "w":False, "i":False, "k":False, "o":False, "l":False}
pl2_inp = {"a":False, "d":False, "w":False, "i":False, "k":False, "o":False, "l":False}

player1 = Player(350, 350, "r")
player2 = Player(450, 350, "l")
player1.enemy = player2
player2.enemy = player1
player1, player2, map = load_map(player1, player2)

game_state = "menu"
s=0
N=0

def server_handler(s):
    global player1, player2, pl1_inp, pl2_inp, game_state, N, cards_list, hovered_button, map
    buffer = ""
    while True:
        chunk = s.recv(1024).decode("utf-8")
        buffer += chunk
        while "\n" in buffer:
            data, buffer = buffer.split("\n", 1)
            if data.strip():
                if data == "game_start":
                    game_state = "game"
                    continue
                elif data == "1" or data == "2":
                    N=int(data)
                    game_state = "waiting for player"
                    if N == 1:
                        player1.update_sockets(s)
                        player2.update_punches_real_player(False)
                    else:
                        player2.update_sockets(s)
                        player1.update_punches_real_player(False)
                    continue

                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    print("упс проблема с json")
                    continue

                if data["name"] == "info":
                    player1.update_from_dict(data["player1"])
                    player2.update_from_dict(data["player2"])
                    if N == 1:
                        pl2_inp = data["pl2_inp"]
                    if N == 2:
                        pl1_inp = data["pl1_inp"]
                elif data["name"] == "ping":
                    s.send(json.dumps({"name":"ping"}).encode("utf-8")+b"\n")
                elif data["name"] == "cards_list":
                    cards_list = load_cards(data["cards"])
                elif data["name"] == "hovered_button_changed":
                    hovered_button.a = data["hovered_button"]
                elif data["name"] == "choosen_card":
                    if N == 1:
                        cards_list[data["choosen_card"]-1].when_applied(player1)
                        player1.upgrades.append(cards_list[data["choosen_card"]-1])
                    if N == 2:
                        cards_list[data["choosen_card"]-1].when_applied(player2)
                        player2.upgrades.append(cards_list[data["choosen_card"]-1])
                    player1, player2, map = load_map(player1, player2)
                    game_state = "game"

def connect():
    global game_state, s, N
    game_state = "waiting for server"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_NOTE, 8000))
    th = threading.Thread(
        target=server_handler, args=(s,)
    )
    th.start()

while running:
    delta = clock.tick(fps)/1000
    screen.fill((255, 255, 255))

    if game_state=="menu":
        running = menu(start_button, running, connect, screen)
    elif game_state=="game":
        running, pl1_inp, pl2_inp, game_state, loser = game(player1, player2, pl1_inp, pl2_inp, delta, screen, s, running, map, N)
    elif game_state=="card_choosing" and len(cards_list) != 0:
        running, hovered_button, game_state, reload = card_choosing(screen, s, cards_list, player1, player2, N, loser, running, WIDTH, HEIGHT, card_button_1, card_button_2, card_button_3, hovered_button, game_state) #todo
        if reload:
            player1, player2, map = load_map(player1, player2)
    else:
        running = loading(game_state, HEIGHT, WIDTH, screen, running)

    pygame.display.flip()