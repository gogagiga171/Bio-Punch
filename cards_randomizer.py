from classes.upgrades.SizeUpgrades import UBig, USmall
from classes.upgrades.PoisonUpgrades import UPoisonPunch, UDisease
import random

def get_cards():
    cards = ["Big", "Small", "PoisonPunch", "Disease"]
    choosen_cards = random.sample(cards, 3)
    return choosen_cards

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