"""
This class is responsible for storing all the information about de current state of a chess game. It will also be
responsible for determining the valid moves at the current  state. It will also keep a move log.
"""
class GameState():
    def __init__(self):
        #tablero de 8x8.
        #La primera letra representa si la pieza es negra o blanca, 'n' o 'b', respectivamente.
        #'--' representa espacios blancos, vacios.
        self.board = [
            ['nT','nC','nA','nD','nR','nA','nC','nT'],
            ['nP','nP','nP','nP','nP','nP','nP','nP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['bT','bC','bA','bD','bR','bA','bC','bT']]
        self.whiteToMove = True
        self.moveLog = []
        
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #log the move so we undo ir later
        self.whiteToMove = not self.whiteToMove #swap players

class Move():
    # map keys values
    # key : value
    ranksToRow = {
        '1':7,'2':6,'3':5,'4':4,
        '5':3,'6':2,'7':1,'8':0}
    rowToRanks = {v:k for k,v in ranksToRow.items()}
    filesToCols = {
        'a':0,'b':1,'c':2,'d':3,
        'e':4,'f':5,'g':6,'h':7
        }
    colsToFiles = {v:k for k,v in filesToCols.items()}
    
    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
    
    def getChessNotation(self):
        # you can add to make this like real chess notation
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)
    
    def getRankFile(self,c,r):
        return self.colsToFiles[c] + self.rowToRanks[r]
    