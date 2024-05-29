import math
import random

from Utility import Utility
from Zobrist import Zobrist

WIN_SIZE = 5

class Game:
   def __init__(self, board, size):
      self.board = board
      self.size = size
      self.util = Utility(self.board, self.size)
      self.zobrist = Zobrist()
      self.RANDTAB = self.zobris.zobrist()
      self.TRANSPOS_TAB = []

   def actions(self):
      res = []
      threat_space = []
      check_row = [0, -self.size, self.size]
      check_col = [-1, 0, 1]
      util = self.utility()
      for i in range(self.size):
         for j in range(self.size):
            if self.board[i][j] == None:
               found = False
               for row in check_row:
                  if found:
                     break
                  for col in check_col:
                     index = i * self.size + j
                     if ((index + 1) % 15 == 0 and col == 1) or (index % 15 == 0 and col == -1):
                        continue
                     n = index + row + col
                     if n >= 0 and n < 255 and self.board[n // self.size][n % self.size] != None:
                        res.append(index)
                        found = true
                        break
      
      for i in res:
         self.result(index, 'x')
         x_util = self.utility()
         self.back(index, 'x')

         self.result(index, 'o')
         o_util = self.utility()
         self.back(index, 'o')

         if (x_util != util or o_util != util):
            threat_space.append([index, max(abs(x_util - util), abs(o_util - util))])
      
      threat_space 

   def result(self, action, player):
      self.board[action // self.size][action % self.size] = player
   
   def back(self, action, player):
      self.board[action // self.size][action % self.size] == ' '

   def utility(self):
      winner = self.util.calculate_winner()
      if winner != None:
         return math.inf if winner[0] == 'x' else -math.inf
      else:
         two, blt, brt, thr, fou, stf = self.util.two(), self.util.block_three(), self.util.broken_three(), self.util.straight_three(), self.util.four(), self.util.straight_four()
         return 5 * (two[0] - two[1]) + 20 * (blt[0] - blt[1]) + 150 * (brt[0] - brt[1]) + 300 * (thr[0] - thr[1]) + 5000 * (fou[0] - fou[1]) + 200000 * (stf[0] - stf[1])

   def terminal(self):
      return self.util.calculate_winner() == None or self.is_draw()


   def max_player(self, alpha, beta, depth):
      if self.terminal() or depth > 3:
         return [self.utility(), None]
      [board_hash, cur_acts] = [self.zobrist.hash(self.board, self.size, self.RANDTAB), self.actions()]
      return math.inf

   def is_draw(self):
      return not any(' ' in row for row in self.board) and self.util.calculate_winner() == None

   


if __name__ == "__main__":
   arr = ['x', 'x', 'x', ' ', ' ', ' ', ' ']
   board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'o', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            ]
   test_draw = [['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], 
                ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o'], 
                ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o'], 
                ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o'], 
                ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], 
                ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], 
                ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], 
                ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o'], 
                ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o'], 
                ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o'], 
                ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'], 
                ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o'], 
                ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o'], 
                ['o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o'], 
                ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'] 
                ]
   size = 15
   game = Game(board, size)
   print(Game(test_draw, size).zobrist())
