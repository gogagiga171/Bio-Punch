import pygame
from classes import *
import socket
import json
import time
import threading
from map import map
from settings import MESSAGE_DELTA

#ожидаем подключение двух игроков пока не подключаться у игроков экран (ожидание второго игрока)
#отправить сообщения о начале игры и id игроков
#получать от игроков сообщения с input
#отправлять 20 раз в секунду местоположение всех объектов

player1 = Player(250, 350)
player2 = Player(350, 350)
pl1_inp = {"a":False, "d":False, "w":False}
pl2_inp = {"a":False, "d":False, "w":False}

def client_handler(p1, p2, cl, conn, addr):
    global pl1_inp, pl2_inp
    while True:
        data = conn.recv(1024)
        if cl == 1:
            pl1_inp = json.loads(data.decode("utf-8"))
        if cl == 2:
            pl2_inp = json.loads(data.decode("utf-8"))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 8000))
s.listen()

conn1, addr1 = s.accept()
conn1.send(b"1")
conn2, addr2 = s.accept()
conn2.send(b"2")

conn1.send(b"game_start")
conn2.send(b"game_start")

th1 = threading.Thread(
    target=client_handler, args=(player1, player2, 1, conn1, addr1)
)
th2 = threading.Thread(
    target=client_handler, args=(player1, player2, 2, conn2, addr2)
)
th1.start()
th2.start()

pygame.init()
clock = pygame.time.Clock()
fps = 60
start = time.time()
while True:
    delta = clock.tick(fps) / 1000

    player1.logic(pl1_inp, delta, map, Vector((0, 2000)))
    player2.logic(pl2_inp, delta, map, Vector((0, 2000)))

    if time.time()-start>MESSAGE_DELTA:
        data = {
            "player1": player1.convert_dict(),
            "player2": player2.convert_dict(),
            "pl1_inp": pl1_inp,
            "pl2_inp": pl2_inp
        }
        data_bytes = json.dumps(data).encode("utf-8")
        conn1.send(data_bytes)
        conn2.send(data_bytes)
        start = time.time()
