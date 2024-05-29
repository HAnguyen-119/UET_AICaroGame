import random

class Zobrist:   
   def randomInt(self):
      min = 0
      max = pow(2, 64)
      return random.randint(min, max)
   
   def indexOf(self, piece):
      return 0 if piece == 'x' else 1

   def zobrist(self, size):
      return [[[self.randomInt() for k in range(2)] for j in range(size)] for i in range(size)]

   def hash(self, board, size, zobrist_table):
      h = 0
      for i in range(size):
         for j in range(size):
            if board[i][j] != ' ':
               piece = self.indexOf(board[i][j])
               h ^= zobrist_table[i][j][piece]
      return h

if __name__ == '__main__':
   zobrist = Zobrist()
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
   zobrist_table = zobrist.zobrist(size)
   hash_value = zobrist.hash(board, size, zobrist_table)
   print(hash_value)
