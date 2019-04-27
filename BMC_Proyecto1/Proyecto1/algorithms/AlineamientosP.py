import numpy as np
#TODO: agregar sección de #ayuda

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
    directions = ["", "⬅ ", "", "⬆ ", "⬅⬆ ", "⬉ ", "⬅⬉ ", "", "⬉⬆ ", "⬅⬉⬆ "]
    # directions = ["", "⬅", "", "⬆", "⬅⬆", "⬉", "⬅⬉", "", "⬉⬆", "⬅⬉⬆"]

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
def alineamientoGlobal(A, B, Match, Mismatch, GapA=-2, GapB=-2):
    matrixPesos, matrixFlechas, matrizWeb = matrizPesos_Global(A, B, Match, Mismatch, GapA, GapB)
    alineamientos = []
    # Encontrar el máximo de la matriz, global es la última casilla
    j = len(A)
    i = len(B)
    obtenerAlineamientosGeneral(matrixFlechas, A, B, matrixFlechas[i][j], i, j, "", "", alineamientos)
    return alineamientos, matrizWeb


# Alinea los trozos más similares de las cadenas dejando la cadena más larga completa y la más corta alineada
# con la parte más pequeña en el lugar de la misma parte en la más grande.
def alineamientoLocal(A, B, Match, Mismatch, GapA, GapB):
    matrixPesos, matrixFlechas, matrizWeb = matrizPesos_Local(A, B, Match, Mismatch, GapA, GapB)
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
def alineamientoSemiglobal(A, B, dondeBuscar, Match, Mismatch, GapA, GapB):
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
def obtenerAlineamientosGeneralCancion(matrixFlechas, A, B, code, i, j, Atemp, Btemp, alineamientos):
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
        elif code == 6:
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1
        elif code == 8:
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1
        else:
            # Diagonal
            Atemp = A[j - 1] + Atemp
            Btemp = B[i - 1] + Btemp
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1
    alineamientos += [(Atemp, Btemp)]


# Basado en el alineamiento Local, alinea las partes similares de una canción.
def alinearCanciones(A, B, porcentaje):
    matrixPesos, matrixFlechas = matrizPesos_Local(A, B)
    alineamientos = []

    # Vamos a normalizar la matriz de pesos
    max = np.amax(matrixPesos)
    matrixPesos = matrixPesos / max

    # Encontrar todos los valores que sean mayores al porcentaje indicado
    indices = np.argwhere(matrixPesos >= porcentaje)

    # Obtengo todos los trozos que sean similares
    # Por cada trozo similar me muestra todos los posibles alineamientos de este mismo
    for indice in indices:
        i = indice[0]
        j = indice[1]
        alineamientosTmp = []
        obtenerAlineamientosGeneralCancion(matrixFlechas, A, B, matrixFlechas[i][j], i, j, "", "", alineamientosTmp)
        alineamientos += alineamientosTmp

    return alineamientos


