rank_display = {
    1: 'A',
    10: 'T',
    11: 'J',
    12: 'Q',
    13: 'K',
}

class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        if rank in rank_display.keys():
            # self.display = f'{ rank_display[rank] }{ suit }'
            self.display = rank_display[rank] + suit
        else:
            # self.display = f'{ rank }{ suit }'
            self.display = str(rank) + suit
    
    def __repr__(self):
        return self.display

    def __str__(self):
        return self.display
