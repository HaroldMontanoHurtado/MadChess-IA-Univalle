"""
Esta clase es responsable de almacenar todos la informacion de los estados actuales del juego de ajedrez. 
Tambien será responsable de determinar los movimientos valido del estado actual. 
Tambien mantendrá un registro de movimientos.
"""
class GameState():
    def __init__(self):
        # tablero de 8x8.
        # La primera letra representa si la pieza es negra o blanca, 'n' o 'b', respectivamente.
        #'--' representa espacios blancos, vacios.
        self.tablero = [
            ['nT','nC','nA','nD','nR','nA','nC','nT'],
            ['nP','nP','nP','nP','nP','nP','nP','nP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['bT','bC','bA','bD','bR','bA','bC','bT']]
        self.whiteToMove = True
        self.registroMov = []
        
    def mover(self, movimiento): #makeMove
        self.tablero[movimiento.startRow][movimiento.startCol] = '--'
        self.tablero[movimiento.endRow][movimiento.endCol] = movimiento.pieceMoved
        self.registroMov.append(movimiento) #registrar el movimiento para que lo deshagamos más tarde
        self.whiteToMove = not self.whiteToMove #swap players

class Movimiento():
    # map keys values
    # key : value
    ranksToRow = {
        '1':7,'2':6,'3':5,'4':4,
        '5':3,'6':2,'7':1,'8':0}
    # ahora invertimos el roll de llave valor
    rowToRanks = {v:k for k,v in ranksToRow.items()}
    filesToCols = {
        'a':0,'b':1,'c':2,'d':3,
        'e':4,'f':5,'g':6,'h':7}
    colsToFiles = {v:k for k,v in filesToCols.items()}
    
    def __init__(self,startSq,endSq,board): # Sq: square
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
    
    def getChessNotation(self):
        # puedes agregar para hacer esto como una notación de ajedrez real
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
    
    def getRankFile(self,c,r):
        return self.colsToFiles[c] + self.rowToRanks[r]
