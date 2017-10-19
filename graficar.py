import sys
import matplotlib.pyplot as plt

from os import listdir
from os.path import join, isdir

from lightcurve import lightcurve

def graficar(path, kepler_id=None, Q=None):
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
    if kepler_id and Q:
        plt.title('{0} for Q{1}'.format(kepler_id, Q))
    # plt.savefig(archivo+".png", bbox_inches="tight")

    plt.show()

    plt.gcf().clear()

path = sys.argv[1]
kepler_id = sys.argv[2]
Q = sys.argv[3]
graficar(path, kepler_id, Q)

