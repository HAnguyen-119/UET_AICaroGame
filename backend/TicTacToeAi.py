import copy
import random
import math
import numpy as np
from Zobrist import Zobrist

class BoardInfo:
    xTurn = False
    zobrist = Zobrist(15)
    boardStates = {}
    rowStates = {}
    colStates = {}
    firstDiagStates = {}
    secondDiagStates = {}


fourX = [' xxxx', 'x xxx', 'xx xx', 'xxx x', 'xxxx ']
fourO = [' oooo', 'o ooo', 'oo oo', 'ooo o', 'oooo ']

threeX = ['  xxx  ', 'o xxx  ', '  xxx o']
threeO = ['  ooo  ', 'x ooo  ', '  ooo x']

brokenThreeX = [' x xx ', ' xx x ']
brokenThreeO = [' o oo ', ' oo o ']

def get_move(board, size):
    # Find all available positions on the board
    size = int(size)
    if isEmpty(board, size) or (countX(board, size) == 1 and countO(board, size) == 0): BoardInfo.zobrist = Zobrist(size)

    if isEmpty(board, size):
        return (size // 2, size // 2)

    nextMove = (-1, -1)
    isMaximizing = isXTurn(board, size)
    moves = emptyAndHasAdjacent(board, size)

    if isMaximizing:
        bestMoveValue = -math.inf
        for (i, j) in moves: 
            board[i][j] = 'x'
            bestValue = minimax(board, size, 0, False, -math.inf, math.inf)
            board[i][j] = ' '
            if bestValue >= bestMoveValue: 
                nextMove = (i, j)
                bestMoveValue = bestValue
    else:
        bestMoveValue = math.inf
        for (i, j) in moves: 
            board[i][j] = 'o'
            bestValue = minimax(board, size, 0, True, -math.inf, math.inf)
            board[i][j] = ' '
            if bestValue <= bestMoveValue: 
                nextMove = (i, j)
                bestMoveValue = bestValue      
    return nextMove

def countX(board, size):
    x = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] == 'x': x += 1
    return x

def countO(board, size):
    o = 0
    for i in range(size):
        for j in range(size):
            if board[i][j] == 'o': o += 1
    return o
   
def isXTurn(board, size):
    return countX(board, size) == countO(board, size)        

