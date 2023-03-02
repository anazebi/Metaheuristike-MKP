from Ruksak import Step
from random import choice, shuffle
from copy import deepcopy
from Ruksak import properties_number

def sort_steps(steps):             # sortira korake silazno po promjeni vrijednosti ruksaka koju uzrokuju
    return sorted(steps, key = lambda x: x.evaluate_step, reverse = True)

def best(knapsack):
         
     neighborhood = []

     for item2 in knapsack.items_out:           

         current_value = knapsack.value
         print("Trenutno: ", current_value)

         for item1 in knapsack.items_in:      

             if knapsack.switch_possible(item1, item2):
                 new_value = knapsack.evaluate_switch(item1, item2)
                 step = Step(add_items = [item2,], remove_items = [item1,])

                 if new_value > knapsack.value:
                     neighborhood.append(step)
                     print("Poboljsanje: ", new_value)

                 neighborhood.append(step)
             else:
                 pass
     
     return neighborhood

def first_improve(knapsack):       # gradi okolinu trenutne konfiguracije ruksaka do pronalazenja prve zamjene predmeta koja poboljsava vrijednost ruksaka, uz postivanje svih njegovih kapaciteta

     neighborhood = []

     for item2 in knapsack.sort(knapsack.items_out):            # ubacujem predmet s NAJVECIM omjerom vrijednost : suma tezina

         current_value = knapsack.value
         print("Trenutno: ", current_value)

         for item1 in knapsack.sort_up(knapsack.items_in):      # izbacujem predmet s NAJMANJIM omjerom vrijednost : suma tezina

             if knapsack.switch_possible(item1, item2):
                 new_value = knapsack.evaluate_switch(item1, item2)
                 step = Step(add_items = [item2,], remove_items = [item1,])

                 if new_value > knapsack.value:
                     neighborhood.append(step)
                     print("Poboljsanje: ", new_value)
                     return neighborhood                    # okolina se gradi do prvog susjeda koji poboljsava trenutnu vrijednost ruksaka

                 neighborhood.append(step)
             else:
                 pass

     return neighborhood

def best_improve(knapsack):        # izvrsava pronadeni korak iz okoline trenutne konfiguracije ruksaka koji poboljsava ukupnu vrijednost predmeta u ruksaku
                                   # funkcija koja mijenja konfiguraciju ruksaka
    start = first_improve(knapsack)             # pronalazi konfiguracije koje mozemo doseci iz trenutne konfiguracije
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

