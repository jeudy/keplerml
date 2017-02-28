import os
import sys

archivos_descargados = os.listdir(sys.argv[1])
script = open(sys.argv[2], 'r')

archivos_script = script.readlines()
script.close()

for i in range(len(archivos_script)):
	archivos_script[i] = archivos_script[i].split(" ")[-1].split("/")[-1].strip('\n')

dif = set(archivos_script) - set(archivos_descargados)

archivos_faltantes = open("archivos_faltantes", 'w')

for archivo in dif:
	archivos_faltantes.write(archivo + '\n')

archivos_faltantes.close()