def evaluate(board, size):
    res = 0

    for i in range(size):
        h = BoardInfo.zobrist.hashRow(board, size, i)
        if h in BoardInfo.rowStates: res += BoardInfo.rowStates[h]
        else:
            x = 0
            o = 0
            for j in range(size - 4):

                if ''.join(board[i][j:j+5]) == 'xxxxx': x += 1000000
                elif ''.join(board[i][j:j+5]) == 'ooooo': o += 1000000

                if j < size - 5 and  ''.join(board[i][j:j+6]) == ' xxxx ': x += 500
                elif j < size - 5 and ''.join(board[i][j:j+6]) == ' oooo ': o += 500

                if ''.join(board[i][j:j+5]) in fourX: x += 50
                elif ''.join(board[i][j:j+5]) in fourO: o += 50

                if j < size - 6 and ''.join(board[i][j:j+7]) in threeX: x += 30
                elif j < size - 6 and ''.join(board[i][j:j+7]) in threeO: o += 30

                if j < size - 5 and ''.join(board[i][j:j+6]) in brokenThreeX: x += 20
                elif j < size - 5 and ''.join(board[i][j:j+6]) in brokenThreeO: o += 20

            BoardInfo.rowStates[h] = x - o
            res += x - o

    # Check columns
    for i in range(size):
        h = BoardInfo.zobrist.hashCol(board, size, i)
        if h in BoardInfo.colStates: res += BoardInfo.colStates[h]
        else:
            x = 0
            o = 0
            for j in range(size - 4):
                
                if board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] == 'xxxxx': return 1000000
                elif board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] == 'ooooo': return -1000000

                if j < size - 5 and board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] == ' xxxx ': x += 500
                elif j < size - 5 and board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] == ' oooo ': o += 500

                if board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] in fourX: x += 50
                elif board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] in fourO: o += 50

                if j < size - 6 and board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] + board[j + 6][i] in threeX: x += 30
                elif j < size - 6 and board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] + board[j + 6][i] in threeO: o += 30

                if j < size - 5 and board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] in brokenThreeX: x += 20
                elif j < size - 5 and board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] in brokenThreeO: o += 20

            BoardInfo.colStates[h] = x - o
            res += x - o

    # Check diagonals
    for i in range(size - 4):
        for j in range(size - 4):
            h = BoardInfo.zobrist.hashFirstDiag(board, size, i, j)
            if h in BoardInfo.firstDiagStates: res += BoardInfo.firstDiagStates[h]
            else:
                x = 0
                o = 0

                if ''.join(board[i+k][j+k] for k in range(5)) == 'xxxxx': return 1000000
                elif ''.join(board[i+k][j+k] for k in range(5)) == 'ooooo': return -1000000

                if i < size - 5 and j < size - 5 and ''.join(board[i+k][j+k] for k in range(6)) == ' xxxx ': x += 500
                elif i < size - 5 and j < size - 5 and ''.join(board[i+k][j+k] for k in range(6)) == ' oooo ': o += 500

                if ''.join(board[i+k][j+k] for k in range(5)) in fourX: x += 50
                elif ''.join(board[i+k][j+k] for k in range(5)) in fourO: o += 50

                if i < size - 6 and j < size - 6 and ''.join(board[i+k][j+k] for k in range(7)) in threeX: x += 30
                elif i < size - 6 and j < size - 6 and ''.join(board[i+k][j+k] for k in range(7)) in threeO: o += 30
        
                if i < size - 5 and j < size - 5 and ''.join(board[i+k][j+k] for k in range(6)) in brokenThreeX: x += 20
                elif i < size - 5 and j < size - 5 and ''.join(board[i+k][j+k] for k in range(6)) in brokenThreeO: o += 20

                BoardInfo.firstDiagStates[h] = x - o
                res += x - o
    
    for i in range(size - 4):
        for j in range(4, size):
            h = BoardInfo.zobrist.hashSecondDiag(board, size, i, j)
            if h in BoardInfo.secondDiagStates: res += BoardInfo.secondDiagStates[h]
            else:
                x = 0
                o = 0
                if ''.join(board[i+k][j-k] for k in range(5)) == 'xxxxx': return 1000000
                elif ''.join(board[i+k][j-k] for k in range(5)) == 'ooooo': return -1000000
                
                if i < size - 5 and j >= 5 and ''.join(board[i+k][j-k] for k in range(6)) == ' xxxx ': x += 500
                elif i < size - 5 and j >= 5 and ''.join(board[i+k][j-k] for k in range(6)) == ' oooo ': o += 500

                if ''.join(board[i+k][j-k] for k in range(5)) in fourX: x += 50
                elif ''.join(board[i+k][j-k] for k in range(5)) in fourO: o += 50

                if i < size - 6 and j >= 6 and ''.join(board[i+k][j-k] for k in range(7)) in threeX: x += 30
                elif i < size - 6 and j >= 6 and ''.join(board[i+k][j-k] for k in range(7)) in threeO: o += 30

                if i < size - 5 and j >= 5 and ''.join(board[i+k][j-k] for k in range(6)) in brokenThreeX: x += 20
                elif i < size - 5 and j >= 5 and ''.join(board[i+k][j-k] for k in range(6)) in brokenThreeO: o += 20

                BoardInfo.firstDiagStates[h] = x - o
                res += x - o

    return res

