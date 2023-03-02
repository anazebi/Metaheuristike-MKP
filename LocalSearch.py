from copy import deepcopy
from functools import reduce
from Neighborhood import sort_steps

class LocalSearch(object):
    
    def __init__(self, max_iteration):
        
        self.iteration_counter = 0
        self.iteration_better = 0
        self.max_iteration = max_iteration


    def __call__(self, neighborhood_function, knapsack):

        solutions = neighborhood_function(knapsack)         # moguci koraci iz trenutnog stanja
        sorted_steps = sort_steps(solutions)                # sortiranje koraka 

        best_solution = knapsack.value                      # trenutna konfiguracija
        # best_solution_steps = deepcopy(knapsack.steps)      
        best_solution_items = deepcopy(knapsack.items_in)   

        while self.iteration_counter < self.max_iteration:  # broj iteracija kontroliramo iz vana
            
            self.iteration_counter += 1
            next_step = sorted_steps.pop(0)                 # najbolji moguci korak

            if not next_step.evaluate_step() < 0:           # ako korak vodi k poboljsanju trenutnog stanja, izvrsavamo ga

                solution = knapsack.value + next_step.evaluate_step()
                knapsack.execute_step(next_step)

                if solution > best_solution:
                    best_solution = solution
                    self.iteration_better = self.iteration_counter
                    best_solution_items = deepcopy(knapsack.items_in)

            else:                                           # ako korak ne vodi k poboljsanju trenutnog stanja, nasli smo lokalni maksimum
                break

            next_solutions = neighborhood_function(knapsack)
            sorted_steps = sort_steps(next_solutions)

        knapsack.items_in = best_solution_items
        knapsack.value = best_solution

        print("Provedeno je ukupno %d iteracija" %self.iteration_counter)
        print ("Najbolje rjesenje nadeno je u iteraciji %d s vrijednoscu %d" % (self.iteration_better, best_solution))
        