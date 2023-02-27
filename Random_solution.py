from copy import deepcopy
from random import shuffle
from Ruksak import Knapsack

def random_rjesenje(ruksak):

    items = deepcopy(ruksak.all_items)

    shuffle(items)

    for item in items:
        if ruksak.can_add(item):
            ruksak.add_item(item)
        else:
            continue