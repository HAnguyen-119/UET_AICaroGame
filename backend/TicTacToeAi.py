import copy
import random
import math

from Game import Game

def get_move(board, size):
   game = Game(board, size)
   row, col = divmod(game.ai_move(), size)

   return (row, col)