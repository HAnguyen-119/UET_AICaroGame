import copy
import random
import math
import numpy as np

def get_move(board, size):
    # Find all available positions on the board
    size = int(size)

    if isEmpty(board, size):
        return (size // 2, size // 2)

    nextMove = (-1, -1)
    isMaximizing = isXTurn(board, size)
    
    if isMaximizing:
        bestMoveValue = -1000
        for i in range(size):
            for j in range(size):
                if isEmptyAndHasAdjacent(board, size, i, j):
                    board[i][j] = 'x'
                    bestValue = minimax(board, size, 0, False, -1000, 1000)
                    board[i][j] = ' '
                    if bestValue > bestMoveValue: 
                        nextMove = (i, j)
                        bestMoveValue = bestValue
    else:
        bestMoveValue = 1000
        for i in range(size):
            for j in range(size):
                if isEmptyAndHasAdjacent(board, size, i, j):
                    board[i][j] = 'o'
                    bestValue = minimax(board, size, 0, True, -1000, 1000)
                    board[i][j] = ' '
                    if bestValue < bestMoveValue: 
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
    if countX(board, size) < 5: return 0

    # Check rows
    for i in range(size):
        for j in range(size - 4):
            if board[i][j] != board[i][j + 1]: continue
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][j + 4]:
                if board[i][j] == 'x': return 10
                elif board[i][j] == 'o': return -10

    # Check columns
    for i in range(size):
        for j in range(size - 4):
            if board[j][i] != board[j + 1][i]: continue
            if board[j][i] == board[j + 1][i] == board[j + 2][i] == board[j + 3][i] == board[j + 4][i]:
                if board[j][i] == 'x': return 10
                elif board[j][i] == 'o': return -10

    # Check diagonals
    for i in range(size - 4):
        for j in range(size - 4):
            if board[i][j] != board[i + 1][j + 1]: continue
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == board[i + 4][j + 4]:
                if board[i][j] == 'x': return 10
                elif board[i][j] == 'o': return -10
    
    for i in range(size - 4):
        for j in range(4, size):
            if board[i][j] != board[i + 1][j - 1]: continue
            if board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == board[i + 4][j - 4]:
                if board[i][j] == 'x': return 10
                elif board[i][j] == 'o': return -10
            
    return 0

def minimax(board, size, depth, isMaximizing, alpha, beta):
    score = evaluate(board, size)
    if depth == min(countX(board, size), 3): 
        return score
    if score == 10:
        return 10 - depth
    elif score == -10:
        return -10 + depth
    if isMaximizing:
        bestValue = -1000
        for i in range(size):
            for j in range(size):
                if isEmptyAndHasAdjacent(board, size, i, j): 
                    board[i][j] = 'x'
                    bestValue = max(bestValue, minimax(board, size, depth + 1, False, alpha, beta))
                    alpha = max(alpha, bestValue)
                    board[i][j] = ' '
                    if alpha >= beta:
                        break
        return bestValue
    else:
        bestValue = 1000
        for i in range(size):
            for j in range(size):
                if isEmptyAndHasAdjacent(board, size, i, j): 
                    board[i][j] = 'o'
                    bestValue = min(bestValue, minimax(board, size, depth + 1, True, alpha, beta))
                    beta = min(beta, bestValue)
                    board[i][j] = ' '
                    if alpha >= beta:
                        break
        return bestValue

def isEmptyAndHasAdjacent(board, size, row, col):
    if board[row][col] != ' ':
        return False
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), 
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < size and 0 <= c < size:
            if board[r][c] in ['x', 'o']:
                return True
    return False

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
board = [['x', 'o', ' '],
         [' ', 'o', ' '],
         [' ', ' ', 'x']]
board = [['o', 'o', 'o', 'o', 'x'],
         ['o', 'o', 'o', 'x', 'x'],
         ['x', 'o', 'x', 'x', 'x'],
         ['o', 'x', 'x', 'x', 'x'],
         ['o', 'x', 'o', 'x', 'o']]
'''
'''
board = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ']]


board = [[' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ']]
'''
'''
board = [[' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ']]
#print(countX(board))
#print(countO(board))
#print(evaluate(board, 6))
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

while (not isFull(board, 15)):
    a = int(input())
    b = int(input())
    board[a][b] = 'x'
    move = get_move(board, 15)
    print(move)
    board[move[0]][move[1]] = 'o'
    
    print(board)
    if (evaluate(board, 15) == 10): 
        print('x win')
        break
    elif (evaluate(board, 15) == -10): 
        print('o win')
        break
print("draw")
#print(get_move(board, 5))    
'''
