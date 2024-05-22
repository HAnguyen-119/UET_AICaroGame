import copy
import random
import math

def get_move(board, size):
    # Find all available positions on the board
    size = int(size)
    '''
    available_moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                available_moves.append((i, j))

    # If there are no available moves, return None
    if not available_moves:
        return None
    '''
    nextMove = (-1, -1)
    isMaximizing = isXTurn(board, size)
    if isMaximizing:
        bestMoveValue = -math.inf
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ':
                    board[i][j] = 'x'
                    bestValue = minimax(board, size, 0, False, -math.inf, math.inf)
                    board[i][j] = ' '
                    if bestValue >= bestMoveValue: 
                        nextMove = (i, j)
                        bestMoveValue = bestValue
    else:
        bestMoveValue = math.inf
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ':
                    board[i][j] = 'o'
                    bestValue = minimax(board, size, 0, True, -math.inf, math.inf)
                    board[i][j] = ' '
                    if bestValue <= bestMoveValue: 
                        nextMove = (i, j)
                        bestMoveValue = bestValue         
    return nextMove

def isXTurn(board, size):
    x, o = 0, 0
    for i in range(size):
        for j in range(size):
            if board[i][j] == 'x': x += 1
            elif board[i][j] == 'o': o += 1
    return x == o            
    
def evaluate(board, size):
    # Check rows
    for i in range(size):
        for k in range(size - 5):
            if all(board[i][j] == 'x' for j in range(k, k + 5)): return 10
            if all(board[i][j] == 'o' for j in range(k, k + 5)): return -10
    # Check columns
    for i in range(size):
        for k in range(size - 5):
            if all(board[j][i] == 'x' for j in range(k, k + 5)): return 10
            if all(board[j][i] == 'o' for j in range(k, k + 5)): return -10
    # Check diagonals
    #for k in range(size - 5):
    #    if all(board[i][i] == 'x' for i in range(k, k + 5)) or all(board[size - 1 - i][i] == 'x' for i in range(k, k + 5)): return 10
    #   if all(board[i][i] == 'o' for i in range(k, k + 5)) or all(board[size - 1 - i][i] == 'o' for i in range(k, k + 5)): return -10
    for j in range(size - 4):
        for k in range(size - j - 4):
            if all(board[i][i + j] == 'x' for i in range(k, k + 5)) or all(board[i + j][i] == 'x' for i in range(k, k + 5)): return 10
            if all(board[i][i + j] == 'o' for i in range(k, k + 5)) or all(board[i + j][i] == 'o' for i in range(k, k + 5)): return -10

    for j in range(size - 4):
        for k in range(size - j - 4):
            if all(board[i][size - 1 - i - j] == 'x' for i in range(k, k + 5)) or all(board[i + j][size - 1 - i] == 'x' for i in range(k, k + 5)): return 10
            if all(board[i][size - 1 - i - j] == 'o' for i in range(k, k + 5)) or all(board[i + j][size - 1 - i] == 'o' for i in range(k, k + 5)): return -10
    return 0

def minimax(board, size, depth, isMaximizing, alpha, beta):
    score = evaluate(board, size)
    if depth == size: 
        return score
    if score == 10:
        return 10 - depth
    elif score == -10:
        return -10 + depth
    if isMaximizing:
        bestValue = -math.inf
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ': 
                    board[i][j] = 'x'
                    bestValue = max(bestValue, minimax(board, size, depth + 1, False, alpha, beta))
                    alpha = max(alpha, bestValue)
                    board[i][j] = ' '
                    if alpha >= beta:
                        break
        return bestValue
    else:
        bestValue = math.inf
        for i in range(size):
            for j in range(size):
                if board[i][j] == ' ': 
                    board[i][j] = 'o'
                    bestValue = min(bestValue, minimax(board, size, depth + 1, True, alpha, beta))
                    beta = min(beta, bestValue)
                    board[i][j] = ' '
                    if alpha >= beta:
                        break
        return bestValue

'''
board = [['x', 'o', ' '],
         [' ', 'o', ' '],
         [' ', ' ', 'x']]
board = [['o', 'o', 'o', 'o', 'x'],
         ['o', 'o', 'o', 'x', 'x'],
         ['x', 'o', 'x', 'x', 'x'],
         ['o', 'x', 'x', 'x', 'x'],
         ['o', 'x', 'o', 'x', 'o']]
'''
board = [[' ', 'x', ' ', ' ', ' ', ' ', ' '],
         [' ', 'o', 'x', ' ', ' ', ' ', ' '],
         ['x', ' ', 'o', 'x', ' ', ' ', 'o'],
         [' ', 'x', ' ', 'o', 'x', 'o', ' '],
         [' ', ' ', 'x', ' ', 'o', ' ', ' '],
         [' ', ' ', ' ', 'o', ' ', ' ', ' '],
         [' ', ' ', 'o', ' ', 'x', ' ', ' ']]
#print(evaluate(board, 7))
#print(get_move(board, 5))    

