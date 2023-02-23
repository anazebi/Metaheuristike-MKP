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
    
     def makni_predmet(self, predmet):
        if predmet in self.predmeti:
            for i in range(properties_number):
                setattr(self, 'con{}'.format(i+1), getattr(self, 'con{}'.format(i+1)) + getattr(item, 'con{}'.format(i+1)))
            self.vrijednost -= predmet.vrijednost
            self.predmeti.remove(predmet)
            self.svi_predmeti.append(predmet)
            return True
        return False
    
    def dodaj_predmet(self, predmet):
        if self.mogu_dodati(predmet):
            self.predmeti.append(predmet)
            for i in range(properties_number):
                setattr(self, 'property{}'.format(i+1),getattr(self,'property{}'.format(i+1))- getattr(predmet,'property{}'.format(i+1)))
            self.vrijednost += predmet.value
            self.svi_predmeti.remove(predmet)
            return True
        return False

    def sortirani(self,predmeti, key = Item.ratio):
        return sorted(predmeti, key = key, reverse = True)
    
    def makni_predmet(self, predmet):
        if predmet in self.predmeti:
            for i in range(properties_number):
                setattr(self, 'property{}'.format(i+1), getattr(self, 'property{}'.format(i+1))+ getattr(predmet, 'property{}'.format(i+1)))
            
            self.vrijednost -= predmet.value
            self.predmeti.remove(predmet)
            self.svi_predmeti.append(predmet)
            return True
        return False
   
    def izvsi_korak(self, korak, silent=False):
        for predmet in korak.makni_predmete:
            if not predmet in self:
                return False
            self.makni_predmet(predmet)
        for predmet in korak.dodaj_predmete:
            if not self.mogu_dodati(predmet):
                return False
            self.dodaj_predmet(predmet)
        if not silent:
            self.broj_iteracija += 1
            self.koraci_do_sada.append(korak)
            
    def evaluiraj_zamjenu(self, predmet1, predmet2):
        return self.mogu_zamjeniti(predmet1, predmet2)
    
    
    def mogu_zamjeniti(self, predmet1, predmet2):
        if predmet1 not in self.predmeti or predmet2 in self.predmeti:
            return False
        for i in range properties_number:
            if not (getattr(predmet2, 'con{}'.format(i)) <= (getattr(self, 'con{}'.format(i))+getattr(predmet1, 'con{}'.format(i)))
                    return False
        return self.vrijednost - predmet1.vrijednost + predmet2.vrijednost
                    
    def zamjena(predmet1, predmet2):
        if self.mogu_zamjeniti(predmet1, predmet2):
             self.makni_predmet(predmet1)
             self.dodaj_predmet(predmet2)
             return True
        return False


    
    def __contains__(self, predmet):
        return any(map(lambda x: x == predmet, self.predmeti))
     
 class Korak(object):

    def __init__(self, dodaj_predmete=[], makni_predmete=[]):
        self.dodaj_predmete = dodaj_predmete
        self.makni_predmete = makni_predmete

    @property #ne kuzim to?

    def evaluiraj_korak(self):
        makni_vrijednost = dodaj_vrijednost = 0
        if not len(self.makni_predmete) == 0:
            makni_vrijednost = reduce(lambda x, y: x+y, [predmet.vrijednost for predmet in self.makni_predmete])
        if not len(self.dodaj_predmete) == 0:
            dodaj_vrijednost = reduce(lambda x, y: x+y, [predmet.vrijednost for predmet in self.dodaj_predmete])
        return dodaj_vrijednost - makni_vrijednost

    def okreni(self):
        return Korak( dodaj_predmete=self.makni_predmete, makni_predmete=self.dodaj_predmete)
    
    def __eq__(self, korak1):
        if not isinstance(korak1, Korak):
            return False
        return self.dodaj_predmete == korak1.dodaj_predmete and self.makni_predmete == korak1.makni_predmete
                    
                    

                    
               
