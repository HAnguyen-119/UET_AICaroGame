import random

class Zobrist: 

    def __init__(self, size):
        self.zobristTable = [[[self.randomInt() for k in range(2)] for j in range(size)] for i in range(size)]

    def randomInt(self):
        min = 0
        max = pow(2, 64)
        return random.randint(min, max)
   
    def indexOf(self, piece):
        return 0 if piece == 'x' else 1

    def hash(self, board, size):
        h = 0
        for i in range(size):
            for j in range(size):
                if board[i][j] != ' ':
                    piece = self.indexOf(board[i][j])
                    h ^= self.zobristTable[i][j][piece]
        return h
    
    def hashRow(self, board, size, row):
        h = 0
        for j in range(size):
            if board[row][j] != ' ':
                piece = self.indexOf(board[row][j])
                h ^= self.zobristTable[row][j][piece]
        return h

    def hashCol(self, board, size, col):
        h = 0
        for i in range(size):
            if board[i][col] != ' ':
                piece = self.indexOf(board[i][col])
                h ^= self.zobristTable[i][col][piece]
        return h
    
    def hashFirstDiag(self, board, size, row, col):
        h = 0
        while row > 0 and col > 0:
            row -= 1
            col -= 1
        while row < size and col < size:
            piece = self.indexOf(board[row][col])
            h ^= self.zobristTable[row][col][piece]
            row += 1
            col += 1
        return h
        
    def hashSecondDiag(self, board, size, row, col):
        h = 0
        while row > 0 and col < size - 1:
            row -= 1
            col += 1
        while row < size and col > 0:
            piece = self.indexOf(board[row][col])
            h ^= self.zobristTable[row][col][piece]
            row += 1
            col -= 1
        return h