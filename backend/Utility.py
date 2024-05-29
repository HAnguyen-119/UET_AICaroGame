WIN_SIZE = 5

class Utility:
   def __init__(self, board, size):
      self.board = board
      self.size = size
   
   def make_diags(self, start, n, d):
      return [start + i * d for i in range(n)]
   
   def counter(self, arr):
      count = {}
      for x in arr:
         count[x] = (count.get(x, 0) + 1)
      return count
   
   def calculate_lines(self, n):
      res = []
      #row
      for i in range(self.size):
         for j in range(self.size - n + 1):
            row = [[i, j + k] for k in range(n)]
            res.append(row)
      
      #col
      for i in range(self.size):
         for j in range(self.size - n + 1):
            col = [[j + k, i] for k in range(n)]
            res.append(col)
      
      #main diagonal
      for i in range(self.size - n + 1):
         for j in range(self.size - n + 1):
            diag = [[i + k, j + k] for k in range(n)]
            res.append(diag)

      #secondary diagonal
      for i in range(self.size - n + 1):
         for j in range(n - 1, self.size):
            diag = [[i + k, j - k] for k in range(n)]
            res.append(diag)
      return res
         
   def calculate_winner(self):
      LINES = self.calculate_lines(WIN_SIZE)
      for line in LINES:
         first_value = self.board[line[0][0]][line[0][1]]
         if first_value != ' ' and all(self.board[pos[0]][pos[1]] == first_value for pos in line):
            return [first_value, line]

      return None

   def four(self):
      res = [0, 0]
      SIXES = self.calculate_lines(6)

      for line in SIXES:
         middle = line[1:5]
         line_val = [self.board[x[0]][x[1]] for x in line]
         is_four = all(self.board[x[0]][x[1]] == self.board[middle[0][0]][middle[0][1]] for x in middle)
         if self.board[middle[0][0]][middle[0][1]] != ' ':
            if is_four and self.counter(line_val).get(' ', 0) == 1:
               if self.board[middle[0][0]][middle[0][1]] == 'x':
                  res[0] += 1
               else:
                  res[1] += 1
      return res
   
   def straight_four(self):
      res = [0, 0]
      SIXES = self.calculate_lines(6)

      for line in SIXES:
         middle = line[1:5]
         line_val = [self.board[x[0]][x[1]] for x in line]
         is_four = all(self.board[x[0]][x[1]] == self.board[middle[0][0]][middle[0][1]] for x in middle)
         if self.board[middle[0][0]][middle[0][1]] != ' ':
            if is_four and self.counter(line_val).get(' ', 0) == 2:
               if self.board[middle[0][0]][middle[0][1]] == 'x':
                  res[0] += 1
               else:
                  res[1] += 1
      return res

   def straight_three(self):
      res = [0, 0]
      FIVES = self.calculate_lines(5)

      for line in FIVES:
         middle = line[1:4]
         line_val = [self.board[x[0]][x[1]] for x in line]
         is_three = all(self.board[x[0]][x[1]] == self.board[middle[0][0]][middle[0][1]] for x in middle)
         if self.board[middle[0][0]][middle[0][1]] != ' ':
            if is_three and self.counter(line_val).get(' ', 0) == 2:
               if self.board[middle[0][0]][middle[0][1]] == 'x':
                  res[0] += 1
               else:
                  res[1] += 1
      return res
   
   def broken_three(self):
      res = [0, 0]
      SIXES = self.calculate_lines(6)

      for line in SIXES:
         middle = line[1:5]

         line_val = [self.board[x[0]][x[1]] for x in line]
         middle_val = [self.board[x[0]][x[1]] for x in middle]

         is_three = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 3
         if self.board[middle[0][0]][middle[0][1]] != ' ' and self.board[middle[3][0]][middle[3][1]] != ' ':
            if is_three:
               if self.counter(middle_val).get('x', 0) == 3:
                  res[0] += 1
               elif self.counter(middle_val).get('o', 0) == 3:
                  res[1] += 1
      return res

   def block_three(self):
      res = [0, 0]
      SIXES = self.calculate_lines(6)

      for line in SIXES:
         middle = line[1:5]

         line_val = [self.board[x[0]][x[1]] for x in line]
         middle_val = [self.board[x[0]][x[1]] for x in middle]

         is_three = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 2
         if is_three:
            if self.counter(middle_val).get('x', 0) == 3 and self.counter(line_val).get('x', 0) == 3:
               res[0] += 1
            elif self.counter(middle_val).get('o', 0) == 3 and self.counter(line_val).get('o', 0) == 3:
               res[1] += 1
      return res
   
   def two(self):
      res = [0, 0]
      FIVES = self.calculate_lines(5)
      
      for line in FIVES:
         middle = line[1:4]

         line_val = [self.board[x[0]][x[1]] for x in line]
         middle_val = [self.board[x[0]][x[1]] for x in middle]

         is_two = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 3
         if is_two:
            if self.counter(middle_val).get('x', 0) == 2:
               res[0] += 1
            elif self.counter(middle_val).get('o', 0) == 2:
               res[1] += 1
      
      return res



   

if __name__ == '__main__':
   arr = ['x', 'x', 'x', ' ', ' ', ' ', ' ']
   board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', 'x', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            ]
   size = 15
   utility = Utility(board, size)
   bt = utility.broken_three()
   print(bt)
