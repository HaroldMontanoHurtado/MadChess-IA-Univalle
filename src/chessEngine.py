"""
Esta clase es responsable de almacenar todos la informacion de los estados actuales del juego de ajedrez. 
Tambien será responsable de determinar los movimientos valido del estado actual. 
Tambien mantendrá un registro de movimientos.
"""
class GameState():
    def __init__(self):
        '''
        tablero de 8x8.
        La primera letra representa si la pieza es negra o blanca, 'n' o 'b', respectivamente.
        '--' representa espacios blancos, vacios.
        '''
        self.tablero = [
            ['nT','nC','nA','nD','nR','nA','nC','nT'],
            ['nP','nP','nP','nP','nP','nP','nP','nP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['bT','bC','bA','bD','bR','bA','bC','bT']] # ['bT','bC','bA','bD','bR','bA','bC','bT']
        self.funcionesMov = {
            'P':self.getMovPeon, 'T':self.getMovTorre, 'C':self.getMovCab,
            'A':self.getMovAlfil, 'D':self.getMovDama, 'R':self.getMovRey}
        self.muevenBlancas = True
        # solo blancas, porque para negras seria negar este permiso (not muevenBlancas)
        self.logMovimientos = []
        self.reyBlancoUbicacion = (7,4)
        self.reyNegroUbicacion = (0,4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkMate = False
        self.tablas_staleMate = False
        self.posibleCaptAlPaso = () # casilla donde puede ocurrir la captura al pasar
        self.logPosiblesEnPass = [self.posibleCaptAlPaso]
        # derechos de enroque || castling rights
        self.actualDerechoEnrocar = DerechosEnroque(True, True, True, True)
        self.logDerechosEnroque = [DerechosEnroque(
            self.actualDerechoEnrocar.ebr, self.actualDerechoEnrocar.enr,
            self.actualDerechoEnrocar.ebd, self.actualDerechoEnrocar.end)]
        
    """
    toma un movimiento como parámetro y lo ejecuta
    (esto no funcionará para enroque, promoción de peón y captura al paso)
    """
    def mover(self, movs): #makeMove
        self.tablero[movs.filInicial][movs.colInicial] = '--'
        self.tablero[movs.filFinal][movs.colFinal] = movs.piezaMovida
        self.logMovimientos.append(movs) # registro de movs
        self.muevenBlancas = not self.muevenBlancas # cambio de turno || switch turn
        # actualizar la ubicacion del rey si es movido
        if movs.piezaMovida == 'bR':
            self.reyBlancoUbicacion = (movs.filFinal, movs.colFinal)
        elif movs.piezaMovida == 'nR':
            self.reyNegroUbicacion = (movs.filFinal, movs.colFinal)
        
        # si el peón se mueve dos veces, el próximo movimiento puede capturar al paso
        if movs.piezaMovida[1] == 'P' and abs(movs.filInicial - movs.filFinal) == 2:
            self.posibleCaptAlPaso = ((movs.filFinal + movs.filInicial)//2, movs.colFinal)
        else:
            self.posibleCaptAlPaso = ()
        # si se mueve al paso, debe actualizar el tablero para capturar el peón
        if movs.alPaso:
            self.tablero[movs.filInicial][movs.colFinal] = '--'
        # si la promoción de peón cambia de pieza
        if movs.promocionPeon:
            #piezaPromovida = input('Promove a D, T, A or C: ') #podemos hacer que esto sea parte de la interfaz de usuario más tarde
            piezaPromovida = 'D'
            self.tablero[movs.filFinal][movs.colFinal] = movs.piezaMovida[0] + piezaPromovida
        
        self.logPosiblesEnPass.append(self.posibleCaptAlPaso)
        
        # movimientos de enroque
        if movs.enroque:
            if movs.colFinal - movs.colInicial == 2:
                self.tablero[movs.filFinal][movs.colFinal - 1] = self.tablero[movs.filFinal][movs.colFinal + 1] # mover torre
                self.tablero[movs.filFinal][movs.colFinal + 1] = '--' # espacio vacío donde estaba la torre
            else:
                self.tablero[movs.filFinal][movs.colFinal + 1] = self.tablero[movs.filFinal][movs.colFinal - 2] # mover torre
                self.tablero[movs.filFinal][movs.colFinal - 2] = '--' # espacio vacío donde estaba la torre
        # actualizar los derechos de enroque
        self.actualizarDerechosEnroque(movs)
        self.logDerechosEnroque.append(DerechosEnroque(
            self.actualDerechoEnrocar.ebr, self.actualDerechoEnrocar.enr, self.actualDerechoEnrocar.ebd, self.actualDerechoEnrocar.end))
        
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
            
            #deshacer captura al paso es diferente
            if mov.alPaso:
                self.tablero[mov.filFinal][mov.colFinal] = '--' #elimina el peón que se agregó en el cuadro equivocado
                self.tablero[mov.filInicial][mov.colInicial] = mov.piezaCapturada #vuelve a poner el peón en la casilla correcta de la que fue capturado
                
                self.logPosiblesEnPass.pop()
                self.posibleCaptAlPaso = self.logPosiblesEnPass[-1]
            
            #dehacer los derechos del enroque
            self.logDerechosEnroque.pop() # eliminar las actualizaciones de los últimos movimientos
            nuevosDerechos = self.logDerechosEnroque[-1]
            self.derechoActualEnroque = DerechosEnroque(nuevosDerechos.ebr, nuevosDerechos.enr, nuevosDerechos.ebd, nuevosDerechos.end)
            
            #deshacer enroque
            if mov.enroque:
                if mov.colFinal - mov.colInicial == 2: # flanco del rey
                    self.tablero[mov.filFinal][mov.colFinal + 1] = self.tablero[mov.filFinal][mov.colFinal - 1] # mover torre
                    self.tablero[mov.filFinal][mov.colFinal - 1] = '--' # espacio vacío donde estaba la torre
                else: # flanco de dama
                    self.tablero[mov.filFinal][mov.colFinal - 2] = self.tablero[mov.filFinal][mov.colFinal + 1] # mover torre
                    self.tablero[mov.filFinal][mov.colFinal + 1] = '--' # espacio vacío donde estaba la torre
            
            #ADD THESE
            self.checkMate = False
            self.tablas_staleMate = False
        
    '''
    Todos los movimientos considerando checks (jaque) || All moves considering checks
    '''
    def getMovValidos(self):
        movs = []
        self.inCheck, self.pins, self.checks = self.chequearPinsYChecks()
        
        if self.muevenBlancas:
            reyFil = self.reyBlancoUbicacion[0]
            reyCol = self.reyBlancoUbicacion[1]
        else:
            reyFil = self.reyNegroUbicacion[0]
            reyCol = self.reyNegroUbicacion[1]
        if self.inCheck:
            if len(self.checks) == 1: # solo 1 jaque, para bloquear jaque o mover rey
                movs = self.getTodoPosiblesMov()
                # para bloquear un jaque debes mover una pieza a uno de los cuadrados entre la pieza enemiga y el rey
                check = self.checks[0] # verificar info
                checkFil = check[0]
                checkCol = check[1]
                chequeandoPieza = self.tablero[checkFil][checkCol] # pieza enemiga causando check
                casillasValidas = [] # casilla a la que se puede mover
                # si caballo, debe capturar caballo o mover rey, otra pieza puede ser bloqueada
                if chequeandoPieza[1] == 'C':
                    casillasValidas = [(checkFil, checkCol)]
                else:
                    for i in range(1, 8):
                        #check[2] y check[3] son las direcciones de verificación
                        casillaValida = (reyFil + check[2]*i, reyCol + check[3]*i)
                        casillasValidas.append(casillaValida)
                        #una vez que llegue al final de la pieza, verifique
                        if casillaValida[0] == checkFil and casillaValida[1] == checkCol:
                            break
                # deshazte de cualquier movimiento que no bloquee el jaque o mueva al rey
                for i in range(len(movs)-1,-1,-1): #vaya hacia atrás cuando esté eliminando de una lista mientras itera
                    if movs[i].piezaMovida[1] != 'R': #movs no mueve al rey, por lo que debe bloquear o capturar
                        if not(movs[i].filFinal, movs[i].colFinal) in casillasValidas: #movs no bloquea check o pieza capturada
                            movs.remove(movs[i])
            else: # check dos veces, el rey tiene que moverse
                self.getMovRey(reyFil, reyCol, movs)
        else: # no está bajo amenaza, por lo que todos los movimientos están bien
            movs = self.getTodoPosiblesMov()
        
        if len(movs) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.tablas_staleMate = True
        else:
            self.checkMate = False
            self.tablas_staleMate = False
        
        return movs
    
    """
    Todos los movimientos sin considerar checks
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
    ''' 
    obtenga todos los movimientos de cada pieza para las piezas ubicadas en
    fila, columna y agregue estos movimientos a la lista
    '''
    def getMovPeon(self, f, c, mov):
        piezaPinned = False
        direccionPin = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == f and self.pins[i][1] == c:
                piezaPinned = True
                direccionPin = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.muevenBlancas:
            cantMov = -1
            filInicial = 6
            filAtras = 0
            colorEnemigo = 'n'
        else:
            cantMov = 1
            filInicial = 1
            filAtras = 7
            colorEnemigo = 'b'
        promoPeon = False
        
        if self.tablero[f+cantMov][c] == '--': # mover 1 casilla
            if not piezaPinned or direccionPin == (cantMov,0):
                if f+cantMov == filAtras:
                    promoPeon = True
                mov.append(Movimiento((f, c), (f+cantMov, c), self.tablero, promocionPeon=promoPeon))
                if f == filInicial and self.tablero[f+2*cantMov][c] == '--': # mover 2 casillas
                    mov.append(Movimiento((f, c), (f+2*cantMov, c), self.tablero))
        #capturas
        if c-1 >= 0: # capturar por izquierda
            if not piezaPinned or direccionPin == (cantMov,-1):
                if self.tablero[f+cantMov][c-1][0] == colorEnemigo:
                    if f+cantMov == filAtras: #si la pieza llega al rango del banco entonces es una promoción de peón
                        promoPeon = True
                    mov.append(Movimiento((f, c), (f+cantMov, c-1), self.tablero, promocionPeon=promoPeon))
                if (f+cantMov, c-1) == self.posibleCaptAlPaso:
                    mov.append(Movimiento((f, c), (f+cantMov, c-1), self.tablero, alpaso=True))
        if c+1 <= 7: # capturar por derecha
            if not piezaPinned or direccionPin == (cantMov, 1):
                if self.tablero[f+cantMov][c+1][0] == colorEnemigo:
                    if f+cantMov == filAtras: #si la pieza llega al rango del banco entonces es una promoción de peón
                        promoPeon = True
                    mov.append(Movimiento((f, c), (f+cantMov, c+1), self.tablero, promocionPeon=promoPeon))
                if (f+cantMov, c+1) == self.posibleCaptAlPaso:
                    mov.append(Movimiento((f, c), (f+cantMov, c+1), self.tablero, alpaso=True))
    
    def getMovTorre(self, f, c, mov):
        piezaPinned = False
        direccionPin = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == f and self.pins[i][1] == c:
                piezaPinned = True
                direccionPin = (self.pins[i][2], self.pins[i][3])
                #no se puede quitar la dama de los movimientos de pin o torre, solo se quita en los movimientos de alfil
                if self.tablero[f][c][1] != 'D':
                    self.pins.remove(self.pins[i])
                break
        # visto desde el punto de las blancas
        direcciones = ((-1,0),(0,-1),(1,0),(0,1)) # up, left, down, right
        colorEnemigo = 'n' if self.muevenBlancas else 'b' # enemigos: negros, en otro caso: blancos
        for d in direcciones:
            for i in range(1,8):
                filFinal = f + d[0]*i
                colFinal = c + d[1]*i
                if 0 <= filFinal < 8 and 0 <= colFinal < 8: # en tablero
                    if not piezaPinned or direccionPin == d or direccionPin == (-d[0], -d[1]):
                        piezaFinal = self.tablero[filFinal][colFinal]
                        if piezaFinal == '--': # espacio vacio valido
                            mov.append(Movimiento((f,c),(filFinal,colFinal),self.tablero))
                        elif piezaFinal[0] == colorEnemigo:
                            mov.append(Movimiento((f,c),(filFinal,colFinal),self.tablero))
                            break
                        else: # pieza invalidada amigablemente
                            break
                else: # fuera del tablero
                    break
    
    def getMovCab(self, f, c, mov):
        piezaPinned = False
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == f and self.pins[i][1] == c:
                piezaPinned = True
                self.pins.remove(self.pins[i])
                break
        
        movCaballo = ((-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2))
        colorAliado = 'b' if self.muevenBlancas else 'n'
        for m in movCaballo:
            filFinal = f + m[0]
            colFinal = c + m[1]
            if 0 <= filFinal < 8 and 0 <= colFinal < 8:
                if not piezaPinned:
                    piezaFinal = self.tablero[filFinal][colFinal]
                    # verifica que no haya aliados (ocupada solo espacios vacios o enemigos)
                    if piezaFinal[0] != colorAliado:
                        mov.append(Movimiento((f,c),(filFinal,colFinal),self.tablero))
    
    def getMovAlfil(self, f, c, mov):
        piezaPinned = False
        direccionPin = ()
        for i in range(len(self.pins)-1, -1, -1):
            if self.pins[i][0] == f and self.pins[i][1] == c:
                piezaPinned = True
                direccionPin = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        direcciones = ((-1,-1),(-1,1),(1,-1),(1,1)) #4 diagonales
        colorEnemigo = 'n' if self.muevenBlancas else 'b' # enemigos: negros, en otro caso: blancos
        for d in direcciones:
            for i in range(1,8): # el alfil solo puede moverse un max de 7 casillas
                filFinal = f + d[0]*i
                colFinal = c + d[1]*i
                if 0 <= filFinal < 8 and  0 <= colFinal < 8: # en tablero
                    if not piezaPinned or direccionPin == d or direccionPin == (-d[0], -d[1]):
                        piezaFinal = self.tablero[filFinal][colFinal]
                        if piezaFinal == '--': # espacio vacio valido
                            mov.append(Movimiento((f,c),(filFinal,colFinal),self.tablero))
                        elif piezaFinal[0] == colorEnemigo:
                            mov.append(Movimiento((f,c),(filFinal,colFinal),self.tablero))
                            break
                        else: # pieza invalidada amigablemente
                            break
                else: # fuera del tablero
                    break
    
    def getMovDama(self, fil, col, mov):
        # combinamos los movimientos de las torres y alfiles
        self.getMovTorre(fil,col,mov)
        self.getMovAlfil(fil,col,mov)
    
    def getMovRey(self, f, c, movs):
        movsFil = (-1,-1,-1,0,0,1,1,1)
        movsCol = (-1,0,1,-1,1,-1,0,1)
        colorAliado = 'b' if self.muevenBlancas else 'n'
        for i in range(8):
            filFinal = f + movsFil[i]
            colFinal = c + movsCol[i]
            if 0 <= filFinal < 8 and 0 <= colFinal < 8:
                piezaFinal = self.tablero[filFinal][colFinal]
                if piezaFinal[0] != colorAliado:
                    # Coloque el rey en el cuadrado final y consulte los checks
                    if colorAliado == 'b':
                        self.reyBlancoUbicacion = (filFinal, colFinal)
                    else:
                        self.reyNegroUbicacion = (filFinal, colFinal)
                    inCheck, pins, checks = self.chequearPinsYChecks()
                    if not inCheck:
                        movs.append(Movimiento((f,c), (filFinal, colFinal), self.tablero))
                    # Coloque el rey de vuelta en la ubicación original
                    if colorAliado == 'b':
                        self.reyBlancoUbicacion = (f, c)
                    else:
                        self.reyNegroUbicacion = (f, c)
        self.getMovEnroque(f, c, movs, colorAliado)
    '''
    Genere movimientos de castillo para el rey en (f, c) y agréguelos a la lista de movimientos
    '''
    def getMovEnroque(self, f, c, movs, colorAliado):
        inCheck = self.sqBajoAtaque(f, c, colorAliado)
        if inCheck:
            #print('oof')
            return #no se puede enrocar en jaque
        #no se puede enrocar si se rinde correctamente
        if (self.muevenBlancas and self.actualDerechoEnrocar.ebr) or (not self.muevenBlancas and self.actualDerechoEnrocar.enr):
            self.getMovEnroqueReyside(f, c, movs, colorAliado)
        if (self.muevenBlancas and self.actualDerechoEnrocar.ebd) or (not self.muevenBlancas and self.actualDerechoEnrocar.end):
            self.getMovEnroqueDamaside(f, c, movs, colorAliado)
    '''
    Genere movimientos de enroque en el flanco de rey para el rey en (f,c). Este método solo 
    se activará si el jugador todavía tiene derechos de castillo en el flanco de rey.
    '''
    def getMovEnroqueReyside(self, f, c, movs, colorAliado):
        #comprueba si dos casillas entre el rey y la torre están despejadas y no están bajo ataque
        if self.tablero[f][c+1] == '--' and self.tablero[f][c+2] == '--' and \
            not self.sqBajoAtaque(f, c+1, colorAliado) and not self.sqBajoAtaque(f, c+2, colorAliado):
                movs.append(Movimiento((f,c),(f,c+2), self.tablero, enroque=True))
    '''
    Genere movimientos de enroque en el flanco de dama para el rey en (f,c). Este método solo
    se activará si el jugador todavía tiene derechos de castillo en el flanco de dama.
    '''
    def getMovEnroqueDamaside(self, f, c, movs, colorAliado):
        #comprueba si dos casillas entre el rey y la torre están despejadas y no están bajo ataque
        if self.tablero[f][c-1] == '--' and self.tablero[f][c-2] == '--' and self.tablero[f][c-3] == '--' and \
            not self.sqBajoAtaque(f, c-1, colorAliado) and not self.sqBajoAtaque(f, c-2, colorAliado):
                movs.append(Movimiento((f,c),(f,c-2), self.tablero, enroque=True))
    
    '''
    Returns si la plaza está bajo ataque
    '''
    def sqBajoAtaque(self, f, c, colorAliado):
        # verifica (check) fuera de la casilla
        colorEnemigo = 'b' if colorAliado == 'n' else 'n'
        direcciones = ((-1, 0),(0, -1),(1, 0),(0, 1),(-1,-1),(-1, 1),(1,-1),(1, 1))
        for j in range(len(direcciones)):
            d = direcciones[j]
            posiblePin = () # restablecer posibles pins
            for i in range(1, 8):
                filFinal = f + d[0]*i
                colFinal = c + d[1]*i
                if 0 <= filFinal < 8 and 0 <= colFinal < 8:
                    piezaFinal = self.tablero[filFinal][colFinal]
                    if piezaFinal[0] == colorAliado: # ningún ataque desde esa dirección
                        break
                    elif piezaFinal[0] == colorEnemigo:
                        tipo = piezaFinal[1]
                        # 5 posibilidades aquí en este complejo condicional
                        #1.) ortogonalmente lejos del rey y la pieza es una torre
                        #2.) Diagonalmente lejos del rey y la pieza es un alfil
                        #3.) A 1 cuadrado de distancia en diagonal del rey y es pieza es un peón
                        #4.) Cualquier dirección y pieza es una reina
                        #5.) Cualquier dirección a 1 cuadrado de distancia y pieza es un rey (esto es
                        # necesario para evitar que un rey se mueva a un cuadrado controlado por otro rey)
                        if (0 <= j <= 3 and tipo == 'T') or \
                            (4 <= j <= 7 and tipo == 'A') or \
                            (i == 1 and tipo == 'P' and (
                                (colorEnemigo == 'b' and 6 <= j <= 7) or (colorEnemigo == 'n' and 4 <= j <= 5))) or \
                            (tipo == 'D') or (i == 1 and tipo == 'R'):
                                return True
                        else: # pieza enemiga que no aplica check:
                            break
                else:
                    break # fuera de tablero
        # Verificar los check del caballo
        movsCaballo = ((-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2))
        for m in movsCaballo:
            filFinal = f + m[0]
            colFinal = c + m[1]
            if 0 <= filFinal < 8 and 0 <= colFinal < 8:
                piezaFinal = self.tablero[filFinal][colFinal]
                if piezaFinal[0] == colorEnemigo and piezaFinal == 'C': # caballo enemigo atacando al rey
                    return True
        return False
    
    '''
    Return si el jugador está en jaque, una lista de pines y una lista de jaque (check list)
    '''
    def chequearPinsYChecks(self):
        pins = [] #casilla donde está la pieza fijada aliada y la dirección fijada desde
        checks = [] #casilla donde el enemigo está aplicando check
        inCheck = False
        if self.muevenBlancas:
            colorEnemigo = 'n'
            colorAliado = 'b'
            filInicial = self.reyBlancoUbicacion[0]
            colInicial = self.reyBlancoUbicacion[1]
        else:
            colorEnemigo = 'b'
            colorAliado = 'n'
            filInicial = self.reyNegroUbicacion[0]
            colInicial = self.reyNegroUbicacion[1]
        #Consulte Outward desde King para pins y checks, realice un seguimiento de los pins
        direcciones = ((-1, 0),(0, -1),(1, 0),(0, 1),(-1,-1),(-1, 1),(1,-1),(1, 1))
        for j in range(len(direcciones)):
            d = direcciones[j]
            posiblePin = () # restablecer posibles pins
            for i in range(1, 8):
                filFinal = filInicial + d[0]*i
                colFinal = colInicial + d[1]*i
                if 0 <= filFinal < 8 and 0 <= colFinal < 8:
                    piezaFinal = self.tablero[filFinal][colFinal]
                    if piezaFinal[0] == colorAliado and piezaFinal[1] != 'R':
                        if posiblePin == (): # La primera pieza aliada podría ser pinned
                            posiblePin = (filFinal, colFinal, d[0], d[1])
                        else: #Segunda pieza aliada, por lo que no hay PIN o check posible en esta dirección
                            break
                    elif piezaFinal[0] == colorEnemigo:
                        tipo = piezaFinal[1]
                        # 5 posibilidades aquí en este complejo condicional
                        #1.) ortogonalmente lejos del rey y la pieza es una torre
                        #2.) Diagonalmente lejos del rey y la pieza es un alfil
                        #3.) A 1 cuadrado de distancia en diagonal del rey y es pieza es un peón
                        #4.) Cualquier dirección y pieza es una reina
                        #5.) Cualquier dirección a 1 cuadrado de distancia y pieza es un rey (esto es
                        # necesario para evitar que un rey se mueva a un cuadrado controlado por otro rey)
                        if (0 <= j <= 3 and tipo == 'T') or \
                            (4 <= j <= 7 and tipo == 'A') or \
                            (i == 1 and tipo == 'P' and ((colorEnemigo == 'b' and 6 <= j <= 7) or (colorEnemigo == 'n' and 4 <= j <= 5))) or \
                            (tipo == 'D') or (i == 1 and tipo == 'R'):
                                if posiblePin == (): # Sin bloqueo de piezas, así que verifique
                                    inCheck = True
                                    checks.append((filFinal, colFinal, d[0], d[1]))
                                    break
                                else: # Bloqueo de piezas para pin
                                    pins.append(posiblePin)
                                    break
                        else: # pieza enemiga que no aplica check:
                            break
                else:
                    break # fuera de tablero
        # Verificar los check del caballo
        movsCaballo = ((-2,-1),(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2))
        for m in movsCaballo:
            filFinal = filInicial + m[0]
            colFinal = colInicial + m[1]
            if 0 <= filFinal < 8 and 0 <= colFinal < 8:
                piezaFinal = self.tablero[filFinal] [colFinal]
                if piezaFinal[0] == colorEnemigo and piezaFinal == 'C': # caballo enemigo atacando al rey
                    inCheck = True
                    checks.append((filFinal, colFinal, m[0],  m[1]))
        return inCheck, pins, checks

    def actualizarDerechosEnroque(self, movs):
        if movs.piezaMovida == 'bR':
            self.actualDerechoEnrocar.ebr = False
            self.actualDerechoEnrocar.ebd = False
        elif movs.piezaMovida == 'nR':
            self.actualDerechoEnrocar.enr = False
            self.actualDerechoEnrocar.end = False
        elif movs.piezaMovida == 'bT':
            if movs.filInicial == 7:
                if movs.colInicial == 0: # torre izq
                    self.actualDerechoEnrocar.ebd = False
                elif movs.colInicial == 7: # torre der
                    self.actualDerechoEnrocar.ebr = False
        elif movs.piezaMovida == 'nT':
            if movs.filInicial == 0:
                if movs.colInicial == 0: # torre izq
                    self.actualDerechoEnrocar.end = False
                elif movs.colInicial == 7: # torre der
                    self.actualDerechoEnrocar.enr = False

class DerechosEnroque():
    def __init__(self, ebr, enr, ebd, end):
        self.ebr = ebr #enroque blanco lado rey
        self.enr = enr #enroque negro lado rey
        self.ebd = ebd #enroque blanco lado dama
        self.end = end #enroque negro lado dama

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
    
    def __init__(self, inicialSq, finalSq, board, alpaso=False, promocionPeon=False, enroque=False): # Sq: square
        self.filInicial = inicialSq[0] # clic de fila  inicial
        self.colInicial = inicialSq[1] # clic de columna inicial
        self.filFinal = finalSq[0] # clic de fila final
        self.colFinal = finalSq[1] # clic de columna final
        self.piezaMovida = board[self.filInicial][self.colInicial]
        self.piezaCapturada = board[self.filFinal][self.colFinal]
        self.alPaso = alpaso
        self.promocionPeon = promocionPeon
        self.enroque = enroque
        if alpaso:
            self.piezaCapturada = 'nP' if self.piezaMovida == 'bP' else 'bP' # de paso captura peones de colores opuestos
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
