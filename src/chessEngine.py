"""
Esta clase es responsable de almacenar todos la informacion de los estados actuales del juego de ajedrez. 
Tambien será responsable de determinar los movimientos valido del estado actual. 
Tambien mantendrá un registro de movimientos.
"""
class GameState():
    def __init__(self):
        # tablero de 8x8.
        # La primera letra representa si la pieza es negra o blanca, 'n' o 'b', respectivamente.
        # '--' representa espacios blancos, vacios.
        self.tablero = [
            ['nT','nC','nA','nD','nR','nA','nC','nT'],
            ['nP','nP','nP','nP','nP','nP','nP','nP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['bT','bC','bA','bD','bR','bA','bC','bT']]
        self.muevenBlancas = True
        # solo blancas, porque para negras seria negar este permiso (not muevenBlancas)
        self.logMovimientos = []
    """
    toma un movimiento como parámetro y lo ejecuta
    (esto no funcionará para enroque, promoción de peón y captura al paso)
    """
    def mover(self, movimiento): #makeMove
        self.tablero[movimiento.startRow][movimiento.startCol] = '--'
        self.tablero[movimiento.endRow][movimiento.endCol] = movimiento.piezaMovida
        self.logMovimientos.append(movimiento) # registrar el movimiento para que lo deshagamos más tarde
        self.muevenBlancas = not self.muevenBlancas # swap players
    """
    deshacer el ultimo movimiento hecho
    """
    def deshacerMov(self):
        if len(self.logMovimientos) != 0:
            mov = self.logMovimientos.pop() # Cerciorarse de que haya un movimiento para deshacer
            self.tablero[mov.startRow][mov.startCol] = mov.piezaMovida
            self.tablero[mov.endRow][mov.endCol] = mov.piezaCapturada
            self.muevenBlancas = not self.muevenBlancas # el switch retrocede
    """
    All moves considering checks
    """
    def getMovValidos(self):
        return self.getTodoPosiblesMov() # por ahora no vamos a preocuparnos por los checks
    """
    All moves without considering checks
    """
    def getTodoPosiblesMov(self):
        movimientos = []
        for fil in range(len(self.tablero)): # numero de filas
            for col in range(len(self.tablero[fil])): # numero de cols
                turno = self.tablero[fil][col][0]
                if (turno == 'b' and self.muevenBlancas) or (turno == 'n' and not self.muevenBlancas):
                    pieza = self.tablero[fil][col][1]
                    if pieza == 'P':
                        self.getMovPeon(fil, col, movimientos)
                    if pieza == 'T':
                        self.getMovTorre(fil, col, movimientos)
        return movimientos
    """
    obtenga todos los movimientos de peón para el peón ubicado en fila, columna y agregue estos movimientos a la lista
    """
    def getMovPeon(self, fil, col, mov):
        # Mueven peones blancos
        if self.muevenBlancas:
            if self.tablero[fil-1][col] == '--': #1 peón avanza una casilla
                mov.append(Movimiento((fil,col), (fil-1, col), self.tablero))
                if fil == 6 and self.tablero[fil-2][col] == '--': #2 peón avanza dos casillas
                # si el peon esta al inicio (fil==6), entonces puede avanzar 2 casillas
                    mov.append(Movimiento((fil,col), (fil-2,col), self.tablero))
            if col-1 >= 0: # capturado a la diagonal izquierda
                if self.tablero[fil][col][0] == 'b': # pieza enemiga capturada
                    mov.append(Movimiento((fil,col),(fil-1,col-1),self.tablero))
            if col+1 <= 7: # capturado a la diagonal derecha
                if self.tablero[fil-1][col+1][0] == 'b': # pieza enemiga capturada
                    mov.append(Movimiento((fil,col),(fil-1,col+1),self.tablero))
        # Mueven peones negros
        else:
            pass
    """
    obtenga todos los movimientos de torre para el torre ubicado en fila, columna y agregue estos movimientos a la lista
    """
    def getMovTorre(self, fil, col, mov):
        pass
    def getMovCab(self, fil, col, mov):
        pass
    def getMovAlfil(self, fil, col, mov):
        pass
    def getMovDama(self, fil, col, mov):
        pass
    def getMoRey(self, fil, col, mov):
        pass

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
        self.startRow = startSq[0] # clic de fila  inicial
        self.startCol = startSq[1] # clic de columna inicial
        self.endRow = endSq[0] # clic de fila final
        self.endCol = endSq[1] # clic de columna final
        self.piezaMovida = board[self.startRow][self.startCol]
        self.piezaCapturada = board[self.endRow][self.endCol]
    
    def getChessNotation(self):
        # puedes agregar para hacer esto como una notación de ajedrez real
        return self.getRankFile(self.startRow,self.startCol) + ' ' + self.getRankFile(self.endRow,self.endCol)
    
    def getRankFile(self,c,r):
        return self.colsToFiles[c] + self.rowToRanks[r]
