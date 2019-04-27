#Alineamiento Global
#Fuente: https://es.wikipedia.org/wiki/Algoritmo_Needleman-Wunsch
#Cada elemento de la matriz es una lista
#Cada lista, a su vez, posee dos elementos:
#1. El valor de alineamiento
#2. Una sublista que contiene tres booleanos
#(banderas) indicando el lugar(es) de donde
#se viene el valor de alineamiento:
#(Izquierda, Diagonal, Arriba)
#3. Otra sublista con dos strings que
#corresponden al alineamiento de las hileras
#en esa casilla
def NeedlemanWunsch(A,B,Match,Mismatch,Gap):
    lenA, lenB = len(A)+1,len(B)+1
    Matrix = [[[0,[],["",""]] for x in range(lenA)] for y in range(lenB)]


    for j in range(0,lenA):
        for i in range(0,lenB):
            #Val = Matrix[i][j][0]
            LeftVal = Matrix[i][j-1][0]
            DiagVal = Matrix[i - 1][j - 1][0]
            UpVal = Matrix[i - 1][j][0]

            LeftAlign = Matrix[i][j - 1][2]
            UpAlign = Matrix[i - 1][j][2]
            DiagAlign = Matrix[i - 1][j - 1][2]

            if i == 0 and j == 0:
                Matrix[i][j][0] = 0
            elif i == 0:
                #LeftVal = Matrix[i][j-1][0]
                Matrix[i][j][0] = LeftVal + Gap
                Matrix[i][j][1] += ("Left",)

                Matrix[i][j][2][0] += LeftAlign[0] + A[j - 1]
                Matrix[i][j][2][1] += LeftAlign[1] + "_"


            elif j == 0:
                #UpVal = Matrix[i-1][j][0]
                Matrix[i][j][0] = UpVal + Gap
                Matrix[i][j][1] += ("Up",)

                Matrix[i][j][2][0] = UpAlign[0] + "_"
                Matrix[i][j][2][1] = UpAlign[1] + B[i - 1]

            else:
                LeftVal = LeftVal + Gap
                DiagVal = DiagVal + Match if A[j-1]==B[i-1] else Matrix[i-1][j-1][0] + Mismatch
                UpVal = UpVal + Gap

                MaxVal = max(LeftVal, DiagVal, UpVal)

                Matrix[i][j][0] = MaxVal

                if MaxVal == LeftVal:
                    Matrix[i][j][1] += ("Left",)
                    Matrix[i][j][2][0] += LeftAlign[0] + A[j - 1]
                    Matrix[i][j][2][1] += LeftAlign[1] + "_"
                if MaxVal == DiagVal:
                    Matrix[i][j][1] += ("Diagonal",)
                    Matrix[i][j][2][0] += DiagAlign[0] + A[j - 1]
                    Matrix[i][j][2][1] += DiagAlign[1] + B[i - 1]
                if MaxVal == UpVal:
                    Matrix[i][j][1] += ("Up",)
                    Matrix[i][j][2][0] = UpAlign[0] + "_"
                    Matrix[i][j][2][1] = UpAlign[1] + B[i - 1]



    return(Matrix)

