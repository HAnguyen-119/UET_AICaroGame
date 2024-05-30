import math
import random
import heapq

from Utility import Utility
from Zobrist import Zobrist

WIN_SIZE = 5

class Game:
   def __init__(self, board, size):
      self.board = board
      self.size = size
      self.util = Utility(self.board, self.size)
      self.zobrist = Zobrist()
      self.RANDTAB = self.zobrist.zobrist(self.size)
      self.TRANSPOS_TAB = []

   def actions(self):
      res = []
      threat_space = []
      check_row = [0, self.size, -self.size]
      check_col = [-1, 0, 1]
      util = self.utility()
      for i in range(self.size):
         for j in range(self.size):
            if self.board[i][j] == ' ':
               found = False
               for row in check_row:
                  if found:
                     break
                  for col in check_col:
                     index = i * self.size + j
                     if ((index + 1) % 15 == 0 and col == 1) or (index % 15 == 0 and col == -1):
                        continue
                     n = index + row + col
                     if n >= 0 and n < 225 and self.board[n // self.size][n % self.size] != ' ':
                        res.append(index)
                        found = True
                        break
      for index in res:
         self.result(index, 'x')
         x_util = self.utility()
         self.back(index)

         self.result(index, 'o')
         o_util = self.utility()
         self.back(index)

         if x_util != util or o_util != util:
            threat_space.append((index, max(abs(x_util - util), abs(o_util - util))))
      threat_space.sort(key=lambda x: x[1], reverse=True)
    
      return [x[0] for x in threat_space[:3]] if threat_space else res[:3]

   def result(self, action, player):
      self.board[action // self.size][action % self.size] = player
   
   def back(self, action):
      self.board[action // self.size][action % self.size] = ' '

   def utility(self):
      winner = self.util.calculate_winner()
      if winner != None:
         return math.inf if winner[0] == 'x' else -math.inf
      else:
         stf, fou, brt, blt = self.util.six_utility()
         thr, two = self.util.five_utility()
         return 500 * (two[0] - two[1]) + 2000 * (blt[0] - blt[1]) + 15000 * (brt[0] - brt[1]) + 30000 * (thr[0] - thr[1]) + 500000 * (fou[0] - fou[1]) + 20000000 * (stf[0] - stf[1])

   def terminal(self):
      return self.util.calculate_winner() != None or self.is_draw()


   def max_player(self, alpha, beta, depth):
      if self.terminal() or depth > 3:
         return [self.utility(), None]
      board_hash, cur_acts = self.zobrist.hash(self.board, self.size, self.RANDTAB), self.actions()
      v = [alpha, cur_acts[0] if len(cur_acts) > 0 else 112]
      if board_hash in self.TRANSPOS_TAB:
         return [alpha, self.TRANSPOS_TAB[self.TRANSPOS_TAB.index(board_hash)]]
      
      for action in cur_acts:
         self.result(action, 'x')
         min_val = self.min_player(v[0], beta, depth + 1)
         self.back(action)
         
         if min_val[0] > v[0]:
            v = [min_val[0], action]
            if v[0] >= beta:
               break
      self.TRANSPOS_TAB.append(v[1])
      return v

   def min_player(self, alpha, beta, depth):
      if self.terminal() or depth > 3:
         return [self.utility(), None]
      
      board_hash, cur_acts = self.zobrist.hash(self.board, self.size, self.RANDTAB), self.actions()
      v = [beta, cur_acts[0] if len(cur_acts) > 0 else 112]
      if board_hash in self.TRANSPOS_TAB:
         return [beta, self.TRANSPOS_TAB[self.TRANSPOS_TAB.index(board_hash)]]
      
      for action in cur_acts:
         self.result(action, 'o')
         max_val = self.max_player(alpha, v[0], depth + 1)
         self.back(action)
         if max_val[0] < v[0]:
            v = [max_val[0], action]
            if alpha >= v[0]:
               break
      self.TRANSPOS_TAB.append(v[1])

      return v
   
   def move(self, player):
      return self.min_player(-math.inf, math.inf, 0)[1]

   def make_move(self, action, player):
      self.board[action // self.size][action % self.size] = player

   def is_draw(self):
      return not any(' ' in row for row in self.board) and self.util.calculate_winner() == None

   def render(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 'x':
                    print("X", end=" ")
                elif self.board[i][j] == 'o':
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()

if __name__ == "__main__":
   arr = ['x', 'x', 'x', ' ', ' ', ' ', ' ']
   board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', 'x', 'x', 'o', ' ', ' ', ' ', ' '], 
            [' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', 'o', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
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
   # print(game.actions())
   # print(game.board)
   # print(game.utility())
   # game.result(80, 'x')
   # print(game.board)
   # print(game.utility())
   # game.back(80)
   # print(game.board)
   # print(game.utility())
   # while game.util.calculate_winner() == None:
   #    game.render()
   #    print("bot is thinking")
   #    move = game.move('o')
   #    print(move)
   #    game.make_move(move, 'x')
   #    game.render()

   #    if game.util.calculate_winner() != None:
   #       break

   #    print('your turn: ')
   #    x = int(input())
   #    y = int(input())
   #    game.make_move(x * size + y, 'o')
   #    game.render()
