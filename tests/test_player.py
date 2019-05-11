import unittest

from cribbage.player import Player
from cribbage.card import Card


class TestGame(unittest.TestCase):
    def setUp(self):
        self.sam = Player("sam")

    def test_init(self):
        self.assertEqual(self.sam.score, 0)
        self.assertEqual(self.sam.name, "sam")
        self.assertEqual(len(self.sam.hand), 0)

    def test_str(self):
        self.assertEqual(str(self.sam), "sam [0] -- []")

    def test_update_score(self):
        self.assertEqual(self.sam.score, 0)
        self.sam.update_score(10)
        self.assertEqual(self.sam.score, 10)
        self.sam.update_score(5)
        self.assertEqual(self.sam.score, 15)
        self.sam.update_score(0)
        self.assertEqual(self.sam.score, 15)

    def test_is_winner(self):
        self.sam.score = 119
        self.assertFalse(self.sam.is_winner(goal_score=120))
        self.assertTrue(self.sam.is_winner(goal_score=119))

    def test_throw_to_crib_6(self):
        self.sam.hand = Card.build_deck()[:6]
        crib_cards = self.sam.throw_to_crib()
        self.assertEqual(len(self.sam.hand), 4)
        self.assertEqual(len(crib_cards), 2)
        self.assertIsInstance(crib_cards, list)

    def test_throw_to_crib_5(self):
        self.sam.hand = Card.build_deck()[:5]
        crib_cards = self.sam.throw_to_crib()
        self.assertEqual(len(self.sam.hand), 4)
        self.assertEqual(len(crib_cards), 1)
        self.assertIsInstance(crib_cards, list)

    def test_throw_to_crib_4(self):
        self.sam.hand = Card.build_deck()[:4]
        crib_cards = self.sam.throw_to_crib()
        self.assertEqual(len(self.sam.hand), 4)
        self.assertEqual(len(crib_cards), 0)
        self.assertIsInstance(crib_cards, list)

    def test_score_hand(self):
        self.sam.hand = Card.build_deck()[:4]  # AC 2C 3C 4C = 8
        self.sam.score = 0
        self.sam.score_hand()
        self.assertEqual(self.sam.score, 8)
        self.sam.score_hand(Card(5, "C"))
        self.assertEqual(self.sam.score, 20)  # 8 + 12

    def test_set_hand(self):
        self.sam.set_hand(Card.build_deck()[:4])
        self.assertEqual(len(self.sam.hand), 4)
        for i, card in enumerate(Card.build_deck()[:4]):
            self.assertEqual(card.rank, self.sam.hand[i].rank)
            self.assertEqual(card.suit, self.sam.hand[i].suit)

    def test_discard_hand(self):
        self.sam.hand = Card.build_deck()[:4]
        self.sam.discard_hand()
        self.assertEqual(len(self.sam.hand), 0)
