'''
A Player is a contestant in the cribbage match.
'''

from .scoring import score_hand


class Player(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{ self.name }"

    def throw_to_crib(self, my_hand):
        raise NotImplementedError


class NaiveBot(Player):
    '''
    NaiveBot acts as if they know the rules but
    has no understanding of strategy.
    '''

    def __init__(self, name):
        super().__init__(name)

    def throw_to_crib(self, my_hand):
        '''
        NaiveBot will always keeps their first four
        cards and tosses the rest.
        '''
        crib_cards = my_hand[4:]
        my_hand = my_hand[:4]
        return crib_cards, my_hand


class LowBot(Player):
    '''
    LowBot only wants low cards, always throws the highest cards to the crib.
    '''

    def __init__(self, name):
        super().__init__(name)

    def throw_to_crib(self, my_hand):
        my_hand.sort(key=lambda x: x.rank)
        crib_cards = my_hand[4:]
        my_hand = my_hand[:4]
        return crib_cards, my_hand


class HighBot(Player):
    '''
    HighBot only wants high cards, always throws the lowest cards to the crib.
    '''

    def __init__(self, name):
        super().__init__(name)

    def throw_to_crib(self, my_hand):
        my_hand.sort(key=lambda x: -x.rank)
        crib_cards = my_hand[4:]
        my_hand = my_hand[:4]
        return crib_cards, my_hand
