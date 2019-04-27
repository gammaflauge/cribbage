import random

from card import Card


class Game(object):
    def __init__(self, player1, player2):
        self.hand_number = 0
        self.player1 = player1
        self.player1_hand = []
        self.player1_score = 0
        self.player2 = player2
        self.player2_hand = []
        self.player2_score = 0
        self.cut_card = None
        self.crib = []

        self.deck = []
        for suit in ['C', 'D', 'H', 'S']:
            for rank in range(1,14):
                self.deck.append(Card(rank, suit))


    def __repr__(self):
        state = 'Hand Number ' + str(self.hand_number) + '\n'
        state = state + self.player1 + ' [' + str(self.player1_score) + '] -- '
        state = state + ' '.join([str(c) for c in self.player1_hand]) + '\n'
        state = state + self.player2 + ' [' + str(self.player2_score) + '] -- '
        state = state + ' '.join([str(c) for c in self.player2_hand]) + '\n'
        state = state + 'cut card -- ' + str(self.cut_card)
        return state


    def deal(self):
        random.shuffle(self.deck)
        self.player1_hand = self.deck[:6]
        self.player2_hand = self.deck[6:12]
        self.cut_card = self.deck[12]
        self.hand_number = self.hand_number + 1


    def score(self):
        hand_score = 0
        # check for flush
        flush = True
        for card in self.player1_hand[1:]:
            if card.suit != self.player1_hand[0].suit:
                flush = False
        if flush:
            if self.cut_card.suit == self.player1_hand[0].suit:
                hand_score = hand_score + 5
            else:
                hand_score = hand_score + 4

        # count pairs
        pairs = 0
        for i in range(0, len(self.player1_hand) - 1):
            my_rank = self.player1_hand[i].rank
            pairs = pairs + len(
                [c for c in self.player1_hand[i+1:] if c.rank == my_rank])
        hand_score = hand_score + 2 * pairs

        # count 15s
        # check for run

        # return the score
        self.player1_score = self.player1_score + hand_score