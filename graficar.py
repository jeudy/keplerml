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
    plt.plot(arreglo[0], arreglo[1], 'r.')
    plt.ylabel('Flux')
    plt.xlabel('Time')
    plt.title(archivo)
    plt.savefig(archivo+".png", bbox_inches="tight")
    plt.gcf().clear()

def graficar_varios(archivos):
    """
    Grafica varios archivos .fits en un solo grafico
    """
    for archivo in archivos:
        arreglo = lightcurve(archivo)
        plt.plot(arreglo[0], arreglo[1], 'r.')
    plt.ylabel('Flux')
    plt.xlabel('Time')
    plt.title(archivos[0].split('-')[0])
    plt.savefig(archivos[0].split('-')[0]+".png", bbox_inches="tight")
    plt.gcf().clear()


path = sys.argv[1]
# archivo = sys.argv[1]
# graficar(archivo)
archivos = listdir(path)
f = open(path+'/estrellas.inf', 'r')
lista = [i.rstrip() for i in f.readlines()]
f.close()

archivos_fits = [[] for i in lista]

for archivo in archivos:
    if isfile(join(path, archivo)):
        if archivo.split('.')[1] == 'fits':
            for i in range(len(lista)):
                if archivo.split('-')[0] == lista[i]:
                    archivos_fits[i].append(join(path, archivo))

try:
    # for archivo in archivos_fits:
    #     #print(archivo)
    #     graficar(archivo)
    #     #print("ok")
    for files in archivos_fits:
        graficar_varios(files)
except IOError:
    print("BZZT")