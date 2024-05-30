import copy
import random
import math

from Game import Game

# này mà còn không hiểu nữa thì chịu rồi
def get_move(board, size):
   game = Game(board, size)

   row, col = divmod(game.move(), size)

   return (row, col)

