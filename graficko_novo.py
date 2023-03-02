import tkinter as tk
from tkinter import ttk
from tkinter import *


from lib2to3.pgen2.token import NEWLINE
from Random_solution import random_rjesenje
from Greedy_solution import greedy_rjesenje 
from Predmet import Item
from Ruksak import Knapsack
import Neighborhood
from TabuSearch import TabuList, TabuSearch



root = tk.Tk()

root.geometry("800x500")
root.title("Višedimenzionalni problem ruksaka")

label = tk.Label(root, text="Višedimenzionalni problem ruksaka" , font=('Arial', 18))
label.pack(padx=20,pady=20)

podaci= tk.Label(root, text="Podaci")
podaci_combobox = ttk.Combobox(root, values=["test1.txt", "test2.txt", "test3.txt"])
podaci.pack()
podaci_combobox.pack()

buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

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

def greedy():
    podaci = podaci_combobox.get()
    if (podaci !=''):
        Label(root, text="Odabrali ste testni primjer " +  podaci + ". " + "Odabrani algoritam : Greedy ", font=('Arial, 12')).pack()
        ruksak= Knapsack(*load_bag_from(podaci))
        greedy_rjesenje(ruksak)
    else:
        Label(root, text="Niste odabrali testni primjer!", font = ('Arial, 12')).pack()


btn1 = tk.Button(buttonframe, text="Greedy", font=('Arial', 18), command=greedy)
btn1.grid(row=1, column=0, sticky=tk.W+tk.E)

def tabu():
    podaci = podaci_combobox.get()
    
    if (podaci !=''):
        Label(root, text="Odabrali ste testni primjer " +  podaci + ". " + "Odabrani algoritam : Tabu Search ", font=('Arial, 12')).pack()
        
        bag = Knapsack(*load_bag_from(podaci), tabu_list = TabuList(200))
        bag.optimization_tabu(greedy_rjesenje, TabuSearch(300), Neighborhood.first_improve)
    else:
        Label(root, text="Niste odabrali testni primjer!", font = ('Arial, 12')).pack()
    

btn2 = tk.Button(buttonframe, text="Tabu Search", font=('Arial', 18), command=tabu)
btn2.grid(row=1, column=1, sticky=tk.W+tk.E)

def geneticki():
    podaci = podaci_combobox.get()
    
    if (podaci !=''):
        Label(root, text="Odabrali ste testni primjer " +  podaci + ". " + "Odabrani algoritam : Genetički algoritam ", font=('Arial, 12')).pack()

    else:
        Label(root, text="Niste odabrali testni primjer!", font = ('Arial, 12')).pack()
    


btn3 = tk.Button(buttonframe, text="Genetički algoritam", font=('Arial', 18), command=geneticki)
btn3.grid(row=1, column=2, sticky=tk.W+tk.E)

buttonframe.pack(fill='x')
        
root.mainloop()








