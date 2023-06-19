"""
This is our main driver file. It will be responsible for handling user input and 
displaying the current GameState object.
"""
import pygame
import ejmChessEngine 

WIDTH = HEIGHT = 512
DIMENSION = 8 # demensiones del tablero
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animation later on
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called exactly once in the main
"""
def loadImages():
    pieces = ['nP','nT','nC','nA','nD','nR','bP','bT','bC','bA','bD','bR']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(
            pygame.image.load('img/' + piece + '.png'), (SQ_SIZE, SQ_SIZE))

"""
The main driver for our code. This will handle user input and updating the graphics
"""
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color('white'))
    gs = ejmChessEngine.GameState()
    loadImages() #only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected, keep track of the last click of the user (tuple: (row,col))
    playerClicks = [] #keep track of player clicks (two tuples: [(6,4),(4,4)])
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() #(x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row,col): #the user clicked the same square twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row,col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after 2nd click
                    move = ejmChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #reset user clicks
                    playerClicks = []
                
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()

"""
Responsible for all the graphics within a current game state
"""
def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    # add in piece highlighting or move suggetions (later)
    drawPieces(screen, gs.board) #draw pieces on top od those squares
"""
Draw the squares on the board. The top left square is always light
"""
def drawBoard(screen):
    colors = [pygame.Color('white'), pygame.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
"""
Draw the pieces on the board using current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--': # not empty square
                screen.blit(IMAGES[piece], pygame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
