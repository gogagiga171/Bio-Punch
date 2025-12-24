import pygame
from classes.Vector import Vector
import socket
import json
import time
import threading
from map import load_map
from settings import MESSAGE_DELTA

pl1_inp = {"a":False, "d":False, "w":False, "o":False, "l":False}
pl2_inp = {"a":False, "d":False, "w":False, "o":False, "l":False}
pl1_ping = 0
pl2_ping = 0
pl1_ping_fetched = False
pl2_ping_fetched = False
pl1_ping_timer_start = 0
pl2_ping_timer_start = 0

def send_info(conn1, conn2, player1, player2, pl1_inp, pl2_inp, health=False):
    data = {
        "name": "info",
        "player1": player1.convert_quick_dict(),
        "player2": player2.convert_quick_dict(),
        "pl1_inp": pl1_inp,
        "pl2_inp": pl2_inp
    }

    if health:
        data["player1"]["health"] = player1.health
        data["player2"]["health"] = player2.health

    data_bytes = json.dumps(data).encode("utf-8")
    conn1.send(data_bytes + b"\n")
    conn2.send(data_bytes + b"\n")

def ping_sender(conn, pl):
    global pl1_ping_fetched, pl2_ping_fetched, pl1_ping_timer_start, pl2_ping_timer_start
    conn.send(json.dumps({"name":"ping"}).encode("utf-8")+b"\n")
    if pl == 1:
        pl1_ping_timer_start = time.time()
        pl1_ping_fetched = False
        while not pl1_ping_fetched:
            time.sleep(1)
    if pl == 2:
        pl2_ping_timer_start = time.time()
        pl2_ping_fetched = False
        while not pl2_ping_fetched:
            time.sleep(2)

def client_handler(p1, p2, cl, conn, enemy_conn, addr):
    global pl1_inp, pl2_inp, player1, player2
    global pl1_ping, pl2_ping, pl1_ping_fetched, pl2_ping_fetched
    global pl1_ping_timer_start, pl2_ping_timer_start
    while True:
        buffer = ""
        while True:
            chunk = conn.recv(1024).decode("utf-8")
            buffer += chunk
            while "\n" in buffer:
                data, buffer = buffer.split("\n", 1)
                if data.strip():
                    try:
                        data = json.loads(data)
                    except json.JSONDecodeError:
                        print("упс проблема с json")
                        continue

                    if data["name"] == "inp":
                        if cl == 1:
                            pl1_inp = data["inp"]
                            if data["punch"]["punch"]:
                                punched = player1.punch.hit(player1, player2, -player1.vel*pl1_ping)
                                if punched:
                                    send_info(conn, enemy_conn, player1, player2, pl1_inp, pl2_inp, health=True)
                            if data["punch"]["kick"]:
                                punched = player1.kick.hit(player1, player2, -player1.vel * pl1_ping)
                                if punched:
                                    send_info(conn, enemy_conn, player1, player2, pl1_inp, pl2_inp, health=True)
                        if cl == 2:
                            pl2_inp = data["inp"]
                            if data["punch"]["punch"]:
                                punched = player2.punch.hit(player2, player1, -player2.vel*pl2_ping)
                                if punched:
                                    send_info(conn, enemy_conn, player1, player2, pl1_inp, pl2_inp, health=True)
                            if data["punch"]["kick"]:
                                punched = player2.kick.hit(player2, player1, -player2.vel*pl2_ping)
                                if punched:
                                    send_info(conn, enemy_conn, player1, player2, pl1_inp, pl2_inp, health=True)
                    if data["name"] == "ping":
                        if cl == 1:
                            pl1_ping = time.time()-pl1_ping_timer_start
                            pl1_ping_fetched = True
                        if cl == 2:
                            pl2_ping = time.time()-pl2_ping_timer_start
                            pl2_ping_fetched = True


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 8000))
s.listen()

conn1, addr1 = s.accept()
conn1.send(b"1\n")
conn2, addr2 = s.accept()
conn2.send(b"2\n")

conn1.send(b"game_start\n")
conn2.send(b"game_start\n")

player1, player2, map = load_map()

th1 = threading.Thread(
    target=client_handler, args=(player1, player2, 1, conn1, conn2, addr1)
)
th2 = threading.Thread(
    target=client_handler, args=(player1, player2, 2, conn2, conn1, addr2)
)
th1.start()
th2.start()

th1 = threading.Thread(
    target=ping_sender, args=(conn1, 1)
)
th2 = threading.Thread(
    target=ping_sender, args=(conn2, 2)
)
th1.start()
th2.start()

pygame.init()
clock = pygame.time.Clock()
fps = 60
start = time.time()
while True:
    delta = clock.tick(fps) / 1000

    player1.logic(pl1_inp, delta, map, player2, Vector((0, 2000)))
    player2.logic(pl2_inp, delta, map, player1, Vector((0, 2000)))

    if time.time()-start>MESSAGE_DELTA:
        send_info(conn1, conn2, player1, player2, pl1_inp, pl2_inp)
        start = time.time()

    if player1.health <= 0 or player2.health <= 0:
        player1, player2, map = load_map()
        send_info(conn1, conn2, player1, player2, pl1_inp, pl2_inp, health=True)