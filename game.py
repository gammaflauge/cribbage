import random

from card import Card
from player import Player


class Game(object):
    def __init__(self, player1, player2):
        self.hand_number = 0
        self.player1 = player1
        self.player2 = player2
        self.cut_card = None
        self.crib = []

        self.deck = []
        for suit in ["C", "D", "H", "S"]:
            for rank in range(1, 14):
                self.deck.append(Card(rank, suit))

    def __repr__(self):
        return (
            f"Hand Number: { self.hand_number }\n"
            f"  { self.player1 }\n"
            f"  { self.player2 }\n"
            f"  cut card -- { self.cut_card }\n"
            f"  crib -- { self.crib }"
        )

    def deal(self):
        random.shuffle(self.deck)
        self.player1.hand = self.deck[:6]
        self.player2.hand = self.deck[6:12]
        self.cut_card = self.deck[12]
        self.hand_number = self.hand_number + 1

    def throw_to_crib(self):
        self.crib = self.player1.hand[4:] + self.player2.hand[4:]
        self.player1.hand = self.player1.hand[:4]
        self.player2.hand = self.player2.hand[:4]

    def score(self):
        self.player1.score += Card.score_hand(self.player1.hand + [self.cut_card])
        self.player2.score += Card.score_hand(self.player2.hand + [self.cut_card])
