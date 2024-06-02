WIN_SIZE = 5

#Tính điểm Quality cho nước đi
#Cases: 
'''
win: infinity for x, -infinity for o
straight four: .xxxx., .oooo. - point: 20000000 for x, -20000000 for o
block four: oxxxx., .xxxxo, xoooo., .oooox - point: 500000 for x, -5000000 for o
straight_three: - point: 30000 for x, -30000 for o
broken three: - point: 15000 for x, -15000 for o
block three: - point: 2000 for x, -2000 for o
two: - point: 500 for x, -500 for o
'''
class Utility:
   def __init__(self, board, size):
      self.board = board
      self.size = size
   
   # Đếm số lượng x, y và ô trống trong một arr
   ## Phục vụ cho tính các trường hợp xảy ra của Utility Method
   def counter(self, arr):
      count = {}
      for x in arr:
         count[x] = (count.get(x, 0) + 1)
      return count
   
   # Lưu lại tất cả các dòng, cột và đường chéo thích hợp cho độ dài length
   def calculate_lines(self, length):
      lines_array = []

      #row & col
      for i in range(self.size):
         for j in range(self.size - length + 1):
            row = [[i, j + k] for k in range(length)]
            lines_array.append(row)
            col = [[j + k, i] for k in range(length)]
            lines_array.append(col)
      
      #main diagonal
      for i in range(self.size - length + 1):
         for j in range(self.size - length + 1):
            diag = [[i + k, j + k] for k in range(length)]
            lines_array.append(diag)

      #secondary diagonal
      for i in range(self.size - length + 1):
         for j in range(length - 1, self.size):
            diag = [[i + k, j - k] for k in range(length)]
            lines_array.append(diag)
      return lines_array
         
   def calculate_winner(self):
      FIVES = self.calculate_lines(WIN_SIZE)
      for line in FIVES:
         
         # Lưu lại giá trị đầu tiên (nếu xxxxx thì giá trị đầu tiên là x, ooooo thì giá trị đầu tiên là o)
         first_value = self.board[line[0][0]][line[0][1]]

         # Kiểm tra xem tất cả các dòng 5 đều là x hay đều là o
         if first_value != ' ' and all(self.board[pos[0]][pos[1]] == first_value for pos in line):
            return [first_value, line]

      return None

   # cho các utility có array size = 6
   def six_utility(self):
      stf, fou, brt, blt = [0, 0], [0, 0], [0, 0], [0, 0]
      SIXES = self.calculate_lines(6)

      for line in SIXES:
         #cắt 4 giá trị ở giữa
         middle = line[1:5]

         '''
          line là các position của bảng ví dụ [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]] nên phải lấy giá trị line_val
          giả sử line_val sẽ là [' ', 'x', 'x', ' ', 'o']
          tương tự middle và middle_val
         '''
         line_val = [self.board[x[0]][x[1]] for x in line]
         middle_val = [self.board[x[0]][x[1]] for x in middle]

         # Nếu cả 4 giá trị cùng bằng nhau. VD .xxxx. thì middle là xxxx
         is_four = all(self.board[x[0]][x[1]] == self.board[middle[0][0]][middle[0][1]] for x in middle)  

         '''
          Nếu ở middle có 1 ô trống và bên ngoài có 2 ô trống
          ví dụ: .xx.x. thì tổng cộng có 3 ô trống (2 ô ở ngoài và 1 ô ở middle)
         '''
         is_broken_three = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 3

         '''
          tương tự broken three nhưng ở ngoài chỉ có 1 ô trống
          đã loại trường hợp .xx.xx ở trong if else 
          ví dụ: .xx.xo, ox.xx.
         '''
         is_block_three = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 2

         if self.board[middle[0][0]][middle[0][1]] != ' ':

            '''
             Straight Four
             2 ô ở ngoài là ô trống
            '''
            if is_four and self.counter(line_val).get(' ', 0) == 2:
               if self.board[middle[0][0]][middle[0][1]] == 'x':
                  stf[0] += 1
               else:
                  stf[1] += 1
            
            '''
             Block Four
             bị chặn 1 đầu nên chỉ có 1 ô trống
            '''
            if is_four and self.counter(line_val).get(' ', 0) == 1:
               if self.board[middle[0][0]][middle[0][1]] == 'x':
                  fou[0] += 1
               else:
                  fou[1] += 1

            '''
             Broken Three
             điều kiện broken three là cả 2 đầu của middle phải là x hoặc o (nếu không sẽ bị trùng straight three)
            '''
            if self.board[middle[3][0]][middle[3][1]] != ' ':
               if is_broken_three:
                  if self.counter(middle_val).get('x', 0) == 3:
                     brt[0] += 1
                  elif self.counter(middle_val).get('o', 0) == 3:
                     brt[1] += 1

            '''
             Block Three
             tương tự broken three nhưng ở ngoài chỉ có 1 ô trống
            '''
            if is_block_three:
               if self.counter(middle_val).get('x', 0) == 3 and self.counter(line_val).get('x', 0) == 3:
                  blt[0] += 1
               elif self.counter(middle_val).get('o', 0) == 3 and self.counter(line_val).get('o', 0) == 3:
                  blt[1] += 1
         
         
      return stf, fou, brt, blt # (straight four, four, broken three, block three)

   # cho các utitlity có array size = 5
   def five_utility(self):
      thr, two, thf = [0, 0], [0, 0], [0, 0]
      FIVES = self.calculate_lines(5)

      for line in FIVES:
         # cắt 3 ô ở giữa
         middle = line[1:4]

         line_val = [self.board[x[0]][x[1]] for x in line]
         middle_val = [self.board[x[0]][x[1]] for x in middle]

         is_three = all(self.board[x[0]][x[1]] == self.board[middle[0][0]][middle[0][1]] for x in middle)

         is_three_in_five = self.counter(middle_val).get(' ', 0) == 2
         is_block_three = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 2
         is_broken_three = self.counter(middle_val).get(' ', 0) == 1 and (self.counter(middle_val).get('x', 0) == 3 or self.counter(middle_val).get('o', 0) == 3)

         if is_three_in_five:
            if self.counter(line_val).get('x', 0) == 3:
               thf[0] += 1
            elif self.counter(line_val).get('o', 0) == 3:
               thf[1] += 1

         if self.board[middle[0][0]][middle[0][1]] != ' ':
            if is_three and self.counter(line_val).get(' ', 0) == 2:
               if self.board[middle[0][0]][middle[0][1]] == 'x':
                  thr[0] += 1
               else:
                  thr[1] += 1
         
         is_two = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 3
         if is_two:
            if self.counter(middle_val).get('x', 0) == 2:
               two[0] += 1
            elif self.counter(middle_val).get('o', 0) == 2:
               two[1] += 1
      return thr, thf, two  # three, two
   
   '''
   # def straight_four(self):
   #    res = [0, 0]
   #    SIXES = self.calculate_lines(6)

   #    for line in SIXES:
   #       middle = line[1:5]
   #       line_val = [self.board[x[0]][x[1]] for x in line]
   #       is_four = all(self.board[x[0]][x[1]] == self.board[middle[0][0]][middle[0][1]] for x in middle)
   #       if self.board[middle[0][0]][middle[0][1]] != ' ':
   #          if is_four and self.counter(line_val).get(' ', 0) == 2:
   #             if self.board[middle[0][0]][middle[0][1]] == 'x':
   #                res[0] += 1
   #             else:
   #                res[1] += 1
   #    return res
   
   # def broken_three(self):
   #    res = [0, 0]
   #    SIXES = self.calculate_lines(6)

   #    for line in SIXES:
   #       middle = line[1:5]

   #       line_val = [self.board[x[0]][x[1]] for x in line]
   #       middle_val = [self.board[x[0]][x[1]] for x in middle]

   #       is_three = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 3
   #       if self.board[middle[0][0]][middle[0][1]] != ' ' and self.board[middle[3][0]][middle[3][1]] != ' ':
   #          if is_three:
   #             if self.counter(middle_val).get('x', 0) == 3:
   #                res[0] += 1
   #             elif self.counter(middle_val).get('o', 0) == 3:
   #                res[1] += 1
   #    return res

   # def block_three(self):
   #    res = [0, 0]
   #    SIXES = self.calculate_lines(6)

   #    for line in SIXES:
   #       middle = line[1:5]

   #       line_val = [self.board[x[0]][x[1]] for x in line]
   #       middle_val = [self.board[x[0]][x[1]] for x in middle]

   #       is_three = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 2
   #       if is_three:
   #          if self.counter(middle_val).get('x', 0) == 3 and self.counter(line_val).get('x', 0) == 3:
   #             res[0] += 1
   #          elif self.counter(middle_val).get('o', 0) == 3 and self.counter(line_val).get('o', 0) == 3:
   #             res[1] += 1
   #    return res
   
   # def two(self):
   #    res = [0, 0]
   #    FIVES = self.calculate_lines(5)
      
   #    for line in FIVES:
   #       middle = line[1:4]

   #       line_val = [self.board[x[0]][x[1]] for x in line]
   #       middle_val = [self.board[x[0]][x[1]] for x in middle]

   #       is_two = self.counter(middle_val).get(' ', 0) == 1 and self.counter(line_val).get(' ', 0) == 3
   #       if is_two:
   #          if self.counter(middle_val).get('x', 0) == 2:
   #             res[0] += 1
   #          elif self.counter(middle_val).get('o', 0) == 2:
   #             res[1] += 1
      
   #    return res


'''
   

if __name__ == '__main__':
   arr = ['x', 'x', 'x', ' ', ' ', ' ', ' ']
   board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', 'x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', 'x', ' ', 'x', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', 'o', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
            ]
   size = 15
   utility = Utility(board, size)
   thr, thf, two = utility.five_utility()
   print(thr)

