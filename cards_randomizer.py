from classes.upgrades.SizeUpgrades import UBig, USmall, SUBig, SUSmall
from classes.upgrades.PoisonUpgrades import UPoisonPunch, UDisease, SUPoisonPunch, SUDisease
import random

def get_cards():
    cards = ["Big", "Small", "PoisonPunch", "Disease"]
    choosen_cards = random.sample(cards, 3)
    return choosen_cards

def load_server_cards(cards):
    cards_dict = {
        "Big": SUBig(),
        "Small": SUSmall(),
        "PoisonPunch": SUPoisonPunch(),
        "Disease": SUDisease()
    }

    cards_list = []
    for card in cards:
        cards_list.append(cards_dict[card])
    return cards_list

def load_cards(cards):
    cards_dict = {
        "Big": UBig(),
        "Small": USmall(),
        "PoisonPunch": UPoisonPunch(),
        "Disease": UDisease()
    }

    cards_list = []
    for card in cards:
        cards_list.append(cards_dict[card])
    return cards_list