from itertools import combinations


def flush_check(cards):
    if not isinstance(cards, list):
        raise RuntimeError("flush_check needs a list")
    if len(cards) <= 1:
        raise RuntimeWarning("flush_check received a list of len 1")

    for card in cards[1:]:
        if card.suit != cards[0].suit:
            return False
    return True


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

    return fifteens


def run_count(cards):
    all_ranks = [card.rank for card in cards]
    uniq_ranks = sorted(set(all_ranks))

    run = []
    run_len_to_find = len(uniq_ranks)
    while run_len_to_find >= 3 and len(run) == 0:
        for start_card in range(0, len(uniq_ranks) - run_len_to_find + 1):
            sub_hand = uniq_ranks[start_card: start_card + run_len_to_find]
            if _check_if_run(sub_hand):
                run = sub_hand
        run_len_to_find -= 1

    multiplier = 1
    for rank in run:
        multiplier *= all_ranks.count(rank)

    return len(run) * multiplier


def knobs_check(cards):
    for card in cards[:-1]:
        if card.rank == 11 and card.suit == cards[-1].suit:
            return True
    return False


def _check_if_run(ranks):
    if len(ranks) < 3:
        return False

    ranks = sorted(ranks)
    for i in range(1, len(ranks)):
        if ranks[i] - ranks[i - 1] != 1:
            return False
    return True


def score_hand(cards):
    """
    assumes the cut card is always the last card passed in
    """
    if flush_check(cards):
        # hand and cut card all big flush
        flush_score = len(cards)
    elif flush_check(cards[:-1]):
        # hand is flush but cut card does not match
        flush_score = len(cards) - 1
    else:
        flush_score = 0
    pair_score = 2 * pair_count(cards)
    fifteen_score = 2 * fifteen_count(cards)
    run_score = run_count(cards)
    knobs_score = 1 if knobs_check(cards) else 0
    total_score = flush_score + pair_score + \
        fifteen_score + run_score + knobs_score
    return total_score


def stack_count(cards):
    """
    provides the total rank sum for a list of cards accounting
    for all face cards counting as 10
    """
    return sum(
        map(lambda card: card.rank if card.rank < 10 else 10, cards))