cancionPlayazClub = "Me and my homies, we tighter than a glove " + \
                    "We chop a lot of game is how we do it at the Playaz Club " + \
                    "Check the fool or kick it in the tub " + \
                    "'cause we kick much ass at the Playaz Club " + \
                    "I got a hoe named Real de Real " + \
                    "She got a buddy named SP 12, now, you know the deal " + \
                    "We getz freaky in the studio late night " + \
                    "That's why the beats that you hear are comin' real tight " + \
                    "Somethin' to roll to, somethin' to stroll to " + \
                    "If you's a playa in the game this will hold you " + \
                    "Mo money mo money for the bank roll " + \
                    "Stick to the script don't slip in the nine-fo " + \
                    "A lot of fools put salt in the game " + \
                    "Till when these women get the notion that they runnin' the game, huh " + \
                    "I run my own and I'm my own self person " + \
                    "No respect make the situation worse then " + \
                    "Fillmoe, H.P. and Sunnydale, there's a playaz club everywhere you dwell " + \
                    "Lakeview, P.H. and Army Street, a different part of town " + \
                    "A different kind of freak, I just wiggle my toes on a mink rug " + \
                    "And press play on the remote at the Playaz Club " + \
                    "Me and my homies, we tighter than a glove " + \
                    "We chop a lot of game is how we do it at the Playaz Club " + \
                    "Check the fool or kick it in the tub " + \
                    "'cause we kick much ass at the Playaz Club " + \
                    "More champagne, Mr. 4-Tay? " + \
                    "From day one, I had to get my money right " + \
                    "Me, Fly and Franky J we took a airplane flight, huh " + \
                    "They wanted to hear a rap, I said alright bet " + \
                    "We dropped the beat and grabbed the mic then they wrote a check " + \
                    "A few G's for the pocket no hesitation " + \
                    "Took a flight back to the Golden State and " + \
                    "Shops made orders from a whole new capital " + \
                    "The word was gettin' out 4-Tay's out rappable " + \
                    "Don't need a Glock but I bought one just in case " + \
                    "Suckas try to stop me from pursuin' my paper chase " + \
                    "'cause the chase is on because it don't stop " + \
                    "I got the beat and got the rap you make the Glock pop " + \
                    "So treacherous suckas couldn't sweat this on a bad day " + \
                    "By the way just in case you never heard " + \
                    "Rappin' 4-Tay, I'm on the smooth tip " + \
                    "Never trippin' off them suckas poppin' off at the lip " + \
                    "I pop the top off the drank and we can roll some dank, bro " + \
                    "Leave the gat at the house bring some Dominoes " + \
                    "Take off your shoes relax and get a body rub " + \
                    "And shoot your mackin' at these women at the Playaz Club " + \
                    "Me and my homies, we tighter than a glove " + \
                    "We chop a lot of game is how we do it at the Playaz Club " + \
                    "Check the fool or kick it in the tub " + \
                    "'cause we kick much ass at the Playaz Club " + \
                    "You can't resist it but don't get it twisted " + \
                    "V.I.P. that means the number's not listed " + \
                    "Membership is based on clout and how you carry yourself " + \
                    "Now, homie what you all about? " + \
                    "I stack paper and kick it with the O.G's " + \
                    "Some got a nine-to-five, some drink a lot of keys " + \
                    "You can learn a whole lot from a playa " + \
                    "A lot of these playas make a damn good rhyme sayer " + \
                    "A lot of people get a misconception " + \
                    "And start driftin' in the wrong direction " + \
                    "Miss Goody Two Shoes, see you later " + \
                    "I ain't got time you ain't nuthin' but a playa hater " + \
                    "I'd rather kick it with the crew in Arizona " + \
                    "They chop game like we do in California " + \
                    "Another show another flow a new bank account " + \
                    "But cash money comes in large amounts " + \
                    "So get your membership but never slip to lame fast " + \
                    "Or else us and fly will have to tap that ass " + \
                    "And drop you to the ground and make your knees scrub " + \
                    "It's just an everyday thang at the Playaz Club " + \
                    "Me and my homies, we tighter than a glove " + \
                    "We chop a lot of game is how we do it at the Playaz Club " + \
                    "Check the fool or kick it in the tub " + \
                    "'cause we kick much ass at the Playaz Club " + \
                    "Me and my homies, we tighter than a glove " + \
                    "We chop a lot of game is how we do it at the Playaz Club " + \
                    "Check the fool or kick it in the tub " + \
                    "'cause we kick much ass at the Sucka Free club " + \
                    "Yeah, I'd like to send this shout out " + \
                    "To all the Playaz Clubs throughout the world " + \
                    "I know they got a Playaz Club out there in Chicago " + \
                    "What about that one they got out there in Philly, Fo? " + \
                    "You know they got one out there in Atlanta, the way they by choppin' " + \
                    "Shit, Detroit, New York, Texas " + \
                    "Yeah, but we gonna move on down to these " + \
                    "Playaz Clubs close to home like Seattle, L.A., Bakersfield, San Diego " + \
                    "P.A., V-Town, Richmond, Sacramento " + \
                    "Yeah, but a special shot goes out to the " + \
                    "Playaz Club right across the water in the Biggity Biggity O " + \
                    "Yeah, and last but definitely not least yeah, them " + \
                    "Playa Clubs they got right there in the " + \
                    "San Francisco mothafuckin' bay, yeah " + \
                    "Where your Playaz Club at 4? " + \
                    "My Playaz Club right in the heart of Fillmoe " + \
                    "Uh, I feel you boy, where yours at Fly? " + \
                    "Man, on the corner of Third and Newcomb right in the heart of H.P. " + \
                    "Huh, this is for all you playaz out there mayne " + \
                    "We out at the Playaz Club"

