import os
import random

from game import Game
from player import Player

sam = Player("sam")
char = Player("char")
my_game = Game(char, sam)

best_game = str(my_game)
best_score = 0
all_scores = {}

for i in range(0, 100000):
    # print(f"Hand Number { i }")
    pre_score = my_game.player1.score
    my_game.deal()
    my_game.throw_to_crib()

    my_game.score()
    # print(my_game)

    game_score = my_game.player1.score - pre_score
    if game_score in all_scores.keys():
        all_scores[game_score] += 1
    else:
        all_scores[game_score] = 1

    if game_score > best_score:
        best_score = game_score
        best_game = str(my_game)
    
print(f"best game = { best_score }")
print(best_game)

print("*"*80)
scores = sorted(all_scores.keys())
for score in scores:
    print(f"{ score } -> { all_scores[score] }")


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
