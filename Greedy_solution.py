def greedy_rjesenje(ruksak):

    items = ruksak.sort(ruksak.all_items)

    for item in items:
        ruksak.add_item(item)
    return ruksak.value