'''
def evaluate(board, size):

    res = checkWin(board, size)
    if res != 0: return res
    
    sf = countStraightFour(board, size)
    f = countFour(board, size)
    t = countThree(board, size)
    bt = countBrokenThree(board, size)

    return 20 * (bt[0] - bt[1]) + 30 * (t[0] - t[1]) + 50 * (f[0] - f[1]) + 500 * (sf[0] - sf[1])
'''
'''
def checkWin(board, size):
    if countX(board, size) < 5: return 0

    # Check rows
    for i in range(size):
        for j in range(size - 4):
            if board[i][j] == ' ' or board[i][j] != board[i][j + 1]: continue
            if ''.join(board[i][j:j+5]) == 'xxxxx': return 1000000
            elif ''.join(board[i][j:j+5]) == 'ooooo': return -1000000

    # Check columns
    for i in range(size):
        for j in range(size - 4):
            if board[j][i] == ' ' or board[j][i] != board[j + 1][i]: continue
            if board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] == 'xxxxx': return 1000000
            elif board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] == 'ooooo': return -1000000

    # Check diagonals
    for i in range(size - 4):
        for j in range(size - 4):
            if board[i][j] == ' ' or board[i][j] != board[i + 1][j + 1]: continue
            if ''.join(board[i+k][j+k] for k in range(5)) == 'xxxxx': return 1000000
            elif ''.join(board[i+k][j+k] for k in range(5)) == 'ooooo': return -1000000
    
    for i in range(size - 4):
        for j in range(4, size):
            if board[i][j] == ' ' or board[i][j] != board[i + 1][j - 1]: continue
            if ''.join(board[i+k][j-k] for k in range(5)) == 'xxxxx': return 1000000
            elif ''.join(board[i+k][j-k] for k in range(5)) == 'ooooo': return -1000000
            
    return 0

def countStraightFour(board, size):
    
    res = [0, 0]
    # Check rows
    for i in range(size):
        h = BoardInfo.zobrist.hashRow(board, size, i)
        if h in BoardInfo.rowStates: 
            res[0] += BoardInfo.rowStates[h][0]
            res[1] += BoardInfo.rowStates[h][1]
        else:
            x = 0
            o = 0
            for j in range(size - 5):
                if ''.join(board[i][j:j+6]) == ' xxxx ': 
                    res[0] += 1
                    x = 1
                elif ''.join(board[i][j:j+6]) == ' oooo ': 
                    res[1] += 1
                    o = 1
            BoardInfo.rowStates[h] = (x, o)

    # Check columns
    for i in range(size):
        for j in range(size - 5):
            if board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] == ' xxxx ': res[0] += 1
            elif board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] == ' oooo ': res[1] += 1

    # Check diagonals
    for i in range(size - 5):
        for j in range(size - 5):
            if ''.join(board[i+k][j+k] for k in range(6)) == ' xxxx ': res[0] += 1
            elif ''.join(board[i+k][j+k] for k in range(6)) == ' oooo ': res[1] += 1
    
    for i in range(size - 5):
        for j in range(5, size):
            if ''.join(board[i+k][j-k] for k in range(6)) == ' xxxx ': res[0] += 1
            elif ''.join(board[i+k][j-k] for k in range(6)) == ' oooo ': res[1] += 1
    return res

def countFour(board, size):
    res = [0, 0]
    # Check rows
    for i in range(size):
        for j in range(size - 4):
            if ''.join(board[i][j:j+5]) in fourX: res[0] += 1
            elif ''.join(board[i][j:j+5]) in fourO: res[1] += 1

    # Check columns
    for i in range(size):
        for j in range(size - 4):
            if board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] in fourX: res[0] += 1
            elif board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] in fourO: res[1] += 1

    # Check diagonals
    for i in range(size - 4):
        for j in range(size - 4):
            if ''.join(board[i+k][j+k] for k in range(5)) in fourX: res[0] += 1
            elif ''.join(board[i+k][j+k] for k in range(5)) in fourO: res[1] += 1 
    
    for i in range(size - 4):
        for j in range(4, size):
            if ''.join(board[i+k][j-k] for k in range(5)) in fourX: res[0] += 1
            elif ''.join(board[i+k][j-k] for k in range(5)) in fourO: res[1] += 1 
    return res

def countThree(board, size):
    res = [0, 0]
    # Check rows
    for i in range(size):
        for j in range(size - 6):
            if ''.join(board[i][j:j+7]) in threeX: res[0] += 1
            elif ''.join(board[i][j:j+7]) in threeO: res[1] += 1

    # Check columns
    for i in range(size):
        for j in range(size - 6):
            if board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] + board[j + 6][i] in threeX: res[0] += 1
            elif board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] + board[j + 6][i] in threeO: res[1] += 1

    # Check diagonals
    for i in range(size - 6):
        for j in range(size - 6):
            if ''.join(board[i+k][j+k] for k in range(7)) in threeX: res[0] += 1
            elif ''.join(board[i+k][j+k] for k in range(7)) in threeO: res[1] += 1 
    
    for i in range(size - 6):
        for j in range(6, size):
            if ''.join(board[i+k][j-k] for k in range(7)) in threeX: res[0] += 1
            elif ''.join(board[i+k][j-k] for k in range(7)) in threeO: res[1] += 1 
    return res

def countBrokenThree(board, size):
    res = [0, 0]
    # Check rows
    for i in range(size):
        for j in range(size - 5):
            if ''.join(board[i][j:j+6]) in brokenThreeX: res[0] += 1
            elif ''.join(board[i][j:j+6]) in brokenThreeO: res[1] += 1

    # Check columns
    for i in range(size):
        for j in range(size - 5):
            if board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] in brokenThreeX: res[0] += 1
            elif board[j][i] + board[j + 1][i] + board[j + 2][i] + board[j + 3][i] + board[j + 4][i] + board[j + 5][i] in brokenThreeO: res[1] += 1

    # Check diagonals
    for i in range(size - 5):
        for j in range(size - 5):
            if ''.join(board[i+k][j+k] for k in range(6)) in brokenThreeX: res[0] += 1
            elif ''.join(board[i+k][j+k] for k in range(6)) in brokenThreeO: res[1] += 1 
    
    for i in range(size - 5):
        for j in range(5, size):
            if ''.join(board[i+k][j-k] for k in range(6)) in brokenThreeX: res[0] += 1
            elif ''.join(board[i+k][j-k] for k in range(6)) in brokenThreeO: res[1] += 1 
    return res
'''


