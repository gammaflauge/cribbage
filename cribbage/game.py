from .card import Card
from .player import Player
from .round import Round


class Game(object):
    def __init__(self, players):
        self.round_number = 1
        self.dealer_seat = 0
        self.goal_score = 120
        self.game_over = False
        self.winner = None
        self.scores = {}

        if isinstance(players, list):
            self.players = players
        else:
            self.players = [players]

        if len(self.players) <= 2:
            self.cards_per_player = 6
        else:
            self.cards_per_player = 5

        for player in self.players:
            self.scores[player.name] = 0

    def __repr__(self):
        player_lines = ''
        for i, player in enumerate(self.players):
            player_lines += f"{ '*' if i == self.dealer_seat else ' '} { player }\n"

        return (
            f"Round Number: { self.round_number }\n"
            f"{ player_lines }"
        )

    def update_player_score(self, player_name, points):
        self.scores[player_name] += points
        if self.scores[player_name] >= self.goal_score:
            self.declare_winner(player_name)

    def declare_winner(self, player_name):
        self.winner = player_name
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
