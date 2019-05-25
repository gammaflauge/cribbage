"""
A round is one cycle of deal, throw to crib, play hands,
score hands, score crib, and clean up.
"""


import random

from .card import Card
from .scoring import score_hand, stack_sum, score_stack


class Round(object):
    def __init__(self, game):
        self.cut_card = None
        self.crib = []
        self.deck = Card.build_deck()
        self.game = game
        for player in self.game.players:
            player.hand = []

    def __repr__(self):
        player_lines = ""
        for i, player in enumerate(self.game.players):
            player_lines += (
                f"{ '*' if i == self.game.dealer_seat else ' '} { player } "
                f"[{ player.score }] -- { player.hand }\n"
            )

        return (
            f"Round Number: { self.game.round_number }\n"
            f"{ player_lines }"
            f"  cut card -- { self.cut_card }\n"
            f"  crib -- { self.crib }"
        )

    def get_dealer(self):
        return self.game.players[self.game.dealer_seat]

    def deal(self):
        """
        Shuffles deck and passes out cards to each player.

        Players should have empty hands when deal is called, else
        assertion error will be raised
        """
        for player in self.game.players:
            assert player.hand == []

        random.shuffle(self.deck)
        for _ in range(self.game.cards_per_player):
            for player in self.game.players:
                player.hand.append(self.deck.pop())

    def collect_crib(self):
        """
        Calls on each player to select their cards to throw to the crib
        each round.

        If the crib is less than 4 cards after each player has throw in,
        collect crib will add cards from the top of the deck.
        """
        assert self.crib == [], "Crib already exists"

        for player in self.game.players:
            crib_cards = player.throw_to_crib()
            self.crib += crib_cards
            # player.hand = player_new_hand
        while len(self.crib) < 4:
            self.crib.append(self.deck.pop())

    def cut(self):
        """
        Select the cut card from the remaining cards in the deck.

        If a Jack is drawn, bubble back up to the game class to handle knobs.
        """
        assert self.cut_card is None, "Cut card already exists"

        self.cut_card = self.deck.pop()

        if self.cut_card.rank == 11:
            self.game.update_player_score(self.get_dealer(), 2)

    def get_player_turn(self, turn_number=1):
        """
        Return the player who's turn it is to play a card.

        The first turn is turn_number 1
        """
        return self.game.players[
            (self.game.dealer_seat + turn_number) % len(self.game.players)
        ]

    def play_hands(self):
        """
        Starting with the player to the right of the dealer, each player
        plays a card to the stack. Players can score points by making
        15s, pairs, or runs.

        This is repeated until all dealt cards are played.
        """
        # store a copy of player hands that we can restore to after
        # playeing out the hands
        for player in self.game.players:
            player.orig_hand = player.hand
        turn_number = 1
        player = self.get_player_turn(turn_number)
        stack = []
        said_go = 0

        while sum([len(player.hand) for player in self.game.players]) > 0:
            played_card = player.play_card(stack)
            turn_number += 1

            if played_card:
                last_to_play_card = player
                stack.append(played_card)
                self.game.update_player_score(player, score_stack(stack))
                said_go = 0
            else:
                said_go += 1

            if stack_sum(stack) == 31:
                stack = []
            elif said_go == len(self.game.players):
                # all players said go, original player gets a point
                self.game.update_player_score(last_to_play_card, 1)
                stack = []
                said_go = 0

            player = self.get_player_turn(turn_number)

        if stack_sum(stack) != 31:
            # last card played gets a point as long as it didnt hit 31
            self.game.update_player_score(last_to_play_card, 1)

        for player in self.game.players:
            player.hand = player.orig_hand

    def score_hands(self):
        """
        Start with the player to the right of the dealer (+1 in index terms),
        score each hand and add the points to the player total.

        If a player reaches the target score after scoring their hand, the
        game is immediately over.
        """
        assert self.cut_card is not None, "Cut card does not exist"

        for i in range(0, len(self.game.players)):
            # add 1 to players index so that we count dealer last
            player_to_count = self.get_player_turn(i + 1)
            points = score_hand(player_to_count.hand + [self.cut_card])
            self.game.update_player_score(player_to_count, points)
            if self.game.game_over:
                break  # stop counting immediately

    def score_crib(self):
        """
        Count the points for the crib, send back up to the game so
        that player score can be updated.
        """
        assert self.cut_card is not None, "Cut card does not exist"

        player = self.get_dealer()
        points = score_hand(self.crib + [self.cut_card])
        self.game.update_player_score(player, points)

    def run_round(self):
        """
        Execute all steps that make up a round of cribbage:
        """
        assert self.game.game_over == False, "Game already over"
        self.deal()
        self.collect_crib()
        self.cut()
        if not self.game.game_over:
            self.score_hands()
        if not self.game.game_over:
            self.score_crib()
