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

   # lấy ra 3 action có điểm quality cao nhất dùng trong minimax
   def actions(self):
      res = []

      # threat space search
      threat_space = []

      # check các vị trí lân cận có depth là 3
      check_row = [0, self.size, -self.size]
      check_col = [-1, 0, 1]

      # điểm của bảng hiện tại
      util = self.utility()
      for i in range(self.size):
         for j in range(self.size):
            if self.board[i][j] == ' ':
               found = False
               for row in check_row:
                  if found:
                     break
                  for col in check_col:

                     # giá trị của vị trí đó theo thang (1, size * size)
                     index = i * self.size + j

                     # các vị trí góc của board thì có thể bỏ qua
                     if ((index + 1) % 15 == 0 and col == 1) or (index % 15 == 0 and col == -1):
                        continue

                     # lưu lại vị trí để tính xem có hợp lệ hay không
                     new_index = index + row + col
                     if new_index >= 0 and new_index < self.size * self.size and self.board[new_index // self.size][new_index % self.size] != ' ':
                        res.append(index)
                        found = True
                        break
      
      # tính utility cho các điểm có Quality cao
      for index in res:
         # điểm của x move
         self.temp_board_utility(index, 'x')
         x_util = self.utility()

         #trả lại bảng cũ
         self.back(index)

         # điểm của o move
         self.temp_board_utility(index, 'o')
         o_util = self.utility()
         
         #trả lại bảng cũ
         self.back(index)

         # nếu điểm của x và o đều giống điểm của bảng tức là nước đi đó không hợp lệ, không cần thêm vào threat space
         if x_util != util or o_util != util:
            threat_space.append((index, max(abs(x_util - util), abs(o_util - util))))
      
      # sort theo điểm từ cao tới thấp
      # có thể sử dụng max heap, cơ mà syntax heap của python chưa tìm hiểu
      threat_space.sort(key=lambda x: x[1], reverse=True)

      # lấy 3 giá trị tốt nhất 
      return [x[0] for x in threat_space[:3]] if threat_space else res[:3]

   # bảng tạm thời cho nước đi tiếp theo của player
   def temp_board_utility(self, action, player):
      self.board[action // self.size][action % self.size] = player
   
   # trả về bảng cũ sau nước đi tạm thời
   def back(self, action):
      self.board[action // self.size][action % self.size] = ' '

   # tính điểm utility
   # cụ thể xem ở file Utility.py
   def utility(self):
      winner = self.util.calculate_winner()
      if winner != None:
         return math.inf if winner[0] == 'x' else -math.inf
      else:
         stf, fou, brt, blt = self.util.six_utility()
         thr, two = self.util.five_utility()
         return 500 * (two[0] - two[1]) + 2000 * (blt[0] - blt[1]) + 15000 * (brt[0] - brt[1]) + 30000 * (thr[0] - thr[1]) + 500000 * (fou[0] - fou[1]) + 20000000 * (stf[0] - stf[1])
         # thr, two, brf = self.util.five_utility()
         # return 500 * (two[0] - two[1]) + 2000 * (blt[0] - blt[1]) + 15000 * (brt[0] - brt[1]) + 30000 * (thr[0] - thr[1]) + 500000 * (fou[0] - fou[1]) + 5000000 * (brf[0] - brf[1]) + 20000000 * (stf[0] - stf[1])

   # điều kiện dừng của minimax
   def terminal(self):
      return self.util.calculate_winner() != None or self.is_draw()

   # minimax và alpha beta prunning, khỏi giải thích, không hiểu về đọc lại chương 1
   # hash chỉ để lưu lại giá trị hiện tại của bàn cờ và điểm utility cũ, bỏ qua cái này và đọc thì nó giống hệt minimax trên geeksforgeeks
   # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
   def max_player(self, alpha, beta, depth):
      if self.terminal() or depth > 3:
         return [self.utility(), None]
      board_hash, cur_acts = self.zobrist.hash(self.board, self.size, self.RANDTAB), self.actions()
      val = [alpha, cur_acts[0] if len(cur_acts) > 0 else self.get_random_move()] 
      if board_hash in self.TRANSPOS_TAB:
         return [alpha, self.TRANSPOS_TAB[self.TRANSPOS_TAB.index(board_hash)]]
      
      for action in cur_acts:
         self.temp_board_utility(action, 'x')
         min_val = self.min_player(val[0], beta, depth + 1)
         self.back(action)
         
         if min_val[0] > val[0]:
            val = [min_val[0], action]
            if val[0] >= beta:
               break
      self.TRANSPOS_TAB.append(val[1])
      return val

   def min_player(self, alpha, beta, depth):
      if self.terminal() or depth > 3:
         return [self.utility(), None]
      
      board_hash, cur_acts = self.zobrist.hash(self.board, self.size, self.RANDTAB), self.actions()
      val = [beta, cur_acts[0] if len(cur_acts) > 0 else self.get_random_move()]
      if board_hash in self.TRANSPOS_TAB:
         return [beta, self.TRANSPOS_TAB[self.TRANSPOS_TAB.index(board_hash)]]
      
      for action in cur_acts:
         self.temp_board_utility(action, 'o')
         max_val = self.max_player(alpha, val[0], depth + 1)
         self.back(action)
         if max_val[0] < val[0]:
            val = [max_val[0], action]
            if alpha >= val[0]:
               break
      self.TRANSPOS_TAB.append(val[1])

      return val
   
   # random
   def get_random_move(self):
      return random.randint(0, self.size * self.size - 1)

   # tạo nước đi, dùng min player hay max player cũng được
   def move(self):
      return self.min_player(-math.inf, math.inf, 0)[1]

   # điều kiện hoà là phải không có ô trống nào và không có ai thắng
   def is_draw(self):
      return not any(' ' in row for row in self.board) and self.util.calculate_winner() == None

   # cái này để test trong hàm main

   def make_move(self, action, player):
      self.board[action // self.size][action % self.size] = player
   
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
   board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
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
   size = 13
   game = Game(board, size)
   # print(game.actions())
   # print(game.actions())
   # print(game.board)
   # print(game.utility())
   # game.temp_board_utility(80, 'x')
   # print(game.board)
   # print(game.utility())
   # game.back(80)
   # print(game.board)
   # print(game.utility())
   while game.util.calculate_winner() == None:
      game.render()
      print("bot is thinking")
      move = game.move()
      print(move)
      game.make_move(move, 'x')
      game.render()

      if game.util.calculate_winner() != None:
         break

      print('your turn: ')
      x = int(input())
      y = int(input())
      game.make_move(x * size + y, 'o')
      game.render()

