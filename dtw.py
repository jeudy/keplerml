import numpy as np 

def dtw(x, y):
    """ Devuelve una lista de indices que corresponden al camino mas corto entre dos se;ales temporales y la distancia 
        de ese camino
        
        x y y son las funciones a las que se les aplicara el DTW
    
    """

    distancias = np.zeros((len(y), len(x)))

    x = x[~np.isnan(x)]
    y = y[~np.isnan(y)]

    for i in range(len(y)):
        for j in range(len(x)):
            distancias[i,j] = (y[i]-x[j])**2

    costo_acumulado = np.zeros((len(y), len(x)))

    costo_acumulado[0,0] = distancias[0,0]

    for j in range (1, len(x)):
        costo_acumulado[0, j]= distancias[0, j] + costo_acumulado[0, j-1]

    for i in range (1, len(y)):
        costo_acumulado[i, 0]= distancias[i, 0] + costo_acumulado[i-1, 0]

    for i in range(1, len(y)):
        for j in range(1, len(x)):
            costo_acumulado[i, j] = min(costo_acumulado[i-1, j-1], costo_acumulado[i-1, j], costo_acumulado[i, j-1]) + distancias[i,j]

    camino = [[len(x)-1, len(y)-1]]

    i = len(y)-1
    j = len(x)-1

    while i > 0 and j > 0:
        if i == 0:
            j = j - 1

        elif j == 0:
            i = i - 1

        else:
            if costo_acumulado[i-1, j] == min(costo_acumulado[i-1, j-1], costo_acumulado[i-1, j], costo_acumulado[i, j-1]):
                i = i - 1
            elif costo_acumulado[i, j-1] == min(costo_acumulado[i-1, j-1], costo_acumulado[i-1, j], costo_acumulado[i, j-1]):
                j = j - 1
            else:
                i = i - 1
                j = j - 1

        camino.append([j, i])
    camino.append([0, 0])
    lista_distancias = []
    
    for i in range(len(camino)):
        lista_distancias.append(distancias[camino[i][1], camino[i][0]])
    
    distancia_total = 0
    for i in range(len(lista_distancias)):
        distancia_total = distancia_total + lista_distancias[i]
    
    distancia_total = np.sqrt(distancia_total)

    return(distancia_total, camino) #El camino sirve para ver la relacion entre las se;ales (Entre mas diagonal, las se;ales son mas parecidas)
                                    #sin enbargo que las se;ales sean similares no quiere decir que esten cerca