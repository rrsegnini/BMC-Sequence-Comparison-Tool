import numpy as np


def matrizParaWeb(A, B, matrizPesos, matrizFlechas):
    resultado = [["", "_"], ["_"]]
    # Agrear las letras de la cadena B en la primer columna
    # Por cada fila en la matriz (cadena B)
    for i in range(2, len(matrizPesos) + 1):
        resultado.append([B[i - 2]])

    # Agregar las letras de la cadena A en la primer fila
    # Por cada columna en la primer fila de la matriz (cadena A)
    for j in range(2, len(matrizPesos[0]) + 1):
        resultado[0].append(A[j - 2])

    # Agrear el resto de la matriz con las flechas.
    directions = ["", "⬅", "", "⬆", "⬅⬆", "⬉", "⬅⬉", "", "⬉⬆", "⬅⬉⬆"]

    for i in range(1, len(matrizPesos) + 1):
        for j in range(1, len(matrizPesos[0]) + 1):
            resultado[i].append(directions[matrizFlechas[i - 1][j - 1]] + str(matrizPesos[i - 1][j - 1]))

    return resultado


# Alineamiento Global, cálculo de la matriz
# Fuente: https://es.wikipedia.org/wiki/Algoritmo_Needleman-Wunsch
# El código es modificado para crear una matriz que indique las flechas de donde proviene cada puntaje.
# Recibe el string A y B a alinear, opcionalmente un valor para Match, Mismatch, Gap en string A y Gap en el string B.
# Retorna dos matrices, la de pesos, la de flechas que indica de donde provienen.
def matrizPesos_Global(A, B, Match=1, Mismatch=-1, GapA=-2, GapB=-2):
    lenA, lenB = len(A) + 1, len(B) + 1
    matrix = np.zeros((lenB, lenA), dtype=int)
    matrixFlechas = np.zeros((lenB, lenA), dtype=int)

    # izquierda
    for j in range(0, lenA):
        matrix[0][j] = j * GapB
        matrixFlechas[0][j] = 1
    # arriba
    for i in range(0, lenB):
        matrix[i][0] = i * GapA
        matrixFlechas[i][0] = 3

    # Llenar el inicio con el 0, que indica que no hay más camino (el final).
    matrixFlechas[0][0] = 0

    for i in range(1, lenB):
        for j in range(1, lenA):
            leftValue = matrix[i][j - 1] + GapB
            upValue = matrix[i - 1][j] + GapA
            diagonalValue = matrix[i - 1][j - 1]
            diagonalValue += Match if B[i - 1] == A[j - 1] else Mismatch

            matrix[i][j] = max(leftValue, upValue, diagonalValue)

            # Cambio del original, vamos a dar un peso en otra matriz indicando
            # de donde proviene el punto actual, dado un código
            if leftValue == matrix[i][j]:
                matrixFlechas[i][j] += 1
            if upValue == matrix[i][j]:
                matrixFlechas[i][j] += 3
            if diagonalValue == matrix[i][j]:
                matrixFlechas[i][j] += 5
    # print(matrix)
    matrizWeb = matrizParaWeb(A, B, matrix, matrixFlechas)
    return matrix, matrixFlechas, matrizWeb


# Alineamiento local y semiglobal, cálculo de la matriz
# Código base: https://es.wikipedia.org/wiki/Algoritmo_Needleman-Wunsch
# El código es modificado para crear una matriz que indique las flechas de donde proviene cada puntaje.
# Además para agregar el valor de cero al cálculo del máximo.
# Recibe el string A y B a alinear, opcionalmente un valor para Match, Mismatch, Gap en string A y Gap en el string B.
# Retorna dos matrices, la de pesos, la de flechas que indica de donde provienen.
def matrizPesos_Local(A, B, Match=1, Mismatch=-1, GapA=-2, GapB=-2):
    lenA, lenB = len(A) + 1, len(B) + 1
    matrix = np.zeros((lenB, lenA), dtype=int)
    matrixFlechas = np.zeros((lenB, lenA), dtype=int)

    for i in range(1, lenB):
        for j in range(1, lenA):
            leftValue = matrix[i][j - 1] + GapB
            upValue = matrix[i - 1][j] + GapA
            diagonalValue = matrix[i - 1][j - 1]
            diagonalValue += Match if B[i - 1] == A[j - 1] else Mismatch

            matrix[i][j] = max(leftValue, upValue, diagonalValue, 0)

            # Cambio del original, vamos a dar un peso en otra matriz indicando
            # de donde proviene el punto actual, dado un código
            if leftValue == matrix[i][j]:
                matrixFlechas[i][j] += 1
            if upValue == matrix[i][j]:
                matrixFlechas[i][j] += 3
            if diagonalValue == matrix[i][j]:
                matrixFlechas[i][j] += 5
            if 0 == matrix[i][j]:
                matrixFlechas[i][j] = 0

    # print(matrix)
    matrizWeb = matrizParaWeb(A, B, matrix, matrixFlechas)
    return matrix, matrixFlechas, matrizWeb


