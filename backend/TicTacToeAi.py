import copy
import random
import math

from Game import Game

def get_move(board, size):
   count_x, count_y = count(board, size)
   player = X if count_x == count_y else Y
   game = Game(board, size)

   row, col = divmod(game.move(), size)

   return (row, col)

