import random

from .card import Card
from .player import Player


class Game(object):
    def __init__(self, player_names):
        self.hand_number = 0
        self.dealer_seat = 0
        self.cut_card = None
        self.crib = []
        self.goal_score = 120
        self.game_over = False
        self.deck = Card.build_deck()

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
        for i, player in enumerate(self.players):
            player_lines += f"{ '*' if i == self.dealer_seat else ' '} { player }\n"

        return (
            f"Hand Number: { self.hand_number }\n"
            f"{ player_lines }"
            f"  cut card -- { self.cut_card }\n"
            f"  crib -- { self.crib }"
        )

    def deal(self):
        random.shuffle(self.deck)
        self.hand_number = self.hand_number + 1
        for pnum, player in enumerate(self.players):
            index_card = pnum * self.cards_per_player
            player.set_hand(
                self.deck[index_card:index_card + self.cards_per_player])

    def collect_crib(self):
        for player in self.players:
            self.crib += player.throw_to_crib()
        if len(self.crib) == 2:
            self.crib += self.deck[-3:-1]  # -1 is the cut card
        elif len(self.crib) == 3:
            self.crib += self.deck[-2:-1]  # -1 is the cut card

    def cut(self):
        self.cut_card = self.deck[-1]
        if self.cut_card.rank == 11:
            self.players[self.dealer_seat].update_score(2)

    def score_hands(self):
        for i in range(0, len(self.players)):
            # add 1 to players index so that we count dealer last
            player_to_count = (i + self.dealer_seat + 1) % len(self.players)
            player = self.players[player_to_count]
            player.score_hand(self.cut_card)
            if player.is_winner(self.goal_score):
                self.game_over = True
                break  # stop counting immediately
            # count the crib points for the dealer
            if player_to_count == self.dealer_seat:
                player.update_score(Card.score_hand(
                    self.crib + [self.cut_card]))
                if player.is_winner(self.goal_score):
                    self.game_over = True
                    break  # stop counting immediately

    def clean_up_hand(self):
        self.dealer_seat = (self.dealer_seat + 1) % len(self.players)
        for player in self.players:
            player.hand = []
        self.cut_card = None
        self.crib = []

    def check_if_winner(self, player):
        return player.score >= self.goal_score

    def sim_game(self):
        while not self.game_over:
            self.clean_up_hand()
            self.deal()
            self.collect_crib()
            self.cut()
            self.score_hands()
