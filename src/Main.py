"""
This is our main driver file. It will be responsible for handling user input and 
displaying the current GameState object.
"""
import pygame
import ChessEngine

ANCHO = ALTO = 800
DIMENSION = 8 # dimensiones del tablero
SQ_TAM = ALTO // DIMENSION # SQ: square, SQ_TAM=75
MAX_FPS = 15 # for animation later on
IMAGES = {}

"""
Inicializar un diccionario global de imagenes. Esto se llamará exactamente una vez en la pantalla principal.
"""
def cargarImg():
    piezas = ['nP','nT','nC','nA','nD','nR','bP','bT','bC','bA','bD','bR']
    for pieza in piezas:
        IMAGES[pieza] = pygame.transform.scale(
            pygame.image.load('img/' + pieza + '.png'), (SQ_TAM, SQ_TAM))

"""
El controlador principal de nuestro código.
Esto manejará la entrada del usuario y la actualización de los gráficos.
"""
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO,ALTO))
    reloj = pygame.time.Clock()
    pantalla.fill(pygame.Color('white'))
    gs = ChessEngine.GameState()
    movValidos = gs.getMovValidos()
    movHecho = False # variable indicadora para cuando se realiza un movimiento
    
    cargarImg() # solo haz esto una vez, antes del ciclo while
    running = True
    sqSeleccionado = () # no se selecciona ningún cuadrado, 
    # realice un seguimiento del último clic del usuario (tupla: (fila, columna))
    clicsDelJugador = [] # realizar un seguimiento de los clics de los jugadores (dos tuplas: [(6,4),(4,4)])
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # Eventos de MOUSE : mouse handler
            elif e.type == pygame.MOUSEBUTTONDOWN:
                ubicacionMouse = pygame.mouse.get_pos() #(x,y) ubicacion del mouse
                col = ubicacionMouse[0] // SQ_TAM
                fil = ubicacionMouse[1] // SQ_TAM
                if sqSeleccionado == (fil,col): # El usuario hizo clic en el mismo cuadrado dos veces.
                    sqSeleccionado = () # deseleccionar
                    clicsDelJugador = [] # borrar clics del jugador
                else:
                    sqSeleccionado = (fil,col)
                    clicsDelJugador.append(sqSeleccionado) # agregar tanto para el primer como para el segundo clic
                if len(clicsDelJugador) == 2: # después del segundo clic
                    movimiento = ChessEngine.Movimiento(clicsDelJugador[0], clicsDelJugador[1], gs.tablero)
                    print(movimiento.getChessNotation())
                    for i in range(len(movValidos)):
                        if movimiento == movValidos[i]:
                            gs.mover(movValidos[i])
                            movHecho = True
                            sqSeleccionado = () # restablecer clics de usuario
                            clicsDelJugador = []
                    if not movHecho:
                        clicsDelJugador = [sqSeleccionado]
            # Eventos de TECLADO : key handler
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z: # se deshace el mov al presionar 'z'
                    gs.deshacerMov()
                    movHecho = True
        if movHecho:
            animacionMov(gs.logMovimientos[-1], pantalla, gs.tablero, reloj)
            movValidos = gs.getMovValidos()
            movHecho = False
            
        dibujarEstadoJuego(pantalla, gs, movValidos, sqSeleccionado)
        reloj.tick(MAX_FPS)
        pygame.display.flip()
'''
Highlight square selected and moves for piece selected
'''
def resaltarCasillas(pantalla, gs, movValidos, sqSeleccionado):
    if sqSeleccionado != ():
        f,c = sqSeleccionado
        if gs.tablero[f][c][0] == ('b' if gs.muevenBlancas else 'n'): #sqSeleccionado es una pieza que puede ser movida
            # se resalta la casilla seleccionada
            s = pygame.Surface((SQ_TAM, SQ_TAM))
            s.set_alpha(100) # valor de transparencia -> 0 transparent; 255 opaque
            s.fill(pygame.Color('blue'))
            pantalla.blit(s, (c*SQ_TAM, f*SQ_TAM))
            # highlight moves from that square
            s.fill(pygame.Color('cyan'))
            for mov in movValidos:
                if mov.filInicial == f and mov.colInicial == c:
                    pantalla.blit(s, (mov.colFinal*SQ_TAM, mov.filFinal*SQ_TAM))

'''
Responsable de todos los gráficos dentro de un estado actual del juego
'''
def dibujarEstadoJuego(pantalla, gs, movValidos, sqSeleccionado):
    dibujarTablero(pantalla) #draw squares on the board
    resaltarCasillas(pantalla, gs, movValidos, sqSeleccionado)
    dibujarPiezas(pantalla, gs.tablero) #draw pieces on top od those squares
"""
Dibuja los cuadrados en la pizarra. El cuadrado superior izquierdo siempre es claro.
"""
def dibujarTablero(pantalla):
    global colores
    colores = [pygame.Color('#bac8d3'), pygame.Color('#18141d')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colores[((r+c) % 2)]
            pygame.draw.rect(pantalla, color, pygame.Rect(c*SQ_TAM, r*SQ_TAM, SQ_TAM, SQ_TAM))
"""
Dibuja las piezas en el tablero usando GameState.tablero actual
"""
def dibujarPiezas(pantalla, tablero):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pieza = tablero[r][c]
            if pieza != '--': # not empty square
                pantalla.blit(IMAGES[pieza], pygame.Rect(c*SQ_TAM, r*SQ_TAM, SQ_TAM, SQ_TAM))
'''
animar un movimientos
'''
def animacionMov(mov, pantalla, tablero, reloj):
    global colores
    dF = mov.filFinal - mov.filInicial
    dC = mov.colFinal - mov.colInicial
    framesPorSq = 10 # fotogramas para mover una casilla
    framesContador = (abs(dF) + abs(dC)) * framesPorSq
    for frame in range(framesContador + 1):
        f, c = (mov.filInicial + dF*frame/framesContador, mov.colInicial + dC*frame/framesContador)
        dibujarTablero(pantalla)
        dibujarPiezas(pantalla, tablero)
        #erase the piece moved from its ending square
        color = colores[(mov.filFinal + mov.colFinal) % 2]
        casillaFinal = pygame.Rect(mov.colFinal*SQ_TAM, mov.filFinal*SQ_TAM, SQ_TAM, SQ_TAM)
        pygame.draw.rect(pantalla, color, casillaFinal)
        # draw captured piece onto rectangle
        if mov.piezaCapturada != '--':
            pantalla.blit(IMAGES[mov.piezaCapturada], casillaFinal)
        #draw moving piece
        pantalla.blit(IMAGES[mov.piezaMovida], pygame.Rect(c*SQ_TAM, f*SQ_TAM, SQ_TAM, SQ_TAM))
        pygame.display.flip()
        reloj.tick(60)

if __name__ == "__main__":
    main()
