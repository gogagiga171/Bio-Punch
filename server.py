import pygame
import socket
import json
import time
import threading
from map import load_map
from settings import MESSAGE_DELTA, GRAVITY
from classes.Player import ServerSidePlayer
from cards_randomizer import get_cards, load_server_cards

pl1_inp = {"a":False, "d":False, "w":False, "i": False, "k":False, "o":False, "l":False}
pl2_inp = {"a":False, "d":False, "w":False, "i": False, "k":False, "o":False, "l":False}
cards = []
choosing_card = False

class PingManager:
    pl1_ping = 0
    pl2_ping = 0
    pl1_ping_fetched = False
    pl2_ping_fetched = False
    pl1_ping_timer_start = 0
    pl2_ping_timer_start = 0

pm = PingManager

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
    global pm
    conn.send(json.dumps({"name":"ping"}).encode("utf-8")+b"\n")
    if pl == 1:
        pm.pl1_ping_timer_start = time.time()
        pm.pl1_ping_fetched = False
        while not pm.pl1_ping_fetched:
            time.sleep(2)
    if pl == 2:
        pm.pl2_ping_timer_start = time.time()
        pm.pl2_ping_fetched = False
        while not pm.pl2_ping_fetched:
            time.sleep(2)

def client_handler(p1, p2, cl, conn, enemy_conn, addr):
    global pl1_inp, pl2_inp, player1, player2, map
    global pm, choosing_card
    global cards
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
                            send_info(conn, enemy_conn, player1, player2, pl1_inp, pl2_inp, health=False)
                        if cl == 2:
                            pl2_inp = data["inp"]
                            send_info(conn, enemy_conn, player1, player2, pl1_inp, pl2_inp, health=False)
                    if data["name"] == "punch":
                        if cl == 1:
                            if data["type"] == "punch":
                                punched = player1.punch.hit(player1.punch_effects, player1.vel*pm.pl1_ping)
                            if data["type"] == "kick":
                                punched = player1.kick.hit(player1.punch_effects, player1.vel*pm.pl1_ping)
                            if data["type"] == "flight_punch":
                                punched = player1.flight_punch.hit(player1.punch_effects, player1.vel*pm.pl1_ping)
                            if data["type"] == "flight_kick":
                                punched = player1.flight_kick.hit(player1.punch_effects, player1.vel*pm.pl1_ping)
                            if data["type"] == "crouch_punch":
                                punched = player1.crouch_punch.hit(player1.punch_effects, player1.vel*pm.pl1_ping)
                            if data["type"] == "crouch_kick":
                                punched = player1.crouch_kick.hit(player1.punch_effects, player1.vel*pm.pl1_ping)
                            if punched:
                                new_data = {
                                    "name": "punched",
                                    "punch": data["type"]
                                }
                                enemy_conn.send(json.dumps(new_data).encode("utf-8") + b"\n")
                        if cl == 2:
                            if data["type"] == "punch":
                                punched = player2.punch.hit(player2.punch_effects, player2.vel*pm.pl2_ping)
                            if data["type"] == "kick":
                                punched = player2.kick.hit(player2.punch_effects, player2.vel*pm.pl2_ping)
                            if data["type"] == "flight_punch":
                                punched = player2.flight_punch.hit(player2.punch_effects, player2.vel*pm.pl2_ping)
                            if data["type"] == "flight_kick":
                                punched = player2.flight_kick.hit(player2.punch_effects, player2.vel*pm.pl2_ping)
                            if data["type"] == "crouch_punch":
                                punched = player2.crouch_punch.hit(player2.punch_effects, player2.vel*pm.pl2_ping)
                            if data["type"] == "crouch_kick":
                                punched = player2.crouch_kick.hit(player2.punch_effects, player2.vel*pm.pl2_ping)
                            if punched:
                                new_data = {
                                    "name": "punched",
                                    "punch": data["type"]
                                }
                                enemy_conn.send(json.dumps(new_data).encode("utf-8") + b"\n")
                    if data["name"] == "ping":
                        if cl == 1:
                            pm.pl1_ping = time.time()-pm.pl1_ping_timer_start
                            pm.pl1_ping_fetched = True
                        if cl == 2:
                            pm.pl2_ping = time.time()-pm.pl2_ping_timer_start
                            pm.pl2_ping_fetched = True
                    if data["name"] == "hovered_button_changed":
                        enemy_conn.send(json.dumps(data).encode("utf-8") + b"\n")
                    if data["name"] == "choosen_card":
                        enemy_conn.send(json.dumps(data).encode("utf-8") + b"\n")
                        l_cards = load_server_cards(cards)
                        if cl == 1:
                            l_cards[data["choosen_card"]-1].when_applied(p1)
                            p1.upgrades.append(l_cards[data["choosen_card"]-1])
                        elif cl == 2:
                            l_cards[data["choosen_card"]-1].when_applied(p2)
                            p2.upgrades.append(l_cards[data["choosen_card"]-1])
                        player1, player2, map = load_map(player1, player2)
                        choosing_card = False



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 8000))
s.listen()

conn1, addr1 = s.accept()
conn1.send(b"1\n")
conn2, addr2 = s.accept()
conn2.send(b"2\n")

conn1.send(b"game_start\n")
conn2.send(b"game_start\n")

player1 = ServerSidePlayer(350, 350, "r")
player2 = ServerSidePlayer(450, 350, "l")
player1.enemy = player2
player2.enemy = player1
player1, player2, map = load_map(player1, player2)

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

    player1.logic(pl1_inp, delta, map, player2, GRAVITY)
    player2.logic(pl2_inp, delta, map, player1, GRAVITY)

    if time.time()-start>MESSAGE_DELTA:
        send_info(conn1, conn2, player1, player2, pl1_inp, pl2_inp)
        start = time.time()

    if player1.health <= 0 or player2.health <= 0:
        cards = get_cards()
        data = {
            "name": "cards_list",
            "cards": cards
        }
        conn1.send(json.dumps(data).encode("utf-8") + b"\n")
        conn2.send(json.dumps(data).encode("utf-8") + b"\n")
        choosing_card = True
        while choosing_card:
            pass