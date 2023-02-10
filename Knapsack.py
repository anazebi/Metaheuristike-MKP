from copy import deepcopy
from Predmet import Item
from time import clock
from functools import reduce

properties_number = 0

class Ruksak(object):
    
    def __init__(self, svi_predmeti, *args, **kwargs):
        self.vrijednost = 0
        self.svi_predmeti = svi_predmeti #svi predmeti koji su na raspolaganju
        self.pocetna_vrijednost = 0
        self.predmeti = [] #predmeti u ovom ruksaku
        self.broj_iteracija = 0
        self.koraci_do_sada = []
        for ind, arg in enumerate(args):
            setattr(self,'property{}'.format(ind+1),int(arg))
        properties_number = len(args)
        for key in kwargs.keys():
            setattr(self,key,kwargs[key])
    
    def mogu_dodati(self,predmet):
        flag = not predmet in self.predmeti
        for i in range(properties_number):
            flag = flag and getattr(self,'property{}'.format(i+1) >= getattr(predmet,'property{}'.format(i+1)))
            return flag
    
    def dodaj_predmet(self, predmet):
        if self.mogu_dodati(predmet):
            self.predmeti.append(predmet)
            for i in range(properties_number):
                setattr(self, 'property{}'.format(i+1),getattr(self,'property{}'.format(i+1))- getattr(predmet,'property{}'.format(i+1)))
            self.vrijednost += predmet.value
            self.svi_predmeti.remove(predmet)
            return True
        return False

    def sortirani(self,predmeti, key = Predmet.ratio):
        return sorted(predmeti, key = key, reverse = True)
    
    def remove_predmet(self, predmet):
        if predmet in self.predmeti:
            for i in range(properties_number):
                setattr(self, 'property{}'.format(i+1), getattr(self, 'property{}'.format(i+1))+ getattr(predmet, 'property{}'.format(i+1)))
            
            self.vrijednost -= predmet.value
            self.predmeti.remove(predmet)
            self.svi_predmeti.append(predmet)
            return True
        return False
    
    def __contains__(self, predmet):
        return any(map(lambda x: x == predmet, self.predmeti))
