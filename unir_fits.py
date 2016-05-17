import sys
from os import listdir
from os.path import join

import numpy as np 
from astropy.io import fits

import lightcurve

"""
Crea un FITS basado en los datos de una carpeta con FITS
"""

dire = sys.argv[1]

archivos = listdir(dire)
archivos.sort()

datos = []
for i in range(20):
    datos.append([])

for archivo in archivos:
    datos_ar = lightcurve.lightcurve(join(dire, archivo))
    for i in range(len(datos)):
        datos[i].extend(datos_ar[i])

table_hdu = fits.open(join(dire,archivos[0]))[1]

columnas_lista = [str(i).split(';') for i in table_hdu.columns]
columnas_lista = [[k.split('=')[1].strip()[1:-1] for k in i] for i in columnas_lista]

columnas_astropy = []

for i in range(len(columnas_lista)):
    if len(columnas_lista[i]) == 3:
        columnas_astropy.append(fits.Column(name=columnas_lista[i][0], format=columnas_lista[i][1], disp=columnas_lista[i][2], array=datos[i]))
    else:
        columnas_astropy.append(fits.Column(name=columnas_lista[i][0], format=columnas_lista[i][1], unit=columnas_lista[i][2], disp=columnas_lista[i][3], array=datos[i]))

tabla = fits.BinTableHDU.from_columns(columnas_astropy)
tabla.writeto(archivos[0].split('_')[0].split('-')[0]+'.fits')