# Alineamiento SemiGlobal, cálculo de la matriz
# Código base: https://es.wikipedia.org/wiki/Algoritmo_Needleman-Wunsch
# El código es modificado para crear una matriz que indique las flechas de donde proviene cada puntaje.
# Recibe el string A y B a alinear, opcionalmente un valor para Match, Mismatch, Gap en string A y Gap en el string B.
# Retorna dos matrices, la de pesos, la de flechas que indica de donde provienen.
def matrizPesos_Semiglobal(A, B, Match=1, Mismatch=-1, GapA=-2, GapB=-2):
    lenA, lenB = len(A) + 1, len(B) + 1
    matrix = np.zeros((lenB, lenA), dtype=int)
    matrixFlechas = np.zeros((lenB, lenA), dtype=int)

    # izquierda
    for j in range(0, lenA):
        matrixFlechas[0][j] = 1
    # arriba
    for i in range(0, lenB):
        matrixFlechas[i][0] = 3

    # Llenar el inicio con el 0, que indica que no hay más camino (el final).
    matrixFlechas[0][0] = 0

    for i in range(1, lenB):
        for j in range(1, lenA):
            leftValue = matrix[i][j - 1] + GapB
            upValue = matrix[i - 1][j] + GapA
            diagonalValue = matrix[i - 1][j - 1]
            diagonalValue += Match if B[i - 1] == A[j - 1] else Mismatch

            matrix[i][j] = max(leftValue, upValue, diagonalValue)

            # Cambio del original, vamos a dar un peso en otra matriz indicando
            # de donde proviene el punto actual, dado un código
            if leftValue == matrix[i][j]:
                matrixFlechas[i][j] += 1
            if upValue == matrix[i][j]:
                matrixFlechas[i][j] += 3
            if diagonalValue == matrix[i][j]:
                matrixFlechas[i][j] += 5
    # print(matrix)
    matrizWeb = matrizParaWeb(A, B, matrix, matrixFlechas)
    return matrix, matrixFlechas, matrizWeb


# Interpreta la matriz de flechas para crear todos los strings de posibles alineamientos.
# Recibe por parámetro la matriz de flechas, ambos strings de los textos a alinear (A y B).
# Un código, que se encuentra en la casilla apuntada por i, j en la matriz de flechas.
# Los índices I y J, dos strins temporales para crear cada posible alineamiento.
# Finalmente una lista donde se almacenan todos los alineamientos obtenidos.
# Si el valor es cero, se acabo.
# Si es 1 proviene del izquierdo.
# Si es 3 proviene de arriba.
# Si es 5 proviene del diagonal.
# Si es 4 proviene de la izquierda y de arriba.
# si es 6 proviene de la izquierda y de la diagonal.
# si es 8 proviene de la arriba y de la diagonal.
# si es 9 proviene de los tres lugares posibles.
def obtenerAlineamientosGeneral(matrixFlechas, A, B, code, i, j, Atemp, Btemp, alineamientos):
    while code != 0:
        if code == 1:
            # Izquierda
            Atemp = A[j - 1] + Atemp
            Btemp = '_' + Btemp
            code = matrixFlechas[i][j - 1]
            j = j - 1
        elif code == 3:
            # Arriba
            Atemp = '_' + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j]
            i = i - 1
        elif code == 5:
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1
        elif code == 4:
            # Izquierda
            AtempI = A[j - 1] + Atemp
            BtempI = '_' + Btemp
            obtenerAlineamientosGeneral(matrixFlechas, A, B, matrixFlechas[i][j - 1], i, j - 1, AtempI, BtempI,
                                        alineamientos)
            # Arriba
            Atemp = '_' + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j]
            i = i - 1
        elif code == 6:
            # Izquierda
            AtempI = A[j - 1] + Atemp
            BtempI = '_' + Btemp
            obtenerAlineamientosGeneral(matrixFlechas, A, B, matrixFlechas[i][j - 1], i, j - 1, AtempI, BtempI,
                                        alineamientos)
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1
        elif code == 8:
            # Arriba
            AtempA = '_' + Atemp
            BtempA = B[i - 1] + Btemp
            obtenerAlineamientosGeneral(matrixFlechas, A, B, matrixFlechas[i - 1][j], i - 1, j, AtempA, BtempA,
                                        alineamientos)
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1
        else:
            # Arriba
            AtempA = '_' + Atemp
            BtempA = B[i - 1] + Btemp
            obtenerAlineamientosGeneral(matrixFlechas, A, B, matrixFlechas[i - 1][j], i - 1, j, AtempA, BtempA,
                                        alineamientos)
            # Izquierda
            AtempI = A[j - 1] + Atemp
            BtempI = '_' + Btemp
            obtenerAlineamientosGeneral(matrixFlechas, A, B, matrixFlechas[i][j - 1], i, j - 1, AtempI, BtempI,
                                        alineamientos)
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1

    alineamientos += [(Atemp, Btemp)]


