import numpy as np

import time

def lookForSub(aligments, subA, subB):
    for aligment in aligments:
        if subA in aligment[0] and subB in aligment[1]:
            return False
    return True

# Alineamiento basado en el Local, se utilizará para alinear canciones.
def matrizPesos_Cancion(A, B, Match=1, Mismatch=-1, GapA=-2, GapB=-2):
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
                matrixFlechas[i][j] = 1
            elif upValue == matrix[i][j]:
                matrixFlechas[i][j] = 3
            elif diagonalValue == matrix[i][j]:
                matrixFlechas[i][j] = 5
            elif 0 == matrix[i][j]:
                matrixFlechas[i][j] = 0

    return matrix, matrixFlechas


# # Interpreta la matriz de flechas al igual que en todos los demás algoritmos.
# # Está versión para las canciones está limitada a recorrer un único camino.
# def obtenerAlineamientosGeneralCancion(matrixFlechas, A, B, code, i, j, Atemp, Btemp, alineamientos):
#     while code != 0:
#         if code == 1:
#             # Izquierda
#             Atemp = A[j - 1] + Atemp
#             Btemp = '_' + Btemp
#             code = matrixFlechas[i][j - 1]
#             j = j - 1
#         elif code == 3:
#             # Arriba
#             Atemp = '_' + Atemp
#             Btemp = B[i - 1] + Btemp
#             code = matrixFlechas[i - 1][j]
#             i = i - 1
#         elif code == 5:
#             # Diagonal
#             Atemp = A[j - 1] + Atemp
#             Btemp = B[i - 1] + Btemp
#             code = matrixFlechas[i - 1][j - 1]
#             i = i - 1
#             j = j - 1
#
#     alineamientos += [(Atemp, Btemp)]
#
#
# # Basado en el alineamiento Local, alinea las partes similares de una canción.
# def alinearCanciones(A, B, porcentaje):
#     matrixPesos, matrixFlechas = matrizPesos_Cancion(A, B)
#     alineamientos = []
#
#     # Vamos a normalizar la matriz de pesos
#     max = np.amax(matrixPesos)
#     matrixPesos = matrixPesos / max
#
#     # Encontrar todos los valores que sean mayores al porcentaje indicado
#     indices = np.argwhere(matrixPesos >= porcentaje)
#
#     # Obtengo todos los trozos que sean similares
#     # Por cada trozo similar me muestra todos los posibles alineamientos de este mismo
#     for indice in indices:
#         i = indice[0]
#         j = indice[1]
#         alineamientosTmp = []
#         obtenerAlineamientosGeneralCancion(matrixFlechas, A, B, matrixFlechas[i][j], i, j, "", "", alineamientosTmp)
#         alineamientos += alineamientosTmp
#
#     return alineamientos
#
#work
# # Interpreta la matriz de flechas al igual que en todos los demás algoritmos.
# # Está versión para las canciones está limitada a recorrer un único camino.
# def obtenerAlineamientosGeneralCancion(matrixFlechas, code, i, j):
#     while code != 0:
#         if code == 1:
#             # Izquierda
#             code = matrixFlechas[i][j - 1]
#             j = j - 1
#         elif code == 3:
#             # Arriba
#             code = matrixFlechas[i - 1][j]
#             i = i - 1
#         elif code == 5:
#             # Diagonal
#             code = matrixFlechas[i - 1][j - 1]
#             i = i - 1
#             j = j - 1
#
#     return i, j
#
#
# # Basado en el alineamiento Local, alinea las partes similares de una canción.
# def alinearCanciones(A, B, porcentaje, segmentacion):
#     matrixPesos, matrixFlechas = matrizPesos_Cancion(A, B)
#     alineamientos = []
#
#     # Vamos a normalizar la matriz de pesos
#     max = np.amax(matrixPesos)
#     matrixPesos = matrixPesos / max
#
#     # Encontrar todos los valores que sean mayores al porcentaje indicado
#     indices = np.argwhere(matrixPesos >= porcentaje)
#
#     # Obtengo todos los trozos que sean similares
#     # Por cada trozo similar me muestra todos los posibles alineamientos de este mismo
#     for indice in indices:
#         i = indice[0]
#         j = indice[1]
#         il, jl = obtenerAlineamientosGeneralCancion(matrixFlechas, matrixFlechas[i][j], i, j)
#
#         alineamientos.append((A[jl:j], B[il:i]))
#
#     return alineamientos


