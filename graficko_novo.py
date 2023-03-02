import tkinter as tk
from tkinter import ttk
from tkinter import *

import time
from lib2to3.pgen2.token import NEWLINE
from Random_solution import random_rjesenje
from Greedy_solution import greedy_rjesenje 
from Predmet import Item
from Ruksak import Knapsack
import Neighborhood
from TabuSearch import TabuList, TabuSearch
import genetski
from genetski import main, provjera 
import SAHillClimbing
import SHillClimbing
from SAHillClimbing import SAHillClimbing
from SHillClimbing import SHillClimbing
import os


root = tk.Tk()

root.geometry("800x800")
root.title("Višedimenzionalni problem ruksaka")

label = tk.Label(root, text="Višedimenzionalni problem ruksaka" , font=('Arial', 18))
label.pack(padx=20,pady=20)


podaci= tk.Label(root, text="Podaci")
podaci_combobox = ttk.Combobox(root, values=["test1_1.txt","test1_2.txt","test1_3.txt","test1_4.txt","test1_5.txt",
                                            "test2_1.txt","test2_2.txt","test2_3.txt","test2_4.txt","test2_5.txt",
                                            "test3_1.txt","test3_2.txt","test3_3.txt","test3_4.txt","test3_5.txt"])
podaci.pack()
podaci_combobox.pack(padx=20, pady=10)

maks_iter = tk.Label(root, text="Maksimalni broj iteracija").pack()
maks_iter_entry = tk.Text(root, height=1, width=3)
maks_iter_entry.pack(padx=20, pady=10)




buttonframe = tk.Frame(root)
buttonframe.columnconfigure(0, weight=1)
buttonframe.columnconfigure(1, weight=1)
buttonframe.columnconfigure(2, weight=1)

def load_items_from(file_name):                     # ucitavanje podataka o predmetima iz datoteke s imenom file_name
    
    items = []
   
    file_path = os.path.join('Testni podaci',file_name)

    file_lines = open(file_path).readlines()
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

    file_path = os.path.join('Testni podaci',file_name)

    lines = open(file_path).readlines()
    return lines[-1].split()

def load_bag_from(file_name):                       # kreiranje ruksaka s podacima sadrzanima u datoteci file_name

    capacities = load_capacities_from(file_name)
    return (load_items_from(file_name), *capacities)

def greedy():
    podaci = podaci_combobox.get()
    if (podaci !=''):
        Label(root, text="Odabrali ste testni primjer " +  podaci + ". " + "Odabrani algoritam : Greedy ", font=('Arial, 12')).pack()
        ruksak= Knapsack(*load_bag_from(podaci))
        start = time.time()
        rj = greedy_rjesenje(ruksak)
        end = time.time()
        Label(root, text="Rezultat: " + str(rj) + "\n Potrebno vrijeme: " + str(round(end-start,3)) + " s", font=('Arial, 12')).pack()
    else:
        Label(root, text="Niste odabrali testni primjer!", font = ('Arial, 12')).pack()


btn1 = tk.Button(buttonframe, text="Greedy", font=('Arial', 18), command=greedy)
btn1.grid(row=1, column=0, sticky=tk.W+tk.E)

def tabu():
    podaci = podaci_combobox.get()
    maks_iterr = maks_iter_entry.get("1.0", "end-1c")
    
    if (podaci !='' and maks_iterr!=''):
        maks_iterr_int = int(maks_iterr)
        Label(root, text="Odabrali ste testni primjer " +  podaci + ". " + "Odabrani algoritam : Tabu Search. " + "Maksimalni broj iteracija = "+maks_iterr, font=('Arial, 12')).pack()
        
        bag = Knapsack(*load_bag_from(podaci), tabu_list = TabuList(200))
        start = time.time()
        rjesenje = bag.optimization_tabu(greedy_rjesenje, TabuSearch(maks_iterr_int), Neighborhood.first_improve)
        end = time.time()
        Label(root, text="Rezultat: " + str(rjesenje) + "\n Potrebno vrijeme: " + str(round(end-start,3)) + " s", font=('Arial, 12')).pack()
    else:
        Label(root, text="Niste odabrali testni primjer ili maksimalni broj iteracija!", font = ('Arial, 12')).pack()
    

