import sys
from os import listdir
from os.path import join, isfile

def lista_estrellas(archivo):
    f = open(archivo, "r")
    g = open(archivo.split('.')[0]+"2", "w")

    lineas = [linea.split(' ') for linea in f.readlines()]
    lista = set()
    for linea in lineas:
        if linea[0] == "wget":
            lista.add(linea[2].split('-')[0])

    for linea in lista:
        g.write(linea.replace('\'', '')+'\n')

    f.close()
    g.close()

def lista_estrellas_directorio(directorio):
    dire = listdir(directorio)
    for archivo in dire:
        if isfile(join(directorio, archivo)):
            lista_estrellas(join(directorio, archivo))


ruta = sys.argv[1]
lista_estrellas_directorio(ruta)
