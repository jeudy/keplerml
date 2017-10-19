import numpy as np

def DTWDistance(lc1, lc2):
    """
    lc1 y lc2 son las lightcurve a las que se aplicara el DTW
    """
    DTW={} #DTW es un diccionario que representa una matriz de donde cada entrada representa la distancia entre dos puntos de lc1[i] y lc2[j]

    for i in range(len(lc1)):   #Aqui estamos diciendo que la distancia entre un punto cualquiera de una serie y el punto final de la otra es infinita
        DTW[(i,-1)] = float('inf')
    
    for i in range(len(lc2)):
        DTW[(-1,i)] = float('inf')

    DTW[(-1,-1)] = 0    #Aqui hacemos la salvedad de que los puntos finales de las series estan a la misma distancia

    for i in range(len(lc1)):   #Aqui vamos llenando la matriz, cada entrada (i, j) tiene la minima distancia para llegar a ella, por lo que la ultima entrada corresponde a la minima distancia entre lc1 y lc2
        for j in range(len(lc2)):
            dist = np.square(lc1[i] - lc2[j])
            DTW[(i,j)] = dist + min(DTW[(i-1, j)], DTW[(i, j-1)], DTW[(i-1, j-1)])
    return np.sqrt(DTW[len(lc1)-1, len(lc2)-1])
    
