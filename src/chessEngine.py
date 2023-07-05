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
            ['--','nT','--','--','--','--','--','--'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['bT','bC','bA','bD','bR','bA','bC','bT']]
        self.funcionesMov = {
            'P':self.getMovPeon, 'T':self.getMovTorre, 'C':self.getMovCab,
            'A':self.getMovAlfil, 'D':self.getMovDama, 'R':self.getMovRey}
        self.muevenBlancas = True
        # solo blancas, porque para negras seria negar este permiso (not muevenBlancas)
        self.logMovimientos = []
        self.reyBlancoUbicacion = (7,4)
        self.reyNegroUbicacion = (0,4)
        self.checkMate = False
        self.tablas_stalemate = False
    """
    toma un movimiento como parámetro y lo ejecuta
    (esto no funcionará para enroque, promoción de peón y captura al paso)
    """
    def mover(self, movimiento): #makeMove
        self.tablero[movimiento.filInicial][movimiento.colInicial] = '--'
        self.tablero[movimiento.filFinal][movimiento.colFinal] = movimiento.piezaMovida
        self.logMovimientos.append(movimiento) # registrar el movimiento para que lo deshagamos más tarde
        self.muevenBlancas = not self.muevenBlancas # swap players
        # actualizar la ubicacion del rey si es movido
        if movimiento.piezaMovida == 'bR':
            self.reyBlancoUbicacion = (movimiento.filFinal, movimiento.colFinal)
        elif movimiento.piezaMovida == 'nR':
            self.reyNegroUbicacion = (movimiento.filFinal, movimiento.colFinal)
    """
    deshacer el ultimo movimiento hecho
    """
    def deshacerMov(self):
        if len(self.logMovimientos) != 0:
            mov = self.logMovimientos.pop() # Cerciorarse de que haya un movimiento para deshacer
            self.tablero[mov.filInicial][mov.colInicial] = mov.piezaMovida
            self.tablero[mov.filFinal][mov.colFinal] = mov.piezaCapturada
            self.muevenBlancas = not self.muevenBlancas # el switch retrocede
            # actualizar la ubicacion del rey si es actualizada
            if mov.piezaMovida == 'bR':
                self.reyBlancoUbicacion = (mov.filInicial, mov.colInicial)
            elif mov.piezaMovida == 'nR':
                self.reyNegroUbicacion = (mov.filInicial, mov.colInicial)
    """
    All moves considering checks
    """
    def getMovValidos(self):
        #1) generar todos los posibles movimientos
        movs = self.getTodoPosiblesMov()
        #2) por cada movimiento, realizar el movimiento
        for i in range(len(movs)-1, -1, -1):
            self.mover(movs[i])
            #3) generar todos los movimientos del oponente, ver si atacan a tu rey
            #4) para cada uno de los movimientos de tu oponente, mira si atacan a tu rey
            self.muevenBlancas = not self.muevenBlancas
            if self.chequear():
                movs.remove(movs[i]) #5) si atacan a tu rey, movimiento no válido
            self.muevenBlancas = not self.muevenBlancas
            self.deshacerMov()
        if len(movs) == 0:
            if self.chequear():
                self.checkMate = True
            else :
                self.tablas_stalemate = True
        else:
            self.checkMate = False
            self.tablas_stalemate = False
        
        return movs
    
    def chequear(self):
        if self.muevenBlancas:
            return self.sqBajoAtaque(self.reyBlancoUbicacion[0], self.reyBlancoUbicacion[1])
        else:
            return self.sqBajoAtaque(self.reyNegroUbicacion[0], self.reyNegroUbicacion[1])
    
    def sqBajoAtaque(self, fil, col):
        self.muevenBlancas = not self.muevenBlancas # cambiar al turno enemigo
        oponenteMueve = self.getTodoPosiblesMov()
        self.muevenBlancas = not self.muevenBlancas # regresar el turno anterior
        for m in oponenteMueve:
            if m.filFinal == fil and m.colFinal == col: # cuadro (sq) bajo ataque
                return True
        return False
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
                    self.funcionesMov[pieza](fil,col,movimientos)
        return movimientos
    """
    obtenga todos los movimientos de cada pieza para las piezas ubicadas en
    fila, columna y agregue estos movimientos a la lista
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
                if self.tablero[fil-1][col-1][0] == 'n': # pieza enemiga capturada
                    mov.append(Movimiento((fil,col),(fil-1,col-1),self.tablero))
            if col+1 <= 7: # capturado a la diagonal derecha
                if self.tablero[fil-1][col+1][0] == 'n': # pieza enemiga capturada
                    mov.append(Movimiento((fil,col),(fil-1,col+1),self.tablero))
        # Mueven peones negros
        else:
            if self.tablero[fil+1][col] == '--': #1 peón avanza una casilla
                mov.append(Movimiento((fil,col), (fil+1, col), self.tablero))
                if fil == 1 and self.tablero[fil+2][col] == '--': #2 peón avanza dos casillas
                # si el peon esta al inicio (fil==1), entonces puede avanzar 2 casillas
                    mov.append(Movimiento((fil,col), (fil+2,col), self.tablero))
            if col-1 >= 0: # capturado a la diagonal izquierda
                if self.tablero[fil+1][col-1][0] == 'b': # pieza enemiga capturada
                    mov.append(Movimiento((fil,col),(fil+1,col-1),self.tablero))
            if col+1 <= 7: # capturado a la diagonal derecha
                if self.tablero[fil+1][col+1][0] == 'b': # pieza enemiga capturada
                    mov.append(Movimiento((fil,col),(fil+1,col+1),self.tablero))
        # Agregar la promoción de peón más adelante
    
    def getMovTorre(self, fil, col, mov):
        # visto desde el punto de las blancas
        direcciones = ((-1,0),(0,-1),(1,0),(0,1)) # up, left, down, right
        colorEnemigo = 'n' if self.muevenBlancas else 'b' # enemigos: negros, en otro caso: blancos
        for d in direcciones:
            for i in range(1,8):
                filFinal = fil + d[0]*i
                colFinal = col + d[1]*i
                if 0 <= filFinal < 8 and  0 <= colFinal < 8: # en tablero
                    piezaFinal = self.tablero[filFinal][colFinal]
                    if piezaFinal == '--': # espacio vacio valido
                        mov.append(Movimiento((fil,col),(filFinal,colFinal),self.tablero))
                    elif piezaFinal[0] == colorEnemigo:
                        mov.append(Movimiento((fil,col),(filFinal,colFinal),self.tablero))
                        break
                    else: # pieza invalidada amigablemente
                        break
                else: # fuera del tablero
                    break
    
    def getMovCab(self, fil, col, mov):
        movCaballo = ((-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2))
        colorAliado = 'b' if self.muevenBlancas else 'n'
        for m in movCaballo:
            filFinal = fil + m[0]
            colFinal = col + m[1]
            if 0 <= filFinal < 8 and 0 <= colFinal < 8:
                piezaFinal = self.tablero[filFinal][colFinal]
                # verifica que no haya aliados (ocupada solo espacios vacios o enemigos)
                if piezaFinal[0] != colorAliado:
                    mov.append(Movimiento((fil,col),(filFinal,colFinal),self.tablero))
    
    def getMovAlfil(self, fil, col, mov):
        direcciones = ((-1,-1),(-1,1),(1,-1),(1,1)) #4 diagonales
        colorEnemigo = 'n' if self.muevenBlancas else 'b' # enemigos: negros, en otro caso: blancos
        for d in direcciones:
            for i in range(1,8): # el alfil solo puede moverse un max de 7 casillas
                filFinal = fil + d[0]*i
                colFinal = col + d[1]*i
                if 0 <= filFinal < 8 and  0 <= colFinal < 8: # en tablero
                    piezaFinal = self.tablero[filFinal][colFinal]
                    if piezaFinal == '--': # espacio vacio valido
                        mov.append(Movimiento((fil,col),(filFinal,colFinal),self.tablero))
                    elif piezaFinal[0] == colorEnemigo:
                        mov.append(Movimiento((fil,col),(filFinal,colFinal),self.tablero))
                        break
                    else: # pieza invalidada amigablemente
                        break
                else: # fuera del tablero
                    break
    
    def getMovDama(self, fil, col, mov):
        # combinamos los movimientos de las torres y alfiles
        self.getMovTorre(fil,col,mov)
        self.getMovAlfil(fil,col,mov)
    
    def getMovRey(self, fil, col, mov):
        movRey = ((-1,-1),(-1,1),(-1,0),(0,1),(1,0),(0,-1),(1,-1),(1,1))
        colorAliado = 'b' if self.muevenBlancas else 'n'
        for i in range(8):
            filFinal = fil + movRey[i][0]
            colFinal = col + movRey[i][1]
            if 0 <= filFinal < 8 and 0 <= colFinal < 8:
                piezaFinal = self.tablero[filFinal][colFinal]
                # verifica que no haya aliados (ocupada solo espacios vacios o enemigos)
                if piezaFinal[0] != colorAliado:
                    mov.append(Movimiento((fil,col),(filFinal,colFinal),self.tablero))

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
    
    def __init__(self,inicialSq,finalSq,board): # Sq: square
        self.filInicial = inicialSq[0] # clic de fila  inicial
        self.colInicial = inicialSq[1] # clic de columna inicial
        self.filFinal = finalSq[0] # clic de fila final
        self.colFinal = finalSq[1] # clic de columna final
        self.piezaMovida = board[self.filInicial][self.colInicial]
        self.piezaCapturada = board[self.filFinal][self.colFinal]
        self.movID = self.filInicial*1000 + self.colInicial*100 + self.filFinal*10 + self.colFinal
    """
    Overriding the equals method
    """
    def __eq__(self, other):
        if isinstance(other, Movimiento):
            return self.movID == other.movID
        return False
    
    def getChessNotation(self):
        # puedes agregar para hacer esto como una notación de ajedrez real
        return self.getRankFile(self.filInicial,self.colInicial) + ' ' + self.getRankFile(self.filFinal,self.colFinal)
    
    def getRankFile(self,c,r):
        return self.colsToFiles[c] + self.rowToRanks[r]
