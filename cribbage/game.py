from .card import Card
from .player import Player
from .round import Round


class Game(object):
    def __init__(self, players):
        if not isinstance(players, list):
            raise RuntimeError("players argument must be a list")

        self.players = players
        self.round_number = 1
        self.dealer_seat = 0
        self.goal_score = 120
        self.game_over = False
        self.winner = None
        self.scores = {}

        if len(self.players) <= 2:
            self.cards_per_player = 6
        else:
            self.cards_per_player = 5

        for player in players:
            player.score = 0
            player.hand = []

    def __repr__(self):
        player_lines = ''
        for i, player in enumerate(self.players):
            player_lines += f"{ '*' if i == self.dealer_seat else ' '} { player }\n"

        return (
            f"Round Number: { self.round_number }\n"
            f"{ player_lines }"
        )

    def update_player_score(self, player, points):
        player.score += points
        if player.score >= self.goal_score:
            self.declare_winner(player)

    def declare_winner(self, player):
        self.winner = player
        self.game_over = True

    def end_round(self):
        self.round_number += 1
        self.dealer_seat = (self.dealer_seat + 1) % len(self.players)

    def sim_game(self):
        assert (self.game_over == False), "Game already over!"

        Round(self).run_round()
        while not self.game_over:
            self.end_round()
            Round(self).run_round()
