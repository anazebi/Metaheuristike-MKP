from Ruksak import Step
from random import choice, shuffle
from copy import deepcopy
from Ruksak import properties_number

def first_improve(knapsack):       # gradi okolinu trenutne konfiguracije ruksaka do pronalazenja prve zamjene predmeta koja poboljsava vrijednost ruksaka, uz postivanje svih njegovih kapaciteta

     neighborhood = []

     for item2 in knapsack.sort(knapsack.items_out):            

         for item1 in knapsack.sort(knapsack.items_in):
             
             if knapsack.switch_possible(item1, item2):
                 new_value = knapsack.evaluate_switch(item1, item2)
                 step = Step(add_items = [item2,], remove_items = [item1,])

                 if new_value > knapsack.value:
                     neighborhood.append(step)
                     return neighborhood

                 neighborhood.append(step)
             else:
                 pass

     return neighborhood

def sort_steps(steps):             # sortira korake silazno po promjeni vrijednosti ruksaka koju uzrokuju
    return sorted(steps, key = lambda x: x.evaluate_step, reverse = True)

def best_improve(knapsack):        # izvrsava pronadeni korak iz okoline trenutne konfiguracije ruksaka koji poboljsava ukupnu vrijednost predmeta u ruksaku
                                   # funkcija koja mijenja konfiguraciju ruksaka, ako je pozitivna promjena moguca
    start = first_improve(knapsack)
    sorted_steps = sort_steps(start)
    best_solution = knapsack.value
    best_solution_steps = deepcopy(knapsack.steps)
    best_solution_items = deepcopy(knapsack.items_in)

    if not len(sorted_steps) == 0:
        next_step = sorted_steps.pop(0)
        solution = knapsack.value + next_step.evaluate_step
        knapsack.execute_step(next_step)

        if solution > best_solution:
            best_solution = solution
            best_solution_steps = deepcopy(knapsack.steps) 
            best_solution_items = deepcopy(knapsack.items_in) 

    knapsack.value = best_solution 
    knapsack.items_in = best_solution_items
    knapsack.steps = best_solution_steps

    return False

