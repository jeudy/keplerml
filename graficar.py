import sys
import matplotlib.pyplot as plt

from os import listdir
from os.path import join, isfile

from lightcurve import lightcurve

def graficar(archivo):
    """
    Grafica la curva de luz de un archivo .fits
    """
    arreglo = lightcurve(archivo)
    plt.plot(arreglo[0], arreglo[3], 'r+')
    plt.ylabel('Flux')
    plt.xlabel('Time')
    plt.title(archivo)
    # plt.savefig(archivo+".png", bbox_inches="tight")

    plt.show()

    plt.gcf().clear()

path = sys.argv[1]
archivo = sys.argv[1]
graficar(archivo)
