import random
import numpy as np

def fitness_function(C):
    suma = 0
    for i in range(n):
        suma += V[i] * C[i]
    return suma

def crossover1(A, B):
    C = [0 for i in range(n)]
    for i in range(n):
        a = random.randint(0,1)
        if(a == 0):
            C[i] = A[i]
        else:
            C[i] = B[i]
    return C

def crossover2(A, B):
    a = random.randint(0,n-1)
    C = A
    for i in range(a, n):
        C[i] = B[i]
    return C

def mutiraj(C):
    a = random.randint(0, n-1)
    C[a] = abs(C[a] - 1)
    a = random.randint(0, n-1)
    C[a] = abs(C[a] - 1)
    return C

def provjeri_kapacitet():
    for i in range(m):
        if(R[i] > B[i]):
            return 1
    return 0

def update(R, j, korak):
    for i in range(m):
        if(korak == -1):
            R[i] -= W[i][j]
        else:
            R[i] += W[i][j]
        
def provjeri_update(R, j):
    for i in range(m):
        if(R[i] + W[i][j] > B[i]):
            return 0
    return 1

def stvori(C):
    R = [0 for i in range(m)]
    for i in range(m):
        for j in range(n):
            R[i] += C[j]*W[i][j]
    return R

def najmanji(P):
    mini = 0
    najmanji_do_sada = fitness_function(P[0])
    for i in range(1,len(P)):
        if(fitness_function(P[i]) < najmanji_do_sada):
            najmanji_do_sada = fitness_function(P[i])
            mini = i
    return mini

def najveci(P):
    maxi = 0
    najveci_do_sada = fitness_function(P[0])
    for i in range(1,len(P)):
        if(fitness_function(P[i]) > najveci_do_sada):
            maxi = i
            najveci_do_sada = fitness_function(P[i])
    return maxi

def odaberi_roditelje(P):
    A = P
    Rez = []
    p1 = najveci(A) # vraca indeks jedinke s najvecom fitness funkcijom
    P1 = A[p1] # uzimamo tu jedinku
    A = np.delete(A, p1, 0)
    drugi = najveci(A)
    P2 = A[drugi]
    Rez.append(P1)
    Rez.append(P2)
    return Rez
    
def ratio(n, m):
    A = [0 for i in range(n)]
    for i in range(n):
        suma = 0
        for j in range(m):
            suma += W[j][i]
        A[i] = V[i]/suma
    return A

def repair(C, W):
    A = ratio(n, m) # vraca listu omjera vrijednosti i tezine za svaki predmet
    R = stvori(C)
    W = np.array(W) # moramo transponirati matricu jer se moraju sortirati stupci (predmeti)
    A, W, C = zip(*sorted(zip(A, W.transpose(), C))) # sortiramo liste W i C po omjerima sadrzanim u A
    A = list(A) # kada unzipamo dobijemo tuple-ove pa ih moramo pretvoriti u listu da mozemo raditi dalje s njima
    R = list(R)
    W = np.array(W).transpose() # vracamo u pocetni oblik
    W = list(W)
    C = list(C)
    
    for i in range(m):
        for j in range(n):
            R[i] += W[i][j] * C[j]
    for j in range(n-1,0,-1):
        if(C[j] == 1 and provjeri_kapacitet() == 1):
            C[j] = 0
            update(R, j, -1)
    for j in range(n):
        if(C[j] == 0 and provjeri_update(R, j) == 1):
            C[j] = 1
            update(R, j, 1)
    return C

def inicijaliziraj():
    P = [[0 for i in range(n)] for j in range(100)] # pocetna populacija od 100 jedinki
    J = [i for i in range(n)]
    for k in range(100):
        R = [0 for i in range(m)]
        T = [i for i in range(n)]
        j = random.choice(T)
        T.remove(j)
        while(provjeri_update(R, j)):
            P[k][j] = 1
            update(R, j, 1)
            j = random.choice(T)
            T.remove(j)
    return P

def genetic_algorithm():
    t = 0
    P = inicijaliziraj()
    Fitness = [0 for i in range(len(P))]
    for i in range(len(P)):
        Fitness[i] = fitness_function(P[i])
    P_t = max(Fitness)
    indeks = najveci(P)
    while t < 100:
        roditelji = odaberi_roditelje(P)
        P1 = roditelji[0]
        P2 = roditelji[1]
        C = crossover1(P1, P2)
        C = repair(mutiraj(C), W)
        if(C in P):
            continue
        value_C = fitness_function(C)
        index = najmanji(P)
        P[index] = C
        if(value_C > P_t):
            P_t = value_C
            indeks = index
        t = t + 1
    return P[indeks],P_t

f = open("test3.txt")
prvi = f.readline()
prvi = prvi.split(' ')
n = int(prvi[0])
m = int(prvi[1])
drugi = f.readline().replace('\n','').split(' ')
V = [0 for i in range(n)]
for i in range(n):
    V[i] = int(drugi[i])
    
W = [[0 for i in range(n)] for j in range(m)]
for i in range(m):
    l = f.readline()
    l = l.replace('\n','').split(' ')
    for j in range(n):
        W[i][j] = int(l[j])

B = [0 for i in range(m)]
l = f.readline().replace('\n','').split(' ')
for i in range(m):
    B[i] = int(l[i])
    
U = ratio(n,m)   
R = [0 for i in range(m)]
Rjesenja = genetic_algorithm()
print(Rjesenja)
