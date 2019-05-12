'''
A round is one cycle of deal, throw to crib, play hands,
score hands, score crib, and clean up.
'''


import random

from .card import Card
from .scoring import score_hand


class Round(object):
    def __init__(self, game):
        self.cut_card = None
        self.crib = []
        self.deck = Card.build_deck()
        self.game = game
        self.player_hands = {}

        for player in self.game.players:
            self.player_hands[player.name] = []

    def __repr__(self):
        player_lines = ''
        for i, player in enumerate(self.game.players):
            player_lines += (
                f"{ '*' if i == self.game.dealer_seat else ' '} { player } "
                f"[{ self.game.scores[player.name] }]"
                f" -- { self.player_hands[player.name] }\n")

        return (
            f"Round Number: { self.game.round_number }\n"
            f"{ player_lines }"
            f"  cut card -- { self.cut_card }\n"
            f"  crib -- { self.crib }"
        )

    def get_dealer_name(self):
        return self.game.players[self.game.dealer_seat].name

    def deal(self):
        '''
        Shuffles deck and passes out cards to each player.

        Players should have empty hands when deal is called, else
        assertion error will be raised
        '''
        for player in self.game.players:
            assert (self.player_hands[player.name] == [])

        random.shuffle(self.deck)
        for _ in range(self.game.cards_per_player):
            for player in self.game.players:
                self.player_hands[player.name].append(self.deck.pop())

    def collect_crib(self):
        '''
        Calls on each player to select their cards to throw to the crib
        each round.

        If the crib is less than 4 cards after each player has throw in,
        collect crib will add cards from the top of the deck.
        '''
        assert (self.crib == []), "Crib already exists"

        for player in self.game.players:
            crib_cards, player_new_hand = player.throw_to_crib(
                self.player_hands[player.name])
            self.crib += crib_cards
            self.player_hands[player.name] = player_new_hand
        while len(self.crib) < 4:
            self.crib.append(self.deck.pop())

    def cut(self):
        '''
        Select the cut card from the remaining cards in the deck.

        If a Jack is drawn, bubble back up to the game class to handle knobs.
        '''
        assert (self.cut_card is None), "Cut card already exists"

        self.cut_card = self.deck.pop()

        if self.cut_card.rank == 11:
            self.game.update_player_score(self.get_dealer_name(), 2)

    def score_hands(self):
        '''
        Start with the player to the right of the dealer (+1 in index terms),
        score each hand and add the points to the player total.

        If a player reaches the target score after scoring their hand, the
        game is immediately over.
        '''
        assert (self.cut_card is not None), "Cut card does not exist"

        for i in range(0, len(self.game.players)):
            # add 1 to players index so that we count dealer last
            player_to_count = (i + self.game.dealer_seat +
                               1) % len(self.game.players)
            player_name = self.game.players[player_to_count].name
            points = score_hand(
                self.player_hands[player_name] + [self.cut_card])
            self.game.update_player_score(player_name, points)
            if self.game.game_over:
                break  # stop counting immediately

    def score_crib(self):
        '''
        Count the points for the crib, send back up to the game so
        that player score can be updated.
        '''
        assert (self.cut_card is not None), "Cut card does not exist"

        player_name = self.get_dealer_name()
        points = score_hand(self.crib + [self.cut_card])
        self.game.update_player_score(player_name, points)

    def run_round(self):
        '''
        Execute all steps that make up a round of cribbage:
        '''
        assert (self.game.game_over == False), "Game already over"
        self.deal()
        self.collect_crib()
        self.cut()
        if not self.game.game_over:
            self.score_hands()
        if not self.game.game_over:
            self.score_crib()
