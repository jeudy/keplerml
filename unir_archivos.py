import sys

from os import listdir
from os.path import join, isfile

def leer(path):
    f = open(path, "r")
    conjunto = set([i.rstrip() for i in f.readlines()])
    f.close()
    return conjunto

path = sys.argv[1]
archivos = listdir(path)
conjunto = set()

g = open(path, "w")

for archivo in archivos:
    if isfile(join(path, archivo)):
        conjunto |= leer(join(path, archivo))

for estrella in conjunto:
    g.write(estrella + '\n')

g.close()
