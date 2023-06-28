"""
This is our main driver file. It will be responsible for handling user input and 
displaying the current GameState object.
"""
import pygame
import ChessEngine 

ANCHO = ALTO = 600
DIMENSION = 8 # dimensiones del tablero
SQ_TAM = ALTO // DIMENSION # SQ: square
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
    cargarImg() # solo haz esto una vez, antes del ciclo while
    running = True
    sqSelected = () # no se selecciona ningún cuadrado, 
    # realice un seguimiento del último clic del usuario (tupla: (fila, columna))
    clicsDelJugador = [] # realizar un seguimiento de los clics de los jugadores (dos tuplas: [(6,4),(4,4)])
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                ubicacionMouse = pygame.mouse.get_pos() #(x,y) ubicacion del mouse
                col = ubicacionMouse[0] // SQ_TAM
                row = ubicacionMouse[1] // SQ_TAM
                if sqSelected == (row,col): # El usuario hizo clic en el mismo cuadrado dos veces.
                    sqSelected = () # deseleccionar
                    clicsDelJugador = [] # borrar clics del jugador
                else:
                    sqSelected = (row,col)
                    clicsDelJugador.append(sqSelected) # agregar tanto para el primer como para el segundo clic
                if len(clicsDelJugador) == 2: # después del segundo clic
                    movimiento = ChessEngine.Movimiento(clicsDelJugador[0], clicsDelJugador[1], gs.tablero)
                    print(movimiento.getChessNotation())
                    gs.mover(movimiento)
                    sqSelected = () # restablecer clics de usuario
                    clicsDelJugador = []
                
        dibujarEstadoJuego(pantalla, gs)
        reloj.tick(MAX_FPS)
        pygame.display.flip()

"""
Responsable de todos los gráficos dentro de un estado actual del juego
"""
def dibujarEstadoJuego(pantalla, gs):
    dibujarTablero(pantalla) #draw squares on the board
    # add in piece highlighting or move suggetions (later)
    dibujarPiezas(pantalla, gs.tablero) #draw pieces on top od those squares
"""
Dibuja los cuadrados en la pizarra. El cuadrado superior izquierdo siempre es claro.
"""
def dibujarTablero(pantalla):
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

if __name__ == "__main__":
    main()
