import unittest
import random

from cribbage.card import Card
from cribbage.game import Game
from cribbage.player.robot import NaiveBot
from cribbage.round import Round


class TestRound(unittest.TestCase):
    def setUp(self):
        self.p1 = NaiveBot("sam")
        self.p2 = NaiveBot("char")
        self.p3 = NaiveBot("daisy")
        self.p4 = NaiveBot("zee")
        self.game_1p = Game([self.p1])
        self.game_2p = Game([self.p1, self.p2])
        self.game_3p = Game([self.p1, self.p2, self.p3])
        self.game_4p = Game([self.p1, self.p2, self.p3, self.p4])

    def test_init(self):
        my_round = Round(self.game_4p)
        self.assertListEqual(my_round.game.players[0].hand, [])
        self.assertListEqual(my_round.game.players[1].hand, [])
        self.assertListEqual(my_round.game.players[2].hand, [])
        self.assertListEqual(my_round.game.players[3].hand, [])
        self.assertListEqual(my_round.crib, [])

    def test_repr(self):
        pass

    def test_deal(self):
        round_1 = Round(self.game_4p)
        round_1.deal()
        self.assertEqual(len(round_1.game.players[0].hand), 5)
        self.assertEqual(len(round_1.game.players[3].hand), 5)
        self.assertListEqual(round_1.crib, [])
        self.assertIsNone(round_1.cut_card)

        round_2 = Round(self.game_2p)
        round_2.deal()
        self.assertEqual(len(round_2.game.players[0].hand), 6)
        self.assertEqual(len(round_2.game.players[1].hand), 6)
        self.assertListEqual(round_2.crib, [])
        self.assertIsNone(round_2.cut_card)

    def test_collect_crib(self):
        round_1 = Round(self.game_4p)
        round_1.deal()
        round_1.collect_crib()
        self.assertEqual(len(round_1.game.players[0].hand), 4)
        self.assertEqual(len(round_1.game.players[3].hand), 4)
        self.assertEqual(len(round_1.crib), 4)

        round_2 = Round(self.game_4p)
        round_2.deal()
        round_2.collect_crib()
        self.assertEqual(len(round_1.game.players[0].hand), 4)
        self.assertEqual(len(round_1.game.players[0].hand), 4)
        self.assertEqual(len(round_1.crib), 4)

    def test_cut(self):
        round_1 = Round(self.game_2p)
        self.assertEqual(self.game_2p.players[0].score, 0)
        self.assertIsNone(round_1.cut_card)
        round_1.cut()
        self.assertEqual(self.game_2p.players[0].score, 0)
        self.assertIsNotNone(round_1.cut_card)

        # looking for knobs
        while round_1.cut_card.rank != 11:
            round_1.cut_card = None
            round_1.cut()

        self.assertEqual(self.game_2p.players[0].score, 2)
        self.assertEqual(self.game_2p.players[1].score, 0)
        self.assertIsInstance(round_1.cut_card, Card)

    def test_score_hands(self):
        random.seed(1123)
        my_round = Round(self.game_4p)
        my_round.deal()
        my_round.collect_crib()
        my_round.cut()
        my_round.score_hands()
        self.assertEqual(self.game_4p.players[0].score, 4)
        self.assertEqual(self.game_4p.players[1].score, 2)
        self.assertEqual(self.game_4p.players[2].score, 8)
        self.assertEqual(self.game_4p.players[3].score, 2)

    def test_score_crib(self):
        random.seed(1123)
        my_round = Round(self.game_4p)
        my_round.deal()
        my_round.collect_crib()
        my_round.cut()
        my_round.score_crib()
        self.assertEqual(self.game_4p.players[0].score, 5)
        self.assertEqual(self.game_4p.players[1].score, 0)
        self.assertEqual(self.game_4p.players[2].score, 0)
        self.assertEqual(self.game_4p.players[3].score, 0)

    def test_run_round(self):
        random.seed(1123)
        my_round = Round(self.game_4p)
        my_round.deal()
        my_round.collect_crib()
        my_round.cut()
        my_round.score_hands()
        my_round.score_crib()
        self.assertEqual(self.game_4p.players[0].score, 9)
        self.assertEqual(self.game_4p.players[1].score, 2)
        self.assertEqual(self.game_4p.players[2].score, 8)
        self.assertEqual(self.game_4p.players[3].score, 2)

    def test_play_hands(self):
        random.seed(1123)
        # 'sam': [5D, AC, 6D, 6H], 'char': [7D, TS, 7S, 9S], 'daisy': [TH, 3C, 5C, KH], 'zee': [7H, 4H, JC, AD]
        my_round = Round(self.game_4p)
        my_round.deal()
        my_round.collect_crib()
        my_round.cut()
        my_round.play_hands()
        self.assertEqual(self.game_4p.players[0].score, 4)
        self.assertEqual(self.game_4p.players[1].score, 2)
        self.assertEqual(self.game_4p.players[2].score, 1)
        self.assertEqual(self.game_4p.players[3].score, 2)
