import random

from card import Card
from player import Player


class Game(object):
    def __init__(self, player_names):
        self.hand_number = 0
        self.cut_card = None
        self.crib = []

        self.deck = []
        for suit in ["C", "D", "H", "S"]:
            for rank in range(1, 14):
                self.deck.append(Card(rank, suit))

        if isinstance(player_names, list):
            self.players = [Player(name) for name in player_names]
        else:
            self.players = [Player(player_names)]

        if len(self.players) <= 2:
            self.cards_per_player = 6
        else:
            self.cards_per_player = 5

    def __repr__(self):
        player_lines = ''
        for player in self.players:
            player_lines += f"  { player }\n"

        return (
            f"Hand Number: { self.hand_number }\n"
            f"{ player_lines }"
            f"  cut card -- { self.cut_card }\n"
            f"  crib -- { self.crib }"
        )

    def deal(self):
        self.crib = []
        random.shuffle(self.deck)
        self.hand_number = self.hand_number + 1
        for pnum, player in enumerate(self.players):
            player.hand = self.deck[pnum * self.cards_per_player:pnum *
                                    self.cards_per_player + self.cards_per_player]
        self.cut_card = self.deck[-1]

    def throw_to_crib(self):
        for player in self.players:
            self.crib += player.hand[4:]
            player.hand = player.hand[:4]
        if len(self.crib) == 2:
            self.crib += self.deck[-3:-1]  # -1 is the cut card
        elif len(self.crib) == 3:
            self.crib += self.deck[-2:-1]  # -1 is the cut card

    def score(self):
        for player in self.players:
            player.score += Card.score_hand(player.hand + [self.cut_card])
