import unittest

from cribbage.player.player import Player
from cribbage.player.robot import NaiveBot, LowBot, HighBot
from cribbage.card import Card


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.sam = Player("sam")

    def test_init(self):
        self.assertEqual(self.sam.name, "sam")

    def test_str(self):
        self.assertEqual(str(self.sam), "sam")

    def test_throw_to_crib(self):
        with self.assertRaises(NotImplementedError):
            self.sam.throw_to_crib()


class TestNaiveBot(unittest.TestCase):
    def setUp(self):
        self.sam = NaiveBot("sam")

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


class TestLowBot(unittest.TestCase):
    def setUp(self):
        self.sam = LowBot("sam")

    def test_throw_to_crib_6(self):
        self.sam.hand = Card.build_deck()[:6]
        crib_cards = self.sam.throw_to_crib()
        self.assertEqual(len(self.sam.hand), 4)
        self.assertEqual(len(crib_cards), 2)
        self.assertIsInstance(crib_cards, list)

        self.assertEqual(self.sam.hand[0].rank, 1)
        self.assertEqual(self.sam.hand[1].rank, 2)
        self.assertEqual(self.sam.hand[2].rank, 3)
        self.assertEqual(self.sam.hand[3].rank, 4)
        self.assertEqual(crib_cards[0].rank, 5)
        self.assertEqual(crib_cards[1].rank, 6)

    def test_throw_to_crib_5(self):
        self.sam.hand = Card.build_deck()[11:16]
        crib_cards = self.sam.throw_to_crib()
        self.assertEqual(len(self.sam.hand), 4)
        self.assertEqual(len(crib_cards), 1)
        self.assertIsInstance(crib_cards, list)

        self.assertEqual(self.sam.hand[0].rank, 1)
        self.assertEqual(self.sam.hand[1].rank, 2)
        self.assertEqual(self.sam.hand[2].rank, 3)
        self.assertEqual(self.sam.hand[3].rank, 12)
        self.assertEqual(crib_cards[0].rank, 13)

    def test_throw_to_crib_4(self):
        self.sam.hand = Card.build_deck()[:4]
        crib_cards = self.sam.throw_to_crib()
        self.assertEqual(len(self.sam.hand), 4)
        self.assertEqual(len(crib_cards), 0)
        self.assertIsInstance(crib_cards, list)


class TestHighBot(unittest.TestCase):
    def setUp(self):
        self.sam = HighBot("sam")

    def test_throw_to_crib_6(self):
        # AC, 2C, 3C, 4C, 5C, 6C -> should throw AC, 2C
        self.sam.hand = Card.build_deck()[:6]
        crib_cards = self.sam.throw_to_crib()
        self.assertEqual(len(self.sam.hand), 4)
        self.assertEqual(len(crib_cards), 2)
        self.assertIsInstance(crib_cards, list)

        self.assertEqual(self.sam.hand[0].rank, 6)
        self.assertEqual(self.sam.hand[1].rank, 5)
        self.assertEqual(self.sam.hand[2].rank, 4)
        self.assertEqual(self.sam.hand[3].rank, 3)
        self.assertEqual(crib_cards[0].rank, 2)
        self.assertEqual(crib_cards[1].rank, 1)

    def test_throw_to_crib_5(self):
        #  QC, KC, AD, 2D, 3D -> should throw AD
        self.sam.hand = Card.build_deck()[11:16]
        crib_cards = self.sam.throw_to_crib()
        self.assertEqual(len(self.sam.hand), 4)
        self.assertEqual(len(crib_cards), 1)
        self.assertIsInstance(crib_cards, list)

        self.assertEqual(self.sam.hand[0].rank, 13)
        self.assertEqual(self.sam.hand[1].rank, 12)
        self.assertEqual(self.sam.hand[2].rank, 3)
        self.assertEqual(self.sam.hand[3].rank, 2)
        self.assertEqual(crib_cards[0].rank, 1)

    def test_throw_to_crib_4(self):
        self.sam.hand = Card.build_deck()[:4]
        crib_cards = self.sam.throw_to_crib()
        self.assertEqual(len(self.sam.hand), 4)
        self.assertEqual(len(crib_cards), 0)
        self.assertIsInstance(crib_cards, list)
