import numpy as np 
import matplotlib.pyplot as plt 

from dtw import dtw

a = np.linspace(0, 10, num=100)

x = np.cos(a)
y = np.sin(a)

dist, cami = dtw(x, y)
print("La distancia entre las funciones es: "+str(dist)) #2.57969421349

cami_x = [i[0] for i in cami]
cami_y = [i[1] for i in cami]

plt.plot(cami_x, cami_y)
plt.show()

y = x+5

dist, cami = dtw(x, y)
print("La distancia entre las funciones es: "+str(dist)) #50.2493781056

cami_x = [i[0] for i in cami]
cami_y = [i[1] for i in cami]

plt.plot(cami_x, cami_y)
plt.show()

#como se puede ver, aunque en el segundo caso las se;ales son mas parecidas que en el primer caso, estan mas lejos que en el primer caso