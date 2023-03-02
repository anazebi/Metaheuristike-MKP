from lib2to3.pgen2.token import NEWLINE
from Random_solution import random_rjesenje
from Greedy_solution import greedy_rjesenje 
from Predmet import Item
from Ruksak import Knapsack
import Neighborhood
from TabuSearch import TabuList, TabuSearch
from LocalSearch import LocalSearch
from HillClimbing import HillClimbing

#-------------------------------------------------------------------------------------------------#
################# format datoteke u kojoj su sadrzani podaci koje zelimo ucitati: #################
#-------------------------------------------------------------------------------------------------#
# n m                                                   ## n - broj predmeta, m - broj dimenzija  #
# linija s vrijednostima svakoga predmeta                                                         #
# za svaku od m dimenzija: linija s n tezina te dimenzije za svaki od n predmeta                  #
# linija s m kapaciteta ruksaka                                                                   #
#-------------------------------------------------------------------------------------------------#

def load_items_from(file_name):                     # ucitavanje podataka o predmetima iz datoteke s imenom file_name
    
    items = []

    file_lines = open(file_name).readlines()
    file_lines = [line.strip().split(' ') for line in file_lines]
    
    number_of_items = int(file_lines[0][0])

    for i in range (number_of_items):
        weights = []
        for j in range(2, len(file_lines) - 1):     # za svaki predmet prikupljamo pripadne tezine 
            weights.append(file_lines[j][i])
        item = Item('Item %d' % i, int(file_lines[1][i]), *weights)     # kreiramo predmet s prikupljenim tezinama
        items.append(item)                                              # dodajemo predmet u listu

    return items

def load_capacities_from(file_name):                # ucitavanje kapaciteta svih dimenzija ruksaka

    lines = open(file_name).readlines()
    return lines[-1].split()

def load_bag_from(file_name):                       # kreiranje ruksaka s podacima sadrzanima u datoteci file_name

    capacities = load_capacities_from(file_name)
    return (load_items_from(file_name), *capacities)

if __name__ == '__main__':

    bag = Knapsack(*load_bag_from('250-10-02.txt'), tabu_list = TabuList(200))
    # local search heuristic
    # bag.optimization_local(greedy_rjesenje, LocalSearch(100), Neighborhood.first_improve) 
    # Tabu metaheuristic
    # bag.optimization_tabu(greedy_rjesenje, TabuSearch(300), Neighborhood.first_improve)
    # hill climbing
    bag.optimization_hill(greedy_rjesenje, HillClimbing(100), Neighborhood.best)