#Alineamiento Semiglobal
#Cada elemento de la matriz es una lista
#Cada lista, a su vez, posee tres elementos:
#1. El valor de alineamiento
#2. Una sublista que contiene tres booleanos
#(banderas) indicando el lugar(es) de donde
#se viene el valor de alineamiento:
#(Izquierda, Diagonal, Arriba)
#3. Otra sublista con dos strings que
#corresponden al alineamiento de las hileras
#en esa casilla
def SemiGlobal(A,B,Match,Mismatch,Gap):
    lenA, lenB = len(A)+1,len(B)+1
    Matrix = [[[0,[],["",""]] for x in range(lenA)] for y in range(lenB)]


    for j in range(0,lenA):
        for i in range(0,lenB):
            #Val = Matrix[i][j][0]
            LeftVal = Matrix[i][j-1][0]
            DiagVal = Matrix[i - 1][j - 1][0]
            UpVal = Matrix[i - 1][j][0]

            LeftAlign = Matrix[i][j - 1][2]
            UpAlign = Matrix[i - 1][j][2]
            DiagAlign = Matrix[i-1][j-1][2]


            if i == 0 and j == 0:
                Matrix[i][j][0] = 0
            elif i == 0:
                #LeftVal = Matrix[i][j-1][0]
                Matrix[i][j][0] = 0
                Matrix[i][j][1] += ("Left",)
                Matrix[i][j][2][0] += LeftAlign[0] + A[j-1]
                Matrix[i][j][2][1] += LeftAlign[1] + "_"

            elif j == 0:
                Matrix[i][j][0] = 0
                Matrix[i][j][1] += ("Up",)
                Matrix[i][j][2][0] = UpAlign[0] + "_"
                Matrix[i][j][2][1] = UpAlign[1] + B[i - 1]

            else:
                LeftVal = LeftVal + Gap
                DiagVal = DiagVal + Match if A[j-1]==B[i-1] else Matrix[i-1][j-1][0] + Mismatch
                UpVal = UpVal + Gap



                MaxVal = max(LeftVal, DiagVal, UpVal)

                Matrix[i][j][0] = MaxVal

                if MaxVal == LeftVal:
                    Matrix[i][j][1] += ("Left",)
                    Matrix[i][j][2][0] += LeftAlign[0] + A[j - 1]
                    Matrix[i][j][2][1] += LeftAlign[1] + "_"

                elif MaxVal == DiagVal:
                    Matrix[i][j][1] += ("Diagonal",)
                    Matrix[i][j][2][0] += DiagAlign[0] + A[j - 1]
                    Matrix[i][j][2][1] += DiagAlign[1] + B[i - 1]
                elif MaxVal == UpVal:
                    Matrix[i][j][1] += ("Up",)
                    Matrix[i][j][2][0] += UpAlign[0] + "_"
                    Matrix[i][j][2][1] += UpAlign[1] + B[i - 1]



    return(Matrix)

#Alineamiento Local
#Cada elemento de la matriz es una lista
#Cada lista, a su vez, posee dos elementos:
#1. El valor de alineamiento
#2. Una sublista que contiene tres booleanos
#(banderas) indicando el lugar(es) de donde
#se viene el valor de alineamiento:
#(Izquierda, Diagonal, Arriba)
#3. Otra sublista con dos strings que
#corresponden al alineamiento de las hileras
#en esa casilla
def SmithWaterman(A,B,Match,Mismatch,Gap):
    lenA, lenB = len(A)+1,len(B)+1
    Matrix = [[[0,[],["",""]] for x in range(lenA)] for y in range(lenB)]


    for j in range(0,lenA):
        for i in range(0,lenB):
            #Val = Matrix[i][j][0]
            LeftVal = Matrix[i][j-1][0]
            DiagVal = Matrix[i - 1][j - 1][0]
            UpVal = Matrix[i - 1][j][0]

            LeftAlign = Matrix[i][j - 1][2]
            UpAlign = Matrix[i - 1][j][2]
            DiagAlign = Matrix[i - 1][j - 1][2]

            if i == 0 and j == 0:
                Matrix[i][j][0] = 0
            elif i == 0:
                Matrix[i][j][2][0] += LeftAlign[0] + A[j - 1]
                Matrix[i][j][2][1] += LeftAlign[1] + "_"


            elif j == 0:
                Matrix[i][j][2][0] = UpAlign[0] + "_"
                Matrix[i][j][2][1] = UpAlign[1] + B[i - 1]

            else:
                LeftVal = LeftVal + Gap
                DiagVal = DiagVal + Match if A[j-1]==B[i-1] else Matrix[i-1][j-1][0] + Mismatch
                UpVal = UpVal + Gap

                MaxVal = max(LeftVal, DiagVal, UpVal)
                if MaxVal > 0:
                    Matrix[i][j][0] = MaxVal
                else:
                    Matrix[i][j][0] = 0

                if MaxVal == LeftVal:
                    Matrix[i][j][1] += ("Left",)
                    Matrix[i][j][2][0] += LeftAlign[0] + A[j - 1]
                    Matrix[i][j][2][1] += LeftAlign[1] + "_"
                if MaxVal == DiagVal:
                    Matrix[i][j][1] += ("Diagonal",)
                    Matrix[i][j][2][0] += DiagAlign[0] + A[j - 1]
                    Matrix[i][j][2][1] += DiagAlign[1] + B[i - 1]
                if MaxVal == UpVal:
                    Matrix[i][j][1] += ("Up",)
                    Matrix[i][j][2][0] = UpAlign[0] + "_"
                    Matrix[i][j][2][1] = UpAlign[1] + B[i - 1]



    return(Matrix)
