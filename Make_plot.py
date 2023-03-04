import matplotlib.pyplot as plt
  


x = []
y = []
for line in open('SAHill_Rezultati 3.1.txt', 'r'):
    lines = [i for i in line.split()]
    x.append(lines[0])
    y.append(int(lines[1]))
      
plt.rcParams.update({'font.size': 6})

plt.title("Simple Hill Climbing")
plt.xlabel('Broj iteracija')
plt.ylabel('Maksimalna vrijednost ruksaka')
plt.yticks(y)
plt.plot(x, y, marker = 'o', c = 'g')
  
plt.show()
