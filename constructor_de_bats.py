import sys
from os import listdir
from os.path import join, isfile

"""
Los dos argumentos son: 
Un archivo de texto que contenga los Kepler ID (de la forma kplrXXXXXXXXX) de todas las estrellas que se desean incluir en el script 
El folder en el que estan los .bat de los que se desea armar el nuevo script
"""

def explorar(estrellas, bat):
    f =  open(bat, "r")

    lineas = [linea.split(' ') for linea in f.readlines()]
    lista = []
    for linea in lineas:
        if linea[0] == "wget":
            for estrella in estrellas:
                if linea[2].split('-')[0].replace('\'', '') == estrella and linea[2].split('.')[1] == 'fits\'':
                    lista.append(" ".join(linea))
    return lista


estrellas_ar = sys.argv[1]
path = sys.argv[2]


f = open(estrellas_ar, "r")
g = open(estrellas_ar+".bat", "w")

estrellas = [i.rstrip() for i in f.readlines()]
script = []

dire = listdir(path)
for archivo in dire:
    if isfile(join(path, archivo)):
        script.extend(explorar(estrellas, join(path, archivo)))

for comando in script:
    g.write(comando)

g.close()
f.close()