# Interpreta la matriz de flechas al igual que en todos los demás algoritmos.
# Está versión para las canciones está limitada a recorrer un único camino.
def obtenerAlineamientosGeneralCancion(matrixFlechas, code, i, j):
    while code != 0:
        if code == 1:
            # matrixPesos[i][j] = 0
            # Izquierda
            code = matrixFlechas[i][j - 1]
            j = j - 1
        elif code == 3:
            # matrixPesos[i][j] = 0
            # Arriba
            code = matrixFlechas[i - 1][j]
            i = i - 1
        elif code == 5:
            # matrixPesos[i][j] = 0
            # Diagonal
            code = matrixFlechas[i - 1][j - 1]
            i = i - 1
            j = j - 1

    return i, j


# Basado en el alineamiento Local, alinea las partes similares de una canción.
# El valor de porcentaje es un valor que indica que tan grande debe ser un pedazo de texto encontrado en B con respecto
# a A para ser considerado, es decir, si el valor es de 0.05% el texto encontrado en B debe representar un 5% de A
# El valor de segmentos indica que tantas busquedas se realizarán en la matriz de alineamientos. La matriz es dividida
# en segmentos para propiciar más busquedas y encontrar más duplicaciones de textos. Va de 0 a 1. Es un valor porcentual
# que divide la matriz en sectores según ese porcentaje, si el valor es 0.1 la matriz se divide en sectores del 10% de
# tamaño.
def alinearCanciones(A, B, porcentaje = 0.05, segmentos = 0.05):
    matrixPesos, matrixFlechas = matrizPesos_Cancion(A, B)

    largoA = len(matrixPesos[0])
    largoB = len(matrixPesos)

    # Dividir la matriz en bloques.
    largoBloqueA = int(largoA * segmentos)
    largoBloqueB = int(largoB * segmentos)

    bloquesA = [i for i in range(largoA, largoBloqueA, -largoBloqueA)] + [0]
    bloquesB = [i for i in range(largoB, largoBloqueB, -largoBloqueB)] + [0]

    alineamientos = []

    # Obtener los mejores indices de similitud por bloque.
    for x in range(1, len(bloquesB) - 1):
        for y in range(1, len(bloquesA) - 1):
            # Obtengo el bloque a procesar
            b_1, b_2 = bloquesB[x], bloquesB[x - 1]
            a_1, a_2 = bloquesA[y], bloquesA[y - 1]
            tmpMatrix = matrixPesos[b_1:b_2, a_1:a_2]

            # Obtengo los indices maximos dentro de ese bloque
            maximos = np.argwhere(tmpMatrix == np.amax(tmpMatrix))

            # Re ajusto los indices.
            indices = maximos + [b_1, a_1]

            # Alineo los mejores de cada segmento
            for indice in indices:
                i = indice[0]
                j = indice[1]
                il, jl = obtenerAlineamientosGeneralCancion(matrixFlechas, matrixFlechas[i][j], i, j)

                # Verifico que cumpla con el mínimo de porcentaje requerido
                largoCopiaB = j - jl
                if ((largoCopiaB / largoA) > porcentaje):
                    subA = A[jl:j]
                    subB = B[il:i]

                    # Verifico que no haya sido previamente agregado como uno mayor.
                    if lookForSub(alineamientos, subA, subB):
                        alineamientos.append((subA, subB))

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


start = time.time()
res = alinearCanciones(cancionPlayazClub, cancionDrake)
end = time.time()
print(end - start)


print(res)

# Resultado, tarda al rededor de unos 30 segundos utilizando un valor de 1. Es decir, el valor más alto.
# Aún así hay problemas con los porcentajes, por ejmplo si se pide un valor mayor a .9
# Hace que se tomen alineamientos como holaaaaa holaaaa, holaaa holaaa, holaa holaa, hola hola. Diferencias minúsculas
# De apenas un caracter, lo que no tiene mucho sentido, se debe mejorar la forma en que se busquen.
# " She got a buddy named______ SP 12, now, you know the deal We getz freaky in the studio late night That's why the beats that you hear are comin' real tight Somethin' to roll to, somethin' to stroll to_ If you's a play_a in the game_ this __will hold you _Mo mon____ey mo money for the bank roll_ Stick to __the script don't slip in the nine-fo A lot of fools pu_t___ salt in the game Till when these women get the notion that they runnin' the game"
# " She got a buddy named Young JB and now_ you know the deal We __t_urnt up in the studio late night That's why the songs that you hear are comin' real tight OVO crew, _nigga, t___ho_ugh__t _I _t_old you If you__ a player in the game, this should hold you And man shout my nigga Game he just rolled through Eatin' cr_ab _o_ut __in Malibu at Nobu A lot of fools puttin' salt in the game ____Until these women get the notion that they runnin' the game"