# Interpreta la matriz de flechas para crear todos los strings de posibles alineamientos.
# Recibe por parámetro la matriz de flechas, ambos strings de los textos a alinear (A y B).
# Un código, que se encuentra en la casilla apuntada por i, j en la matriz de flechas.
# Los índices I y J, dos strins temporales para crear cada posible alineamiento.
# Un número para indicar que cadena terminará completa y cuál será rellenada con gaps, 1 para A, 2 para B.
# Finalmente una lista donde se almacenan todos los alineamientos obtenidos.
# Si el valor es cero, se acabo.
# Si es 1 proviene del izquierdo.
# Si es 3 proviene de arriba.
# Si es 5 proviene del diagonal.
# Si es 4 proviene de la izquierda y de arriba.
# si es 6 proviene de la izquierda y de la diagonal.
# si es 8 proviene de la arriba y de la diagonal.
# si es 9 proviene de los tres lugares posibles.
def obtenerAlineamientosLocal(matrixFlechas, A, B, code, i, j, Atemp, Btemp, cadenaCompleta, alineamientos):
    while code != 0:
        if code == 1:
            # Izquierda
            Atemp = A[j - 1] + Atemp
            Btemp = '_' + Btemp
            code = matrixFlechas[i][j - 1]
            j = j - 1
        elif code == 3:
            # Arriba
            Atemp = '_' + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j]
            i = i - 1
        elif code == 5:
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1
        elif code == 4:
            # Izquierda
            AtempI = A[j - 1] + Atemp
            BtempI = '_' + Btemp
            obtenerAlineamientosLocal(matrixFlechas, A, B, matrixFlechas[i][j - 1], i, j - 1, AtempI, BtempI,
                                      cadenaCompleta,
                                      alineamientos)
            # Arriba
            Atemp = '_' + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j]
            i = i - 1
        elif code == 6:
            # Izquierda
            AtempI = A[j - 1] + Atemp
            BtempI = '_' + Btemp
            obtenerAlineamientosLocal(matrixFlechas, A, B, matrixFlechas[i][j - 1], i, j - 1, AtempI, BtempI,
                                      cadenaCompleta,
                                      alineamientos)
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1
        elif code == 8:
            # Arriba
            AtempA = '_' + Atemp
            BtempA = B[i - 1] + Btemp
            obtenerAlineamientosLocal(matrixFlechas, A, B, matrixFlechas[i - 1][j], i - 1, j, AtempA, BtempA,
                                      cadenaCompleta,
                                      alineamientos)
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1
        else:
            # Arriba
            AtempA = '_' + Atemp
            BtempA = B[i - 1] + Btemp
            obtenerAlineamientosLocal(matrixFlechas, A, B, matrixFlechas[i - 1][j], i - 1, j, AtempA, BtempA,
                                      cadenaCompleta,
                                      alineamientos)
            # Izquierda
            AtempI = A[j - 1] + Atemp
            BtempI = '_' + Btemp
            obtenerAlineamientosLocal(matrixFlechas, A, B, matrixFlechas[i][j - 1], i, j - 1, AtempI, BtempI,
                                      cadenaCompleta,
                                      alineamientos)
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1

    if cadenaCompleta == 1:
        trozoFaltanteA = A[:j]
        Atemp = trozoFaltanteA + Atemp
        Btemp = "_" * (len(trozoFaltanteA)) + Btemp
    elif cadenaCompleta == 2:
        trozoFaltanteB = B[:i]
        Atemp = "_" * (len(trozoFaltanteB)) + Atemp
        Btemp = trozoFaltanteB + Btemp

    alineamientos += [(Atemp, Btemp)]


# Función para invocar el alineamiento global, hace la unión entre las matrices y la función que las interpreta.
# Se encarga de obtener la matriz de flechas, iniciar una lista para los resultados e invoca el código que interpreta
# la matriz de flechas, además de indicarle al código que interpreta las flechas desde que punto iniciar, es decir
# Encontrar el máximo según se necesita.
def alineamientoGlobal(A, B):
    matrixPesos, matrixFlechas, matrizWeb = matrizPesos_Global(A, B)
    alineamientos = []
    # Encontrar el máximo de la matriz, global es la última casilla
    j = len(A)
    i = len(B)
    obtenerAlineamientosGeneral(matrixFlechas, A, B, matrixFlechas[i][j], i, j, "", "", alineamientos)
    return alineamientos, matrizWeb


