import unittest
import random

from game import Game
from card import Card
from player import Player


class TestGame(unittest.TestCase):
    def setUp(self):
        p1 = "char"
        p2 = "sam"
        p3 = "zee"
        p4 = "daisy"

        self.game_1p = Game(p1)
        self.game_2p = Game([p1, p2])
        self.game_3p = Game([p1, p2, p3])
        self.game_4p = Game([p1, p2, p3, p4])
        self.all_games = [self.game_1p,
                          self.game_2p, self.game_3p, self.game_4p]

    def test_init_deck(self):
        for game in self.all_games:
            self.assertEqual(len(game.deck), 52)
            for suit in ["C", "H", "S", "D"]:
                card_count = len(
                    [card for card in game.deck if card.suit == suit])
                self.assertEqual(card_count, 13)
            for rank in range(1, 14):
                card_count = len(
                    [card for card in game.deck if card.rank == rank])
                self.assertEqual(card_count, 4)

    def test_init_cards_per_player(self):
        self.assertEqual(self.game_1p.cards_per_player, 6)
        self.assertEqual(self.game_2p.cards_per_player, 6)
        self.assertEqual(self.game_3p.cards_per_player, 5)
        self.assertEqual(self.game_4p.cards_per_player, 5)

    def test_deal(self):
        for game in self.all_games:
            self.assertIsNone(game.cut_card)
            for player in game.players:
                self.assertEqual(len(player.hand), 0)
            game.deal()
            for player in game.players:
                self.assertEqual(len(player.hand), game.cards_per_player)
            self.assertIsNone(game.cut_card)

    def test_cut(self):
        for game in self.all_games:
            self.assertIsNone(game.cut_card)
            game.deal()
            self.assertIsNone(game.cut_card)
            game.cut()
            self.assertIsNotNone(game.cut_card)
            self.assertIsInstance(game.cut_card, Card)

    def test_cut_knobs(self):
        random.seed(512019)
        self.game_4p.deal()
        self.game_4p.throw_to_crib()
        self.game_4p.cut()
        self.assertEqual(self.game_4p.players[0].score, 2)
        self.assertEqual(self.game_4p.players[1].score, 0)
        self.assertEqual(self.game_4p.players[2].score, 0)
        self.assertEqual(self.game_4p.players[3].score, 0)

    def test_cut_no_knobs(self):
        random.seed(1032015)
        self.game_4p.deal()
        self.game_4p.throw_to_crib()
        self.game_4p.cut()
        self.assertEqual(self.game_4p.players[0].score, 0)
        self.assertEqual(self.game_4p.players[1].score, 0)
        self.assertEqual(self.game_4p.players[2].score, 0)
        self.assertEqual(self.game_4p.players[3].score, 0)

    def test_throw_to_crib(self):
        for game in self.all_games:
            for _ in range(0, 5):
                game.deal()
                game.throw_to_crib()
                for player in game.players:
                    self.assertEqual(len(player.hand), 4)
                self.assertEqual(len(game.crib), 4)

    def test_score(self):
        random.seed(512019)
        self.game_4p.deal()
        self.game_4p.throw_to_crib()
        self.game_4p.cut()
        self.game_4p.score()

        self.assertEqual(self.game_4p.players[0].score, 6)
        self.assertEqual(self.game_4p.players[1].score, 10)
        self.assertEqual(self.game_4p.players[2].score, 2)
        self.assertEqual(self.game_4p.players[3].score, 9)

        self.game_4p.deal()
        self.game_4p.throw_to_crib()
        self.game_4p.cut()
        self.game_4p.score()

        self.assertEqual(self.game_4p.players[0].score, 12)
        self.assertEqual(self.game_4p.players[1].score, 16)
        self.assertEqual(self.game_4p.players[2].score, 7)
        self.assertEqual(self.game_4p.players[3].score, 11)
