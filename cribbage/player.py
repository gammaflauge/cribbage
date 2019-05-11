'''
A Player is a contestant in the cribbage match.
'''

from .card import Card


class Player(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []

    def __repr__(self):
        return f"{ self.name } [{ self.score }] -- {self.hand }"

    def update_score(self, points):
        self.score += points

    def is_winner(self, goal_score):
        return self.score >= goal_score

    def throw_to_crib(self):
        raise NotImplementedError

    def score_hand(self, cut_card=None):
        '''
        Takes the players hand and a cut_card
        Updates player score and returns the number of points
        '''
        if cut_card:
            points = Card.score_hand(self.hand + [cut_card])
        else:
            points = Card.score_hand(self.hand)

        self.update_score(points)
        return points

    def set_hand(self, cards):
        '''
        accepts a list of cards
        '''
        self.hand = cards

    def discard_hand(self):
        '''
        remove all cards from Players hand
        usually done at the end of the round
        '''
        self.hand = []


class NaiveBot(Player):
    '''
    NaiveBot acts as if they know the rules but
    has no understanding of strategy.
    '''

    def __init__(self, name):
        super().__init__(name)

    def throw_to_crib(self):
        '''
        NaiveBot will always keeps their first four
        cards and tosses the rest.
        '''
        crib_cards = self.hand[4:]
        self.hand = self.hand[:4]
        return crib_cards