# Alinea los trozos más similares de las cadenas dejando la cadena más larga completa y la más corta alineada
# con la parte más pequeña en el lugar de la misma parte en la más grande.
def alineamientoLocal(A, B):
    matrixPesos, matrixFlechas, matrizWeb = matrizPesos_Local(A, B)
    alineamientos = []

    largoA = len(A)
    largoB = len(B)

    # Encontrar los máximos (indices), en toda la matrix (por si está varicas veces el mismo número)
    indices = np.argwhere(matrixPesos == np.amax(matrixPesos))
    for indice in indices:
        i = indice[0]
        j = indice[1]
        alineamientosTmp = []

        # Alinear la parte más pequeña de una cadena contra el total de la otra.
        # Quedará completa la cadena más larga, la más pequeña será rellenada con gaps y ajustada a la más grande..
        if largoB <= largoA:
            Atemp = A[j:]
            Btemp = "_" * (len(A) - j)
            obtenerAlineamientosLocal(matrixFlechas, A, B, matrixFlechas[i][j], i, j, Atemp, Btemp, 1,
                                      alineamientosTmp)
        else:
            Atemp = "_" * (len(B) - i)
            Btemp = B[i:]
            obtenerAlineamientosLocal(matrixFlechas, A, B, matrixFlechas[i][j], i, j, Atemp, Btemp, 2,
                                      alineamientosTmp)

        alineamientos += alineamientosTmp

    return alineamientos, matrizWeb


# Alineamiento semiglobal, si las cadenas no se alinean completamente, la más grande quedará completa, mientras
# que la más pequeña quedará rellenada con gaps para completar los largos.
# dondeBuscar es un parámetro que indica donde debo encontrar el máximo, por que el profesor dijo que debía preguntar.
# 1 para encontrarlo en la última fila, 2 para encontrarlo en la última columna
def alineamientoSemiglobal(A, B, dondeBuscar):
    matrixPesos, matrixFlechas, matrizWeb = matrizPesos_Semiglobal(A, B)
    alineamientos = []

    largoA = len(A)
    largoB = len(B)

    indices = []

    # Encontrar los máximos (indices), en toda la matrix (por si está varicas veces el mismo número)
    if dondeBuscar == 1:
        indices = np.argwhere(matrixPesos[-1] == np.amax(matrixPesos[-1]))
        idxTemp = []
        for index in indices:
            idxTemp.append([largoB, index[0]])
        indices = idxTemp
    elif dondeBuscar == 2:
        indices = np.argwhere(matrixPesos[:, -1] == np.amax(matrixPesos[:, -1]))
        idxTemp = []
        for index in indices:
            idxTemp.append([index[0], largoA])
        indices = idxTemp

    for indice in indices:
        i = indice[0]
        j = indice[1]
        alineamientosTmp = []

        # Hay que completar los alineamientos para que utilicen toda la cadena.
        # Si tengo que buscar en la ultima fila el string B estará completo (se ponen gaps en el).
        # SI tengo que buscar en la ultima columna el string A estará completo (se ponen gaps en el).

        if dondeBuscar == 1:
            Atemp = A[j:]
            Btemp = "_" * (len(A) - j)
            obtenerAlineamientosGeneral(matrixFlechas, A, B, matrixFlechas[i][j], i, j, Atemp, Btemp,
                                        alineamientosTmp)
        elif dondeBuscar == 2:
            Atemp = "_" * (len(B) - i)
            Btemp = B[i:]
            obtenerAlineamientosGeneral(matrixFlechas, A, B, matrixFlechas[i][j], i, j, Atemp, Btemp,
                                        alineamientosTmp)

        alineamientos += alineamientosTmp

    return alineamientos, matrizWeb


# print(alineamientoGlobal("GTACGTATC", "GTCCTAC"))
# print(alineamientoGlobal(a, a))
# print(alineamientoLocal("kkkkodakkkkk", "zzzkodakzzzz"))
# print(alineamientoSemiglobal("kkkkodakkkkk", "zzzkodakzzzz", 1))
# print(alineamientoGlobal("GTACGTATC", "GTCCTAC"))
# print(alineamientoSemiglobal("GTACGTATC", "GTCCTAC", 2))
# print(alineamientoLocal("GTACGTATC", "GTCCTAC"))
#
# A = "GTACGTATC"
# B = "GTCCTAC"
# matriz, matrizFlechas = matrizPesos_Global(A, B)
# matrizWeb = matrizParaWeb(A, B, matriz, matrizFlechas)
# print(matrizWeb)