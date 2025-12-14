import pygame
from settings import SERVER
import json
import threading
from classes import *
from settings import WIDTH, HEIGHT
from map import map
import socket

#подключаемся к серверу, получаем свою цифру
#ждём сигнал "game_start"
#делаем одельный поток чтобы с сервера хватать инфу
#запускаем игровой цикл
#отправляем нажатые клавиши при нажатии

pl1_inp = {"a":False, "d":False, "w":False}
pl2_inp = {"a":False, "d":False, "w":False}

def server_handler(s, N):
    global player1, player2, pl1_inp, pl2_inp
    while True:
        data = json.loads(s.recv(1024).decode("utf-8"))
        player1 = Player(0, 0).from_dict(data["player1"])
        player2 = Player(0, 0).from_dict(data["player2"])
        if N == 1:
            pl2_inp = data["pl2_inp"]
        if N == 2:
            pl1_inp = data["pl1_inp"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER, 8000))
N = int(s.recv(1024).decode("utf-8"))
print("подключился к серверу, я игрок", N)
if N == 1:
    print("жду игрока 2")
gs = s.recv(1024).decode("utf-8")
while gs != "game_start":
    gs = s.recv(1024).decode("utf-8")

th = threading.Thread(
    target=server_handler, args=(s, N)
)
th.start()

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fps = 60
running = True
player1 = Player(250, 350)
player2 = Player(350, 350)
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

    if N==1:
        player1.logic(keys, delta, map, Vector((0, 2000)))
        player2.logic(pl2_inp, delta, map, Vector((0, 2000)))
        if keys != pl1_inp:
            pl1_inp = keys
            s.send(json.dumps(pl1_inp).encode("utf-8"))
    else:
        player1.logic(pl1_inp, delta, map, Vector((0, 2000)))
        player2.logic(keys, delta, map, Vector((0, 2000)))
        if keys != pl2_inp:
            pl2_inp = keys
            s.send(json.dumps(pl2_inp).encode("utf-8"))

    player1.draw(screen)
    player2.draw(screen)
    for obs in map:
        obs.draw(screen)
    pygame.display.flip()