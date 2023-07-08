import random

puntosPiezas = {'R':0, 'D':10, 'T':5, 'A':3, 'C':3, 'P':1}
CHECKMATE = 1000
STALEMATE = 0

'''
elegir y retornar un movimiento random
'''
def encontrarMovRandom(movValidos):
    return movValidos[random.randint(0, len(movValidos)-1)]

'''
encontrar el mejor movimiento basado solo en el material
'''
def encontrarMejorMov(gs, movValidos):
    turnoMultiplicador = 1 if gs.muevenBlancas else -1
    puntajeOponenteMinMax = CHECKMATE
    mejorMovjugador = None
    random.shuffle(movValidos)
    for movJugador in movValidos:
        gs.mover(movJugador)
        movOponentes = gs.getMovValidos()
        puntajeMaxOponente = -CHECKMATE
        for movOpo in movOponentes:
            gs.mover(movOpo)
            if gs.checkMate:
                puntaje = -turnoMultiplicador * CHECKMATE
            elif gs.tablas_staleMate:
                puntaje = STALEMATE
            else:
                puntaje = -turnoMultiplicador * valorMaterial(gs.tablero)
            if puntaje > puntajeMaxOponente:
                puntajeMaxOponente = puntaje
            gs.deshacerMov()
        if  puntajeMaxOponente < puntajeOponenteMinMax:
            puntajeOponenteMinMax = puntajeMaxOponente
            mejorMovjugador = movJugador
        gs.deshacerMov()
        
    return mejorMovjugador

'''
puntaje del tablero basado en el material
'''
def valorMaterial(tablero):
    puntaje = 0
    for f in tablero:
        for casilla in f:
            if casilla[0] == 'b':
                puntaje += puntosPiezas[casilla[1]]
            elif casilla[0] == 'n':
                puntaje -= puntosPiezas[casilla[1]]
    return puntaje


