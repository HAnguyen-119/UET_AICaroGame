# import copy
# import random
# import math

# def get_move(board, size):
#     # Find all available positions on the board
#     a = int(input())
#     b = int(input())
#     return (a, b)
#     size = int(size)
#     '''
#     available_moves = []
#     for i in range(size):
#         for j in range(size):
#             if board[i][j] == ' ':
#                 available_moves.append((i, j))

#     # If there are no available moves, return None
#     if not available_moves:
#         return None
#     '''
#     nextMove = (-1, -1)
#     isMaximizing = isXTurn(board, size)
#     if isMaximizing:
#         bestMoveValue = -math.inf
#         for i in range(size):
#             for j in range(size):
#                 if board[i][j] == ' ':
#                     board[i][j] = 'x'
#                     bestValue = minimax(board, size, 0, False, -math.inf, math.inf)
#                     board[i][j] = ' '
#                     if bestValue >= bestMoveValue: 
#                         nextMove = (i, j)
#                         bestMoveValue = bestValue
#     else:
#         bestMoveValue = math.inf
#         for i in range(size):
#             for j in range(size):
#                 if board[i][j] == ' ':
#                     board[i][j] = 'o'
#                     bestValue = minimax(board, size, 0, True, -math.inf, math.inf)
#                     board[i][j] = ' '
#                     if bestValue <= bestMoveValue: 
#                         nextMove = (i, j)
#                         bestMoveValue = bestValue         
#     return nextMove

# def countX(board, size):
#     x = 0
#     for i in range(size):
#         for j in range(size):
#             if board[i][j] == 'x': x += 1
#     return x  

# def countO(board, size):
#     o = 0
#     for i in range(size):
#         for j in range(size):
#             if board[i][j] == 'o': o += 1
#     return o  
   
# def isXTurn(board, size):
#     return countX(board, size) == countO(board, size)        
    
# def evaluate(board, size):
#     # Check rows
#     for i in range(size):
#         for j in range(size - 4):
#             if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == board[i][j + 4]:
#                 if board[i][j] == 'x': return 10
#                 elif board[i][j] == 'o': return -10
#     # Check columns
#     for i in range(size):
#         for j in range(size - 4):
#             if board[j][i] == board[j + 1][i] == board[j + 2][i] == board[j + 3][i] == board[j + 4][i]:
#                 if board[j][i] == 'x': return 10
#                 elif board[j][i] == 'o': return -10
#     # Check diagonals
#     for i in range(size - 4):
#         for j in range(size - 4):
#             if (board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == board[i + 4][j + 4]):
#                 if board[i][j] == 'x': return 10
#                 elif board[i][j] == 'o': return -10
    
#     for i in range(size - 4):
#         for j in range(4, size):
#             if (board[i][j] == board[i + 1][j - 1] == board[i + 2][j - 2] == board[i + 3][j - 3] == board[i + 4][j - 4]):
#                 if board[i][j] == 'x': return 10
#                 elif board[i][j] == 'o': return -10
            
#     return 0

# def minimax(board, size, depth, isMaximizing, alpha, beta):
#     score = evaluate(board, size)
#     if depth == min(countX(board, size), size): 
#         return score
#     if score == 10:
#         return 10 - depth
#     elif score == -10:
#         return -10 + depth
#     if isMaximizing:
#         bestValue = -math.inf
#         for i in range(size):
#             for j in range(size):
#                 if board[i][j] == ' ': 
#                     board[i][j] = 'x'
#                     bestValue = max(bestValue, minimax(board, size, depth + 1, False, alpha, beta))
#                     alpha = max(alpha, bestValue)
#                     board[i][j] = ' '
#                     if alpha >= beta:
#                         break
#         return bestValue
#     else:
#         bestValue = math.inf
#         for i in range(size):
#             for j in range(size):
#                 if board[i][j] == ' ': 
#                     board[i][j] = 'o'
#                     bestValue = min(bestValue, minimax(board, size, depth + 1, True, alpha, beta))
#                     beta = min(beta, bestValue)
#                     board[i][j] = ' '
#                     if alpha >= beta:
#                         break
#         return bestValue

# '''
# board = [['x', 'o', ' '],
#          [' ', 'o', ' '],
#          [' ', ' ', 'x']]
# board = [['o', 'o', 'o', 'o', 'x'],
#          ['o', 'o', 'o', 'x', 'x'],
#          ['x', 'o', 'x', 'x', 'x'],
#          ['o', 'x', 'x', 'x', 'x'],
#          ['o', 'x', 'o', 'x', 'o']]
# '''
# board = [[' ', 'x', ' ', ' ', 'o', ' ', ' '],
#          [' ', 'o', 'x', 'o', ' ', ' ', ' '],
#          ['x', ' ', 'o', 'x', ' ', ' ', 'o'],
#          [' ', 'o', ' ', 'o', 'x', 'o', ' '],
#          ['o', ' ', 'x', ' ', 'o', ' ', ' '],
#          [' ', ' ', ' ', 'x', ' ', ' ', ' '],
#          [' ', ' ', 'o', ' ', ' ', ' ', ' ']]
# print(evaluate(board, 7))
# #print(get_move(board, 5))    

from test import TicTacToeEnv
from test import DQNAgent

def get_move(board, size):
    env = TicTacToeEnv()
    state_size = (15, 15)
    action_size = 15 * 15
    agent = DQNAgent(state_size, action_size)
    batch_size = 32
    episodes = 1000

    agent.load_model_weights(agent)

    for e in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0

        while not done:
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            total_reward += reward
            agent.remember(state, action, reward, next_state, done)
            state = next_state

            if done:
                agent.update_target_model()
                print(f"Episode: {e+1}/{episodes}, Score: {total_reward}, Epsilon: {agent.epsilon:.2}")

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)

            return (divmod(action, 15))

    agent.save_model(agent)

    env.render()

            