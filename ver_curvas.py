#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import matplotlib.pyplot as plt
from matplotlib import animation
from lightcurve import lightcurve
import numpy as np
#Load the digits dataset

fig = plt.figure("Visualizacion de Curvas de Kepler")
ax = fig.add_subplot(111, title="-")

# La función plot devuelve 2 objetos, por eso la , en la asignación

sp = ax.plot([], [], 'r+')[0]

path = sys.argv[1]

archivos = os.listdir(path)

def update(i):
    filename = archivos[i].split('-')[0].replace('kplr', '')
    print "Revisando ", filename
    ax.set_title("Kepler ID: {}".format(filename))
    arreglo = lightcurve(path + "/" + archivos[i])
    ax.set_ylim(min(arreglo[3]), max(arreglo[3]))
    ax.set_xlim(min(arreglo[0]), max(arreglo[0]))
    sp.set_data(arreglo[0], arreglo[3])
    return sp,None

ani = animation.FuncAnimation(fig, update, frames=len(archivos), interval=2000, repeat=False)

plt.show()
