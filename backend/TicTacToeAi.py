# import copy
# import random


# def get_move(board, size):
#     # Find all available positions on the board
#     size = int(size)
#     available_moves = []
#     for i in range(size):
#         for j in range(size):
#             if board[i][j] == ' ':
#                 available_moves.append((i, j))

#     # If there are no available moves, return None
#     if not available_moves:
#         return None
#     # Choose a random available move
#     return available_moves[random.randint(0, len(available_moves) - 1)]

import copy
import random


# def get_move(board, size):
#     # Find all available positions on the board
#     size = int(size)
#     available_moves = []
#     for i in range(size):
#         for j in range(size):
#             if board[i][j] == ' ':
#                 available_moves.append((i, j))

#     # If there are no available moves, return None
#     if not available_moves:
#         return None
#     # Choose a random available move
#     return available_moves[random.randint(0, len(available_moves) - 1)]

import copy
import random
import math

'''
def get_move(board, size):
    # Find all available positions on the board
    size = int(size)
    available_moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                available_moves.append((i, j))

    # If there are no available moves, return None
    if not available_moves:
        return None
    # Choose a random available move
    return available_moves[random.randint(0, len(available_moves) - 1)]
'''

def get_move(board, size):
    # Find all available positions on the board
    size = int(size)
    available_moves = []
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                available_moves.append((i, j))

    # If there are no available moves, return None
    if not available_moves:
        return None
    nextMove = (-1, -1)
    isMaximizing = isXTurn(board, size)
    if isMaximizing:
        bestMoveValue = -math.inf
        for move in available_moves:
            board[move[0]][move[1]] = 'x'
            bestValue = minimax(board, size, 0, False, -math.inf, math.inf)
            board[move[0]][move[1]] = ' '
            if bestValue >= bestMoveValue: 
                nextMove = move
                bestMoveValue = bestValue
    else:
        bestMoveValue = math.inf
        for move in available_moves:
            board[move[0]][move[1]] = 'o'
            bestValue = minimax(board, size, 0, True, -math.inf, math.inf)
            board[move[0]][move[1]] = ' '
            if bestValue <= bestMoveValue: 
                nextMove = move
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
    for i in range(15):
            for j in range(11):
                if (board[i, j] == board[i, j + 1] == board[i, j + 2] == board[i, j + 3] == board[i, j + 4]):
                    return 1 if board[i, j] == 'x' else -1

    for i in range(15):
        for j in range(11):
            if  (board[j, i] == board[j + 1, i] == board[j + 2, i] == board[j + 3, i] == board[j + 4, i]):
                return 1 if board[i, j] == 'x' else -1

    for i in range(11):
        for j in range(11):
            if (board[i, j] == board[i + 1, j + 1] == board[i + 2, j + 2] == board[i + 3, j + 3] == board[i + 4, j + 4]):
                return 1 if board[i, j] == 'x' else -1
    
    for i in range(11):
        for j in range(11):
            if (board[i, 15 - j] == board[i + 1, 14 - j] == board[i + 2, 13 - j] == board[i + 3, 12 - j] == board[i + 4, 11 - j]):
                return 1 if board[i, 15 - j] == 'x' else -1

    return 0

def minimax(board, size, depth, isMaximizing, alpha, beta):
    score = evaluate(board, size)
    if depth == size: 
        return score
    if score == 1:
        return 10 - depth
    elif score == -1:
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
#print(evaluate(board, 5))
#print(get_move(board, 5))    