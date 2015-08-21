import random
from presets import *
import utility
def random_note_length(max_len, dist):
    """Chooses a random note length given a maximum length and distribution"""
    res = {}
    for choice, weight in dist.items():
        if choice <= max_len:
            res[choice] = weight
    return utility.choose_random_weighted_choice(res)

possible_lengths = sorted([c for c, d, in LENGTH_DIST.items()]) 

for i in range(40):
    c = i+1
    max_poss_len = possible_lengths[(c % len(possible_lengths))]
    print("{:5} : {:5}".format(max_poss_len, random_note_length(max_poss_len, LENGTH_DIST)))
