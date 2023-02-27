import tkinter as tk
from tkinter import ttk


class  Graficko:

    def __init__(self):

        self.root = tk.Tk()

        self.root.geometry("800x500")
        self.root.title("Višedimenzionalni problem ruksaka")

        self.label = tk.Label(self.root, text="Višedimenzionalni problem ruksaka" , font=('Arial', 18))
        self.label.pack(padx=20,pady=20)

        self.podaci= tk.Label(self.root, text="Podaci")
        self.podaci_combobox = ttk.Combobox(self.root, values=["test1", "test2", "test3"])
        self.podaci.pack()
        self.podaci_combobox.pack()

        self.buttonframe = tk.Frame(self.root)
        self.buttonframe.columnconfigure(0, weight=1)
        self.buttonframe.columnconfigure(1, weight=1)
        self.buttonframe.columnconfigure(2, weight=1)

        self.btn1 = tk.Button(self.buttonframe, text="Greedy", font=('Arial', 18))
        self.btn1.grid(row=1, column=0, sticky=tk.W+tk.E)

        self.btn2 = tk.Button(self.buttonframe, text="Tabu Search", font=('Arial', 18))
        self.btn2.grid(row=1, column=1, sticky=tk.W+tk.E)

        self.btn3 = tk.Button(self.buttonframe, text="Genetički algoritam", font=('Arial', 18))
        self.btn3.grid(row=1, column=2, sticky=tk.W+tk.E)

        self.buttonframe.pack(fill='x')


        self.root.mainloop()

Graficko()


