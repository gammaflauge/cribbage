'''
A Player is a contestant in the cribbage match.
'''

from .scoring import score_hand, stack_count


class Player(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{ self.name }"

    def throw_to_crib(self, my_hand):
        raise NotImplementedError

    def play_card(self, my_hand, stack):
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

    def play_card(self, my_hand, stack):
        '''
        NaiveBot always plays the first card in their hand

        Returns None if no cards are legal plays
        '''
        for card in my_hand:
            if stack_count(stack + [card]) <= 31:
                return card
        return None


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

    def play_card(self, my_hand, stack):
        '''
        LowBot wants to keep their low cards as long as possible, so she will
        always play the highest card in their hand if possible
        '''
        my_hand.sort(key=lambda x: x.rank)
        for card in my_hand:
            if stack_count(stack + [card]) <= 31:
                return card
        return None


class HighBot(Player):
    def __init__(self, name):
        super().__init__(name)

    def throw_to_crib(self, my_hand):
        '''
        HighBot only wants high cards, always throws the lowest cards to the crib.
        '''
        my_hand.sort(key=lambda x: -x.rank)
        crib_cards = my_hand[4:]
        my_hand = my_hand[:4]
        return crib_cards, my_hand

    def play_card(self, my_hand, stack):
        '''
        HighBot wants to keep their high cards as long as possible, so she will
        always play the lowest card in their hand if possible
        '''
        my_hand.sort(key=lambda x: -x.rank)
        for card in my_hand:
            if stack_count(stack + [card]) <= 31:
                return card
        return None
