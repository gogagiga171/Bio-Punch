import pygame
from settings import SERVER, SERVER_NOTE
import json
import threading
from classes.Button import Button
from classes.Vector import Vector
from settings import WIDTH, HEIGHT
from map import load_map
import socket
from game_states import game, loading, menu

pl1_inp = {"a":False, "d":False, "w":False, "o":False, "l":False}
pl2_inp = {"a":False, "d":False, "w":False, "o":False, "l":False}
player1, player2, map = load_map()
game_state = "menu"
s=0
N=0

def server_handler(s):
    global player1, player2, pl1_inp, pl2_inp, game_state, N
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
                        pl2_inp["o"] = False
                        pl2_inp["l"] = False
                    if N == 2:
                        pl1_inp = data["pl1_inp"]
                        pl1_inp["o"] = False
                        pl1_inp["l"] = False
                elif data["name"] == "ping":
                    s.send(json.dumps({"name":"ping"}).encode("utf-8")+b"\n")

def connect():
    global game_state, s, N
    game_state = "waiting for server"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_NOTE, 8000))
    th = threading.Thread(
        target=server_handler, args=(s,)
    )
    th.start()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_button = Button(Vector((200, 400)), 400, 100, "start game") #todo изменить магические числа
clock = pygame.time.Clock()
fps = 60
running = True
while running:
    delta = clock.tick(fps)/1000
    screen.fill((255, 255, 255))

    if game_state=="menu":
        running = menu(start_button, running, connect, screen)
    elif game_state=="game":
        running, pl1_inp, pl2_inp = game(player1, player2, pl1_inp, pl2_inp, delta, screen, s, running, map, N)
    else:
        running = loading(game_state, HEIGHT, WIDTH, screen, running)

    pygame.display.flip()