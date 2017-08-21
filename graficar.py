import sys
import matplotlib.pyplot as plt

from os import listdir
from os.path import join, isdir

from lightcurve import lightcurve

def graficar(path):
    """
    Grafica la curva de luz de un archivo .fits
    """
    if isdir(path):
        colors = ['b+','g+','r+','c+','m+','y+','k+']
        color_index = 0
        archivos = listdir(path)
        for archivo in archivos:
            arreglo = lightcurve(join(path, archivo))
            plt.plot(arreglo[0], arreglo[3], colors[color_index%len(colors)])
            color_index += 1
    else:
        arreglo = lightcurve(path)
        plt.plot(arreglo[0], arreglo[3], 'r+')
    plt.ylabel('Flux')
    plt.xlabel('Time')
    # plt.savefig(archivo+".png", bbox_inches="tight")

    plt.show()

    plt.gcf().clear()

path = sys.argv[1]
graficar(path)
