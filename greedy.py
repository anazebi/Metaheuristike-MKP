from Ruksak import Knapsack

def greedy_rjesenje(ruksak):

    items = ruksak.sorted(ruksak.all_items)

    for item in items:
        ruksak.add_item(item)