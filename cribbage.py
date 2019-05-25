import os
import random

import pandas as pd

from cribbage import player, game


def run_sims(players, num_sims):
    '''
    simulates `num_sims` standard games with the input list of players

    returns a dict with the winner count
    '''

    total_hands = 0

    # name: [wins, total_points]
    scorecard = {}
    for player in players:
        scorecard[player.name] = [0, 0]

    for _ in range(0, num_sims):
        my_game = game.Game(players)
        my_game.sim_game()
        total_hands += my_game.round_number
        scorecard[my_game.winner.name][0] += 1
        for player in players:
            scorecard[player.name][1] += player.score

    return scorecard, total_hands


daisy = player.NaiveBot("daisy")
sam = player.LowBot("sam")
char = player.HighBot("char")

num_sims = 2500

scorecard, total_hands = run_sims([daisy, sam, char], num_sims)

print(scorecard)
print(f"played { num_sims } games, { total_hands } hands")

for player in scorecard:
    wins = scorecard[player][0]
    win_pct = round(wins / num_sims * 100, 2)
    avg_hand = round(scorecard[player][1] / total_hands, 1)
    avg_score = round(scorecard[player][1] / num_sims, 1)
    print(
        f"{ player } \n-- { wins } ({ win_pct }%), { avg_hand } points per hand"
        f", { avg_score } points per game"
    )

# 10000 games
# {'daisy': 1495, 'sam': 5663, 'char': 2842}

# main loop
# 1. deal cards
# 2. send to crib
# 3. reveal cut
# 4. non-dealer plays card
# 5. dealer plays card
# 6. repeat 4 and 5 unti out of cards
# 7. score non-dealer hand
# 8. score dealer hand
# 9. score crib
