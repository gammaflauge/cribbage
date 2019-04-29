from itertools import combinations


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

    @staticmethod
    def flush_check(cards):
        if not isinstance(cards, list):
            raise RuntimeError("flush_check needs a list")
        if len(cards) <= 1:
            raise RuntimeWarning("flush_check received a list of len 1")

        for card in cards[1:]:
            if card.suit != cards[0].suit:
                return False
        return True

    @staticmethod
    def pair_count(cards):
        if not isinstance(cards, list):
            raise RuntimeError("pair_count needs a list")
        if len(cards) <= 1:
            raise RuntimeWarning("pair_count received a list of len 1")

        pairs = 0
        for i in range(0, len(cards) - 1):
            my_rank = cards[i].rank
            pairs = pairs + len(
                [c for c in cards[i+1:] if c.rank == my_rank])
        return pairs

    @staticmethod
    def fifteen_count(cards):
        if not isinstance(cards, list):
            raise RuntimeError("flush_check needs a list")
        if len(cards) <= 1:
            raise RuntimeWarning("flush_check received a list of len 1")

        fifteens = 0
        ranks = []
        for card in cards:
            if card.rank > 10:
                ranks.append(10)
            else:
                ranks.append(card.rank)

        for i in range(2, len(ranks) + 1):
            for combo in combinations(ranks, i):
                if sum(combo) == 15:
                    fifteens += 1
                # print(f"combo = { combo }, sum(combo) = { sum(combo) }, fifteens = { fifteens }")

        return fifteens

    @staticmethod
    def run_count(cards):
        if not isinstance(cards, list):
            raise RuntimeError("run_count needs a list")

        print(cards)
        if Card._check_if_run(cards):
            print(f"returning: { len(cards) } for { cards }")
            return len(cards)
        elif len(cards) == 3:
            return 0
        else:
            run_count = 0
            for combo in combinations(cards, len(cards) - 1):
                print(combo)
                run_count += Card.run_count(list(combo))
            return run_count

    @staticmethod
    def _check_if_run(cards):
        if len(cards) < 3:
            return False

        ranks = sorted([card.rank for card in cards])
        for i in range(1, len(ranks)):
            if ranks[i] - ranks[i-1] != 1:
                return False

        return True