cancionDrake = "I'm that nigga with the plugs " + \
               "I'm the nigga who got homies that be sellin' drugs " + \
               "I'm the nigga on the back street " + \
               "With the fat heat, niggas better run like athletes " + \
               "I'm that nigga, I'm that nigga " + \
               "My Bank of America account got six figures " + \
               "I'm that nigga on the block " + \
               "Police pull up, I'm tryna stash the Glock " + \
               "Uh, you that nigga on the low-low " + \
               "You're the nigga, you're the one that be talkin' to the po-pos " + \
               "Porsche sittin' on Forgi's " + \
               "Niggas can't afford these " + \
               "The Panamera shittin' on the 9-11 " + \
               "I call my homies, not 9-11 " + \
               "I'm the nigga with the juice " + \
               "But I'll never do my nigga like Pac did Q " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "I got a shorty name Texas Syn " + \
               "She got a buddy named Young JB and now you know the deal " + \
               "We turnt up in the studio late night " + \
               "That's why the songs that you hear are comin' real tight " + \
               "OVO crew, nigga, thought I told you " + \
               "If you a player in the game, this should hold you " + \
               "And man shout my nigga Game he just rolled through " + \
               "Eatin' crab out in Malibu at Nobu " + \
               "A lot of fools puttin' salt in the game " + \
               "Until these women get the notion that they runnin' the game " + \
               "They got money that they jumpin' on the pole to make " + \
               "Did the motto, took a flight to the golden state " + \
               "I'm the general, just makin' sure my soldiers straight " + \
               "Had to leave my nigga, homie got an open case " + \
               "But I'm big on the west like I'm big in the south " + \
               "So we gon' pay some people off, we gon' figure it out " + \
               "And my name too big, and my gang too big " + \
               "Young Money shit, me and Lil Wayne too big " + \
               "Imma crush that ass even if it ain't too big " + \
               "I would pinky swear but my pinky ring too big (Wassup) " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "I'm that nigga, I'm that nigga " + \
               "Bank of America account got six figures " + \
               "I'm that nigga on the block " + \
               "Fat heat, run like athletes " + \
               "I'm that nigga, I'm that nigga " + \
               "Bank of America account got six figures " + \
               "I'm that nigga on the block " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Bitch, who do you love? " + \
               "Nigga we street and we hood " + \
               "Ain't nobody ever gave us shit " + \
               "When you see us shinin' it's because we steady grindin' " + \
               "We stay paper chasin' " + \
               "Separatin' the real from the fake " + \
               "The fake from the real " + \
               "We livin' to die and dyin' to live! " + \
               "Nigga, that's why we got so many women " + \
               "I'm tryna go deep, hit them asscheeks " + \
               "Bust them guts, make her cum " + \
               "Bitch, you know the game! " + \
               "Ain't a motherfuckin' thing change! " + \
               "Bitch! Who do you love!?"

# print(alinearCanciones(cancionPlayazClub, cancionDrake, 1))

# Resultado, tarda al rededor de unos 30 segundos utilizando un valor de 1. Es decir, el valor más alto.
# Aún así hay problemas con los porcentajes, por ejmplo si se pide un valor mayor a .9
# Hace que se tomen alineamientos como holaaaaa holaaaa, holaaa holaaa, holaa holaa, hola hola. Diferencias minúsculas
# De apenas un caracter, lo que no tiene mucho sentido, se debe mejorar la forma en que se busquen.
# " She got a buddy named______ SP 12, now, you know the deal We getz freaky in the studio late night That's why the beats that you hear are comin' real tight Somethin' to roll to, somethin' to stroll to_ If you's a play_a in the game_ this __will hold you _Mo mon____ey mo money for the bank roll_ Stick to __the script don't slip in the nine-fo A lot of fools pu_t___ salt in the game Till when these women get the notion that they runnin' the game"
# " She got a buddy named Young JB and now_ you know the deal We __t_urnt up in the studio late night That's why the songs that you hear are comin' real tight OVO crew, _nigga, t___ho_ugh__t _I _t_old you If you__ a player in the game, this should hold you And man shout my nigga Game he just rolled through Eatin' cr_ab _o_ut __in Malibu at Nobu A lot of fools puttin' salt in the game ____Until these women get the notion that they runnin' the game"
