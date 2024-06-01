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
import math

from Game import Game

# này mà còn không hiểu nữa thì chịu rồi
def get_move(board, size):
   game = Game(board, size)

   row, col = divmod(game.move(), size)

   return (row, col)

