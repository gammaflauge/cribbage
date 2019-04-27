import os
import random

from game import Game


my_game = Game("char", "sam")


for i in range(0,1):
    my_game.deal()
    my_game.score()
    print(my_game)



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