btn2 = tk.Button(buttonframe, text="Tabu Search", font=('Arial', 18), command=tabu)
btn2.grid(row=1, column=1, sticky=tk.W+tk.E)

def genetski():
    podaci = podaci_combobox.get()
    podaci = os.path.join('Testni podaci', podaci)
    
    if (podaci !=''):
        Label(root, text="Odabrali ste testni primjer " +  podaci + ". " + "Odabrani algoritam : Genetski algoritam ", font=('Arial, 12')).pack()
        start = time.time()
        rj = main(podaci, 300)
        end = time.time()
        Label(root, text="Rezultat: " + str(rj[1]) + "\n Potrebno vrijeme: " + str(round(end-start,3)) + " s", font=('Arial, 12')).pack()
        

    else:
        Label(root, text="Niste odabrali testni primjer!", font = ('Arial, 12')).pack()
    


btn3 = tk.Button(buttonframe, text="Genetski algoritam", font=('Arial', 18), command=genetski)
btn3.grid(row=1, column=2, sticky=tk.W+tk.E)

def SAhillClimbing():         # steepst-ascent hill climbing
    podaci = podaci_combobox.get()
    maks_iterr = maks_iter_entry.get("1.0", "end-1c")
    
    if (podaci !='' and maks_iterr!=''):
        maks_iterr_int = int(maks_iterr)
        Label(root, text="Odabrali ste testni primjer " +  podaci + ". " + "Odabrani algoritam : Steepest-ascent Hill Climbing. " + "Maksimalni broj iteracija = " +maks_iterr, font=('Arial, 12')).pack()
        bag = Knapsack(*load_bag_from(podaci), tabu_list = TabuList(200))
        start = time.time()
        rj = bag.optimization_hill(greedy_rjesenje, SAHillClimbing(maks_iterr_int), Neighborhood.best)
        end = time.time()
        Label(root, text="Rezultat: " + str(rj) + "\n Potrebno vrijeme: " + str(round(end-start,3)) + " s", font=('Arial, 12')).pack()
        

    else:
        Label(root, text="Niste odabrali testni primjer ili maksimalni broj iteracija!", font = ('Arial, 12')).pack()

btn4 = tk.Button(buttonframe, text="Steepest-ascent Hill Climbing", font=('Arial', 18), command=SAhillClimbing)
btn4.grid(row=2, column=0, sticky=tk.W+tk.E)

def ShillClimbing():            # simple hill climbing
    podaci = podaci_combobox.get()
    maks_iterr = maks_iter_entry.get("1.0", "end-1c")
    
    if (podaci !=''):
        maks_iterr_int = int(maks_iterr)
        Label(root, text="Odabrali ste testni primjer " +  podaci + ". " + "Odabrani algoritam : Simple Hill Climbing. " + "Maksimalni broj iteracija = " + maks_iterr, font=('Arial, 12')).pack()
        bag = Knapsack(*load_bag_from(podaci), tabu_list = TabuList(200))
        start = time.time()
        rj = bag.optimization_hill(greedy_rjesenje, SHillClimbing(maks_iterr_int), Neighborhood.first_improve)
        end = time.time()
        Label(root, text="Rezultat: " + str(rj) + "\n Potrebno vrijeme: " + str(round(end-start,3)) + " s", font=('Arial, 12')).pack()
        

    else:
        Label(root, text="Niste odabrali testni primjer ili maksimalni broj iteracija!", font = ('Arial, 12')).pack()

btn5 = tk.Button(buttonframe, text="Simple Hill Climbing", font=('Arial', 18), command=ShillClimbing)
btn5.grid(row=2, column=1, sticky=tk.W+tk.E)

buttonframe.pack(fill='x')
        
root.mainloop()








