import numpy as np

WIN_SIZE = 5


#Code có thể sửa
class TicTacToeEnv:
    def __init__(self, size=15):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.current_player = 1

    def reset(self):
        self.board = np.zeros((self.size, self.size), dtype=int)
        self.current_player = 1
        return self.board.copy()

    def step(self, action):
        row, col = divmod(action, self.size)

        #Nếu Agent đi vào nước đã có người đi rồi thì -1 điểm
        if self.board[row, col] != 0:
            return self.board.copy(), -1, False, {}   

         
        self.board[row, col] = self.current_player
        done = False
        reward = 0 

        curr_point = self.evaluate()
        if curr_point != 0:
            reward += curr_point
            done = True
        else:
            reward += 1
        
        #Đổi người chơi
        self.current_player *= -1
        return self.board.copy(), reward, done, {}


    def evaluate(self):
        # Check rows
        for i in range(self.size):
            for j in range(self.size - WIN_SIZE + 1):
                if self.board[i][j] != self.board[i][j + 1]: continue
                if self.board[i][j] == self.board[i][j + 1] == self.board[i][j + 2] == self.board[i][j + 3] == self.board[i][j + 4]:
                    if self.board[i][j] == 1: return 10
                    elif self.board[i][j] == -1: return -10

        # Check columns
        for i in range(self.size):
            for j in range(self.size - WIN_SIZE + 1):
                if self.board[j][i] != self.board[j + 1][i]: continue
                if self.board[j][i] == self.board[j + 1][i] == self.board[j + 2][i] == self.board[j + 3][i] == self.board[j + 4][i]:
                    if self.board[j][i] == 1: return 10
                    elif self.board[j][i] == -1: return -10

        # Check diagonals
        for i in range(self.size - WIN_SIZE + 1):
            for j in range(self.size - WIN_SIZE + 1):
                if self.board[i][j] != self.board[i + 1][j + 1]: continue
                if self.board[i][j] == self.board[i + 1][j + 1] == self.board[i + 2][j + 2] == self.board[i + 3][j + 3] == self.board[i + 4][j + 4]:
                    if self.board[i][j] == 1: return 10
                    elif self.board[i][j] == -1: return -10
        
        for i in range(self.size - WIN_SIZE + 1):
            for j in range(WIN_SIZE - 1, self.size):
                if self.board[i][j] != self.board[i + 1][j - 1]: continue
                if self.board[i][j] == self.board[i + 1][j - 1] == self.board[i + 2][j - 2] == self.board[i + 3][j - 3] == self.board[i + 4][j - WIN_SIZE + 1]:
                    if self.board[i][j] == 1: return 10
                    elif self.board[i][j] == -1: return -10
                
        return 0


    #In board
    def render(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i, j] == 1:
                    print("X", end=" ")
                elif self.board[i, j] == -1:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()
