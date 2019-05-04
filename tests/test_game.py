import unittest

from game import Game
from player import Player


class TestGame(unittest.TestCase):
    def setUp(self):
        self.my_game = Game("p1", "p2")
