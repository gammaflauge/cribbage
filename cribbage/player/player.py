"""
A Player is a contestant in the cribbage match.
"""


class Player(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []

    def __repr__(self):
        return f"{ self.name }"

    def throw_to_crib(self):
        raise NotImplementedError

    def play_card(self, stack):
        raise NotImplementedError
