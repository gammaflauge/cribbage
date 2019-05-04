from itertools import combinations


rank_display = {1: "A", 10: "T", 11: "J", 12: "Q", 13: "K"}


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
            pairs = pairs + \
                len([c for c in cards[i + 1:] if c.rank == my_rank])
        return pairs

    @staticmethod
    def fifteen_count(cards):
        if not isinstance(cards, list):
            raise RuntimeError("flush_check needs a list")
        if len(cards) <= 1:
            raise RuntimeWarning("flush_check received a list of len 1")

        fifteens = 0
        ranks = [card.rank if card.rank < 10 else 10 for card in cards]

        for i in range(2, len(ranks) + 1):
            for combo in combinations(ranks, i):
                if sum(combo) == 15:
                    fifteens += 1
                # print(f"combo = { combo }, sum(combo) = { sum(combo) }, fifteens = { fifteens }")

        return fifteens

    @staticmethod
    def run_count(cards):
        all_ranks = [card.rank for card in cards]
        uniq_ranks = sorted(set(all_ranks))

        run = []
        run_len_to_find = len(uniq_ranks)
        while run_len_to_find >= 3 and len(run) == 0:
            for start_card in range(0, len(uniq_ranks) - run_len_to_find + 1):
                sub_hand = uniq_ranks[start_card: start_card + run_len_to_find]
                if Card._check_if_run(sub_hand):
                    run = sub_hand
            run_len_to_find -= 1

        multiplier = 1
        for rank in run:
            multiplier *= all_ranks.count(rank)

        # print(f"all done: { cards } -> { len(run) } * { multiplier } = { len(run) * multiplier }")
        return len(run) * multiplier

    @staticmethod
    def _check_if_run(ranks):
        if len(ranks) < 3:
            return False

        ranks = sorted(ranks)
        for i in range(1, len(ranks)):
            if ranks[i] - ranks[i - 1] != 1:
                return False
        return True

    @staticmethod
    def score_hand(cards):
        """
        assumes the cut card is always the last card passed in
        """
        flush_score = 0
        if Card.flush_check(cards):
            flush_score = len(cards)
        pair_score = 2 * Card.pair_count(cards)
        fifteen_score = 2 * Card.fifteen_count(cards)
        run_score = Card.run_count(cards)
        # print(f"{ cards } -> { flush_score } + { pair_score } + { fifteen_score } + { run_score }")
        total_score = flush_score + pair_score + fifteen_score + run_score
        return total_score
