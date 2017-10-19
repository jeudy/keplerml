import numpy as np 

from dtw import DTWDistance

a = np.linspace(0, 10, num=100)

x = np.cos(a)
y = np.sin(a)

dist = DTWDistance(x, y)
print("La distancia entre las funciones es: "+str(dist)) #2.37...

y = x+5

dist = DTWDistance(x, y)
print("La distancia entre las funciones es: "+str(dist)) #50.0


