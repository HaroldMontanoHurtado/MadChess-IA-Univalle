import random

puntosPiezas = {'R':20, 'D':10, 'T':5, 'A':3, 'C':3, 'P':1}
CHECKMATE = 1000
STALEMATE = 0
PROFUNDIDAD = 3

'''
elegir y retornar un movimiento random
'''
def encontrarMovRandom(movValidos):
    return movValidos[random.randint(0, len(movValidos)-1)]

'''
encontrar el mejor movimiento basado solo en el material, minimax sin recursividad
'''
def encontrarMejorMovMinimaxSinRecursion(gs, movValidos):
    turnoMultiplicador = 1 if gs.muevenBlancas else -1
    puntajeOponenteMinMax = CHECKMATE
    mejorMovjugador = None
    random.shuffle(movValidos)
    for movJugador in movValidos:
        gs.mover(movJugador)
        movOponentes = gs.getMovValidos()
        if gs.tablas_staleMate:
            puntajeMaxOponente = STALEMATE
        elif gs.checkMate:
            puntajeMaxOponente = -CHECKMATE
        else:
            puntajeMaxOponente = -CHECKMATE
            for movOpo in movOponentes:
                gs.mover(movOpo)
                gs.getMovValidos()
                if gs.checkMate:
                    puntaje = CHECKMATE
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
metodo auxiliar para hacer el primer llamado recursivo
'''
def encontrarMejorMov(gs, movValidos):
    global sigMov, contador
    sigMov = None
    random.shuffle(movValidos)
    contador = 0
    #encontrarMovMinMax(gs, movValidos, PROFUNDIDAD, gs.muevenBlancas)
    #encontrarMovNegaMax(gs, movValidos, PROFUNDIDAD, 1 if gs.muevenBlancas else -1)
    encontrarMovNegaMaxAlfaBeta(gs, movValidos, PROFUNDIDAD, -CHECKMATE, CHECKMATE, 1 if gs.muevenBlancas else -1)
    #print(contador)
    
    return sigMov

def encontrarMovMinMax(gs, movValidos, profundidad, turnoBlancas):
    global sigMov
    if profundidad == 0:
        return valorMaterial(gs.tablero)
    
    if turnoBlancas:
        maxPuntaje = -CHECKMATE
        for mov in movValidos:
            gs.mover(mov)
            sigsMovs = gs.getMovValidos()
            puntaje = encontrarMovMinMax(gs, sigsMovs, profundidad-1, False)
            if puntaje > maxPuntaje:
                maxPuntaje = puntaje
                if profundidad == PROFUNDIDAD:
                    sigMov = mov
            gs.deshacerMov()
        return maxPuntaje
    
    else:
        minPuntaje = CHECKMATE
        for mov in movValidos:
            gs.mover(mov)
            sigsMovs = gs.getMovValidos()
            puntaje = encontrarMovMinMax(gs, sigsMovs, profundidad-1, True)
            if puntaje < minPuntaje:
                minPuntaje = puntaje
                if profundidad == PROFUNDIDAD:
                    sigMov = mov
            gs.deshacerMov()
        return minPuntaje

def encontrarMovNegaMax(gs, movValidos, profundidad, turnoMultiplicador):
    global sigMov, contador
    contador += 1
    if profundidad == 0:
        return turnoMultiplicador * puntajeTablero(gs)
    
    maxPuntaje = -CHECKMATE
    for mov in movValidos:
        gs.mover(mov)
        sigsMovs = gs.getMovValidos()
        puntaje = -encontrarMovNegaMax(gs, sigsMovs, profundidad-1, -turnoMultiplicador)
        if puntaje > maxPuntaje:
            maxPuntaje = puntaje
            if profundidad == PROFUNDIDAD:
                sigMov = mov
        gs.deshacerMov()
    
    return maxPuntaje

def encontrarMovNegaMaxAlfaBeta(gs, movValidos, profundidad, alfa, beta, turnoMultiplicador):
    global sigMov, contador
    contador += 1
    if profundidad == 0:
        return turnoMultiplicador * puntajeTablero(gs)
    
    #orden de movimiento - implementar más tarde
    maxPuntaje = -CHECKMATE
    for mov in movValidos:
        gs.mover(mov)
        sigsMovs = gs.getMovValidos()
        puntaje = -encontrarMovNegaMaxAlfaBeta(gs, sigsMovs, profundidad-1, -alfa, -beta, -turnoMultiplicador)
        if puntaje > maxPuntaje:
            maxPuntaje = puntaje
            if profundidad == PROFUNDIDAD:
                sigMov = mov
        gs.deshacerMov()
        if maxPuntaje > alfa: # ocurre la poda
            alfa = maxPuntaje
        if alfa >= beta:
            break
    
    return maxPuntaje

'''
un puntaje positivo es bueno para las blancas, y puntaje negativo es bueno para las negras
'''
def puntajeTablero(gs):
    if gs.checkMate:
        if gs.muevenBlancas:
            return -CHECKMATE #ganan negras
        else:
            return CHECKMATE #ganan blancas
    elif gs.tablas_staleMate:
        return STALEMATE
    
    puntaje = 0
    for f in gs.tablero:
        for sq in f:
            if sq[0] == 'b':
                puntaje += puntosPiezas[sq[1]]
            elif sq[0] == 'n':
                puntaje -= puntosPiezas[sq[1]]
    
    return puntaje

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