def minimax(board, size, depth, isMaximizing, alpha, beta):
    score = evaluate(board, size)
    if depth == min(countX(board, size), 3): 
        return score
    if score == 1000000:
        return 1000000 - depth
    elif score == -1000000:
        return -1000000 + depth
    #lastMove = BoardInfo.lastMoves[-1]
    
    h = BoardInfo.zobrist.hash(board, size)
    if h in BoardInfo.boardStates: return BoardInfo.boardStates[h]

    moves = emptyAndHasAdjacent(board, size)
    if isMaximizing:
        bestValue = -math.inf
        for (i, j) in moves: 
            board[i][j] = 'x'
            bestValue = max(bestValue, minimax(board, size, depth + 1, False, alpha, beta))
            alpha = max(alpha, bestValue)
            board[i][j] = ' '
            if alpha >= beta:
                break
    else:
        bestValue = math.inf
        for (i, j) in moves: 
            board[i][j] = 'o'
            bestValue = min(bestValue, minimax(board, size, depth + 1, True, alpha, beta))
            beta = min(beta, bestValue)
            board[i][j] = ' '
            if alpha >= beta:
                break
    BoardInfo.boardStates[h] = bestValue
    return bestValue

def emptyAndHasAdjacent(board, size):
    res = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for i in range(size):
        for j in range(size):
            if board[i][j] != ' ': continue
            for dr, dc in directions:
                r, c = i + dr, j + dc
                if 0 <= r < size and 0 <= c < size:
                    if board[r][c] in ['x', 'o']:
                        res.append((i, j))
    return res

def isEmpty(board, size):
    for i in range(size):
        for j in range(size):
            if board[i][j] != ' ': return False
    return True

def isFull(board, size):
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ': return False
    return True


'''
board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', 'o', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
#print(evaluate(board, 15))
#print(get_move(board, 15))
print(BoardInfo.zobrist.hash(board, 15))
'''
'''
board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
'''
'''
board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]

#print(emptyAndHasAdjacent(board, 15))

def printBoard(board, size):
    for i in range(size):
        print(board[i])
printBoard(board, 8)
while (not isFull(board, 8)):
    
    a = int(input())
    b = int(input())
    board[a][b] = 'x'
    

    #move = get_move(board, 8)
    #print(move)
    #board[move[0]][move[1]] = 'x'

    move1 = get_move(board, 8)
    print(move1)
    board[move1[0]][move1[1]] = 'o'
    
    #print(BoardInfo.lastMoves)
    printBoard(board, 8)
    if (evaluate(board, 8) == 1000000): 
        print('x win')
        break
    elif (evaluate(board, 8) == -1000000): 
        print('o win')
        break
if isFull(board, 8) :print("draw")
#print(get_move(board, 5))    
'''

