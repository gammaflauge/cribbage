import unittest

from player import Player


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
