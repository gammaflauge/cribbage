'''
A card has a rank and a suit.
52 of these make a deck
'''


class Card(object):
    suits = ["C", "D", "H", "S"]
    ranks = range(1, 14)
    rank_display = {1: "A", 10: "T", 11: "J", 12: "Q", 13: "K"}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        if rank in Card.rank_display.keys():
            # self.display = f'{ rank_display[rank] }{ suit }'
            self.display = Card.rank_display[rank] + suit
        else:
            # self.display = f'{ rank }{ suit }'
            self.display = str(rank) + suit

    def __repr__(self):
        return self.display

    def __str__(self):
        return self.display

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.rank == other.rank) and (self.suit == other.suit)
        else:
            return False

    @staticmethod
    def build_deck():
        """
        build and return a stand 52-card deck.
        """
        deck = []
        for suit in Card.suits:
            for rank in Card.ranks:
                deck.append(Card(rank, suit))
        return deck
