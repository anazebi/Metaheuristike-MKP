from copy import deepcopy
from random import shuffle

def random_rjesenje(ruksak):
    predmeti=deepcopy(ruksak.svi_predmeti)
    shuffle(predmeti)
    for predmet in predmeti:
        if ruksak.mogu_dodati(predmet):
            ruksak.dodaj_predmet(predmet)
        else:
            continue