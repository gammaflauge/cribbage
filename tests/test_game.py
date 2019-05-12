import unittest
import random

from cribbage.game import Game
from cribbage.player import NaiveBot
from cribbage.game import Round


class TestGame(unittest.TestCase):
    def setUp(self):
        p1 = NaiveBot("char")
        p2 = NaiveBot("sam")
        p3 = NaiveBot("zee")
        p4 = NaiveBot("daisy")

        self.game_1p = Game(p1)
        self.game_2p = Game([p1, p2])
        self.game_3p = Game([p1, p2, p3])
        self.game_4p = Game([p1, p2, p3, p4])
        self.all_games = [self.game_1p,
                          self.game_2p, self.game_3p, self.game_4p]

    def test_init_cards_per_player(self):
        self.assertEqual(self.game_1p.cards_per_player, 6)
        self.assertEqual(self.game_2p.cards_per_player, 6)
        self.assertEqual(self.game_3p.cards_per_player, 5)
        self.assertEqual(self.game_4p.cards_per_player, 5)

    def test_score(self):
        random.seed(512019)
        # first hand
        Round(self.game_4p).run_round()
        self.assertEqual(self.game_4p.scores["char"], 13)
        self.assertEqual(self.game_4p.scores["sam"], 4)
        self.assertEqual(self.game_4p.scores["zee"], 9)
        self.assertEqual(self.game_4p.scores["daisy"], 0)

        # second hand
        r1 = Round(self.game_4p)
        r1.run_round()
        self.assertEqual(self.game_4p.scores["char"], 25)
        self.assertEqual(self.game_4p.scores["sam"], 12)
        self.assertEqual(self.game_4p.scores["zee"], 15)
        self.assertEqual(self.game_4p.scores["daisy"], 2)

    def test_score_at_endgame(self):
        random.seed(512019)
        # sam should count first and score 4 points
        # zee should score 9 points game and end the game
        self.game_4p.scores["zee"] = 111
        Round(self.game_4p).run_round()
        self.assertTrue(self.game_4p.game_over)
        self.assertEqual(self.game_4p.scores["char"], 0)
        self.assertEqual(self.game_4p.scores["sam"], 4)
        self.assertEqual(self.game_4p.scores["zee"], 120)
        self.assertEqual(self.game_4p.scores["daisy"], 0)

    def test_end_round(self):
        self.assertEqual(self.game_4p.dealer_seat, 0)
        self.assertEqual(self.game_4p.round_number, 1)
        self.game_4p.end_round()
        self.assertEqual(self.game_4p.dealer_seat, 1)
        self.assertEqual(self.game_4p.round_number, 2)
        self.game_4p.end_round()
        self.game_4p.end_round()
        self.game_4p.end_round()
        self.assertEqual(self.game_4p.dealer_seat, 0)
        self.assertEqual(self.game_4p.round_number, 5)

    def test_sim_game(self):
        for game in self.all_games:
            game.sim_game()
            self.assertTrue(game.game_over)
            self.assertIsNotNone(game.winner)
