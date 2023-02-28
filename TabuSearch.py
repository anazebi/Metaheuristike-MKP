from copy import deepcopy
from functools import reduce
from Neighborhood import sort_steps

# tabu lista koja sadrzi "zabranjene korake" 
class TabuList(list):

    # tabu lista ce biti duljine 3, ako ne zadamo drugacije
    def __init__(self, size = 3):           
        self.size = size
        super(TabuList, self).__init__()

    # dodavanje koraka u listu FIFO nacinom
    def append(self, element):
        if len(self) == self.size:                              
            self.pop(0)                                     # ako je tabu lista puna, izbacijemo iz nje element koji je prvi dodan
            return super(TabuList, self).append(element)    # na kraj liste dodajemo zeljeni element
        return super(TabuList, self).append(element)

    # provjera sadrzi li tabu lista dani korak
    def __contains__(self, step):
        for i in range(len(self)):
            if step == self[i]:
                return True
        return False


# klasa koja predstavlja TabuSearch algoritam
class TabuSearch(object): 

    def __init__(self, max_iteration = 2):      # ako ne zadamo drugacije, dopustene su maksimalno dvije uzastopne iteracije bez poboljsanja ukupne vrijednosti ruksaka
        
        self.iteration_counter = 0              # ukupan broj provedenih iteracija
        self.iteration_better = 0               # zadnja iteracija koja je poboljsala vrijednost ruksaka
        self.max_iteration = max_iteration      # maksimalan dozvoljeni broj uzastopnih iteracija bez poboljsanja vrijednosti ruksaka

    # def sort_steps(steps):             # sortira korake silazno po promjeni vrijednosti ruksaka koju uzrokuju
    #    return sorted(steps, key = lambda x: x.evaluate_step, reverse = True)
        
    def __call__(self, neighborhood_function, knapsack):

        solutions = neighborhood_function(knapsack) 
        sorted_steps = sort_steps(solutions)
        for tabu in knapsack.tabu_list:
            if tabu.reverse_step() in sorted_steps:
                sorted_steps.remove(tabu.reverse_step())
        # [sorted_steps.remove(tabu.reverse_step()) for tabu in knapsack.tabu_list if tabu.reverse_step() in sorted_steps]  
        
        best_solution = knapsack.value          # trenutna konfiguracija
        best_solution_steps = deepcopy(knapsack.steps)
        best_solution_items = deepcopy(knapsack.items_in)
        end = False

        while self.iteration_counter - self.iteration_better < self.max_iteration:   
            self.iteration_counter += 1

            if not len(sorted_steps) == 0:
                next_step = sorted_steps.pop(0)
                solution = knapsack.value + next_step.evaluate_step()
                knapsack.execute_step(next_step)
                knapsack.tabu_list.append(next_step.reverse_step())          # u tabu listu dodajemo novi zabranjeni korak, koji bi ponistio upravo napravljeni korak (sprjecavamo vracanje u upravo odabrano stanje)
                
                if(solution > best_solution):
                    print ("Trenutna iteracija %d, trenutno rjesenje %d, najbolje rjesenje pronadeno u iteraciji %d s vrijednosti %d" % (self.iteration_counter, solution, self.iteration_better, best_solution))
                    best_solution = solution
                    best_solution_steps = deepcopy(knapsack.steps)
                    best_solution_items = deepcopy(knapsack.items_in)
                    self.iteration_better = self.iteration_counter
            else:
                best_tabu = reduce(lambda x, y: x if x.evaluate_step() > y.evaluate_step() else y, knapsack.tabu_list) # najbolji zabranjeni korak
                if best_tabu.evaluate_step() > 0:  # ako zabranjeni korak daje novo globalno optimalno rjesenje, dopustamo njegovo izvrsavanje
                    solution = knapsack.value + best_tabu.evaluate_step()
                    if solution > best_solution:
                        print ("[TABU POTEZ] Trenutna iteracija %d, trenutno rjesenje %d, najbolje rjesenje pronadeno u iteraciji %d s vrijednosti %d" % (self.iteration_counter, solution, self.iteration_better, best_solution))
                        best_solution = solution
                        best_solution_steps = deepcopy(knapsack.steps)
                        best_solution_items = deepcopy(knapsack.items_in)
                        self.iteration_better = self.iteration_counter
                    
                    knapsack.execute_step(best_tabu)
            
            next_solutions = neighborhood_function(knapsack) 
            sorted_steps = sort_steps(next_solutions)
            # [sorted_steps.remove(tabu.reverse_step()) for tabu in knapsack.tabu_list if tabu.reverse_step() in sorted_steps] # micemo zabranjene poteze iz dostupnih poteza
            for tabu in knapsack.tabu_list:
                if tabu.reverse_step() in sorted_steps:
                    sorted_steps.remove(tabu.reverse_step())

        print ("Najbolje rjesenje nadeno je u iteraciji %d s vrijednoscu %d" % (self.iteration_better, best_solution))

        knapsack.value = best_solution
        knapsack.items_in = best_solution_items
        knapsack.steps = best_solution_steps

        print ('Tabu search proveden je s maksimumom od %d iteracija i tabu listom duljine %d.' % (self.max_iteration, knapsack.tabu_list.size))
        if not end:
            print ('Tabu search je zaustavljen zbog dostizanja maksimalnog broja iteracija.')
        return False
