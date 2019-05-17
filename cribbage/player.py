'''
A Player is a contestant in the cribbage match.
'''

from .scoring import score_hand, stack_sum


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

    def play_card(self, stack):
        '''
        NaiveBot always plays the first card in their hand

        Returns None if no cards are legal plays
        '''
        for card in self.hand:
            if stack_sum(stack + [card]) <= 31:
                self.hand.remove(card)
                return card
        return None


class LowBot(Player):
    '''
    LowBot only wants low cards, always throws the highest cards to the crib.
    '''

    def __init__(self, name):
        super().__init__(name)

    def throw_to_crib(self):
        self.hand.sort(key=lambda x: x.rank)
        crib_cards = self.hand[4:]
        self.hand = self.hand[:4]
        return crib_cards

    def play_card(self, stack):
        '''
        LowBot wants to keep their low cards as long as possible, so she will
        always play the highest card in their hand if possible
        '''
        self.hand.sort(key=lambda x: x.rank)
        for card in self.hand:
            if stack_sum(stack + [card]) <= 31:
                self.hand.remove(card)
                return card
        return None


class HighBot(Player):
    def __init__(self, name):
        super().__init__(name)

    def throw_to_crib(self):
        '''
        HighBot only wants high cards, always throws the lowest cards to the crib.
        '''
        self.hand.sort(key=lambda x: -x.rank)
        crib_cards = self.hand[4:]
        self.hand = self.hand[:4]
        return crib_cards

    def play_card(self, stack):
        '''
        HighBot wants to keep their high cards as long as possible, so she will
        always play the lowest card in their hand if possible
        '''
        self.hand.sort(key=lambda x: -x.rank)
        for card in self.hand:
            if stack_sum(stack + [card]) <= 31:
                self.hand.remove(card)
                return card
        return None
