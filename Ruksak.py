from copy import deepcopy
from Predmet import Item
from functools import reduce
from time import process_time

properties_number = 0

class Knapsack(object):

    def __init__(self, all_items, *restrictions, **kwargs):
        
        self.all_items = all_items
        self.value = 0
        self.items_out = deepcopy(all_items)              # predmeti van ruksaka
        self.start_value = 0
        self.items_in = []                      # predmeti u ruksaku
        self.iterations = 0                     # broj iteracija
        self.steps = []                         # koraci do sada

        # postavljanje svih ogranicenja na pojedine dimenzije ruksaka
        for indeks, restriction in enumerate(restrictions):
            setattr(self, 'property{}'.format(indeks + 1), int(restriction))

        # broj dimenzija ruksaka
        global properties_number
        properties_number = len(restrictions)

        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def can_add(self, item):                    # funkcija koja vraca true ako dani predmet mozemo dodati u ruksak, false inace 
        
        if item in self.items_in:
            return False                        # predmet ne smije vec biti u ruksaku

        # predmet mozemo dodati ako nijedna njegova tezina ne prelazi preostali kapacitet pripadne dimenzije ruksaka
        for i in range(properties_number):
            if getattr(self, 'property{}'.format(i + 1)) < getattr(item, 'property{}'.format(i + 1)):
                return False
        
        return True

    def add_item(self, item):                   # vraca True ako je predmet uspjesno dodan u ruksak, False inace

        if self.can_add(item):
            self.value += item.value

            for i in range (properties_number):
                setattr(self, 'property{}'.format(i + 1), int(getattr(self, 'property{}'.format(i + 1))) - int(getattr(item, 'property{}'.format(i + 1))))
                # smanjujemo preostali kapacitet svake dimenzije ruksaka za pripadne vrijednosti tezina predmeta kojeg u njega dodajemo
            self.items_in.append(item)
            self.items_out.remove(item)
            # print("dodan predmet")
            # print(vars(item))
            return True
        
        return False

    def remove_item(self, item):                # vraca True ako je predmet uspjesno izbacen, False inace

        if item in self.items_in:
            for i in range(properties_number):
                setattr(self, 'property{}'.format(i + 1), int(getattr(self,'property{}'.format(i + 1))) + int(getattr(item, 'property{}'.format(i + 1)))) 
                # uvecavamo preostali kapacitet svake dimenzije ruksaka za pripadne vrijednosti tezina predmeta kojeg iz njega izbacujemo

            self.value = self.value - item.value
            self.items_out.append(item)         # dodajemo predmet u listu predmeta izvan ruksaka
            self.items_in.remove(item)          # izbacujemo predmet iz liste predmeta sadrzanih u ruksaku
            # print("uklonjen predmet")
            # print(vars(item))
            return True

        return False

    def __contains__(self, item):
        return any(map(lambda x: x == item, self.items_in))    ## any vraca True ako je bilo koja od vrijednosti True, map vraca listu vrijednosti dobivenih kad lambda funkciju primijenimo na listu predmeta u ruksaku 

    def sort(self, items):                      # vraca listu predmeta sortiranu silazno po omjeru vrijednosti i ukupne tezine
        return sorted(items, key = Item.ratio, reverse = True)

    def sort_up(self, items):                   # vraca listu predmeta sortiranu uzlazno po omjeru vrijednosti i ukupne tezine
        return sorted(items, key = Item.ratio, reverse = False)

    def switch_possible(self, item1, item2):    # vraca True ako predmet item1 iz ruksaka mogu zamijeniti predmetom item2 koji nije u ruksaku

        if item1 not in self.items_in or item2 in self.items_in:
            return False

        for i in range (properties_number):
            if(int(getattr(self, 'property{}'.format(i + 1))) + int(getattr(item1, 'property{}'.format(i + 1))) < int(getattr(item2, 'property{}'.format(i + 1)))):
                return False
        
        return True

    def switch(self, item1, item2):                   # vraca True ako je zamjena uspjesno obavljena, false inace 
        
        if self.switch_possible(item1, item2):
            self.add_item(item2)                      # izbacuje item1, dodaje item2
            self.remove_item(item1)                     
            return True

        return False

    def evaluate_switch(self, item1, item2):        # vraca vrijednost ruksaka nakon izbacivanja predmeta item1 te dodavanja predmeta item2

        if(self.switch_possible(item1, item2)):
            return self.value - item1.value + item2.value
        
        return False

    def execute_step(self, step, silent = False):
       
        for item in step.remove_items:
            if not item in self.items_in:
                return False
            self.remove_item(item)
            # print("Uklonjen predmet u koraku") ####
            # print(vars(item))

        for item in step.add_items:
            if not item in self.items_out:
                return False
            self.add_item(item)
            # print("Dodan predmet u koraku")
            # print(vars(item))

        if not silent:
            self.iterations += 1
            self.steps.append(step)

    def optimization_tabu(self, initial_solution_function, heuristic_function = None, neighborhood_function = None):
        
        start = process_time()

        initial_solution_function(self)                     # pronalazi inicijalno/pocetno rjesenje
        self.initial_solution = deepcopy(self.items_in)    
        self.initial_value = self.value

        heuristic_function(neighborhood_function, self)     # inicijalno rjesenje poboljsavamo danom heuristikom primjenom algoritma tabu search

        end = process_time()

        print ('Inicijalno rjesenje sadrzi sljedece predmete: ')
        for i in range(len(self.initial_solution)):
            print (vars(self.initial_solution[i]))
        print ('Ukupna vrijednost svih predmeta sadrzanih u inicijalnom rjesenju iznosi: %d' % self.initial_value)

        print ('Ukupna vrijednost svih predmeta sadrzanih u rjesenju dobivenom primjenom algoritma Tabu search na inicijalno rjesenje: %d' % self.value)              
        print ('Koristeci Tabu search ostvareno je sljedece poboljsanje ukupne vrijednosti ruksaka: %d' % (self.value - self.initial_value))

        for i in range(properties_number):
            print ('Neiskoristeni kapacitet dimenzije{} : %d'.format(i + 1) % getattr(self, 'property{}'.format(i+1)))

        print ('Broj predmeta u ruksaku: %s' % len(self.items_in))
        print ('Vrijeme izvrsavanja: %f milisekundi.' % ((end - start) * 1000))

    
    def optimization_local(self, initial_solution_function, heuristic_function = None, neighborhood_function = None):  # lokalno trazenje
        
        start = process_time()
        
        initial_solution_function(self)                         # pronalazi inicijalno rjesenje
        self.initial_solution = deepcopy(self.items_in)         
        self.initial_value = self.value                         # vrijednost inicijalnog rjesenja
        
        heuristic_function(self)
        
        end = process_time()
        
        print ('Inicijalno rjesenje sadrzi sljedece predmete: ')
        for i in range(len(self.initial_solution)):
            print (vars(self.initial_solution[i]))
        print ('Ukupna vrijednost svih predmeta sadrzanih u inicijalnom rjesenju iznosi: %d' % self.initial_value)

        print ('Ukupna vrijednost svih predmeta sadrzanih u rjesenju dobivenom primjenom heuristike na inicijalno rjesenje: %d' % self.value)              
        print ('Koristeci heuristiku ostvareno je sljedece poboljsanje ukupne vrijednosti ruksaka: %d' % (self.value - self.initial_value))

        for i in range(properties_number):
            print ('Neiskoristeni kapacitet dimenzije{} : %d'.format(i + 1) % getattr(self, 'property{}'.format(i+1)))
        
        # for i in range(len(self.items_in)):
        #    print(vars(self.items_in[i]))

        print ('Broj predmeta u ruksaku: %s' % len(self.items_in))
        print ('Vrijeme izvrsavanja: %f milisekundi.' % ((end - start) * 1000))


# klasa koja predstavlja korak prijelaza iz jedne konfiguracije u drugu
class Step(object):

    def __init__(self, add_items = [], remove_items = []):      # konstruktor koji kreira korak s listom predmeta za dodavanje u ruksak te s listom predmeta za uklanjanje iz ruksaka
        
        self.add_items = add_items
        self.remove_items = remove_items

    def evaluate_step(self):                                   # funkcija vraca promjenu vrijednosti ruksaka nakon izvrsenog koraka, procjenjuje 'snagu' koraka
        
        increase_value = decrease_value = 0

        if not len(self.add_items) == 0:
            increase_value = reduce(lambda x, y : x + y, [item.value for item in self.add_items])  # reduce primjenjuje lambda funkciju na elemente liste

        if not len(self.remove_items) == 0:
            decrease_value = reduce(lambda x, y : x + y, [item.value for item in self.remove_items])

        return increase_value - decrease_value

    def __eq__(self, another_step):                            # omogucujemo usporedbu koraka
        
        if not isinstance(another_step, Step):
            return False

        return self.remove_items == another_step.remove_items and self.add_items == another_step.add_items

    def reverse_step(self):                                    # radi suprotni korak
        return Step(add_items = self.remove_items, remove_items = self.add_items)