"""A class to deal cards from"""

from .cards import cards
import random

class Deck():
    def __init__(self):
        self.used_cards = []

    def flip_card(self):
        idx = random.randint(0, 51)
        while idx in self.used_cards:
            idx = random.randint(0, 51)
        self.used_cards.append(idx)
        return cards[idx]