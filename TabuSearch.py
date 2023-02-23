from copy import deepcopy
from functools import reduce

# tabu lista koja sadrzi "zabranjena stanja" 
# ova klasa nasljeduje od klase list
class TabuList(list):

    def __init__(self, size=3):
        self.size = size
        super(TabuList, self).__init__()

    # dodavanje stanja u listu FIFO nacinom
    def append(self, element):
        if len(self) == self.size:          
            self.pop(0)
            return super(TabuList, self).append(element)
        return super(TabuList, self).append(element)

    # provjera sadrzi li tabu lista dano stanje
    def __contains__(self, move):
        for i in range(len(self)):
            if move == self[i]:
                return True
        return False
