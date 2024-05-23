import numpy as np

WIN_SIZE = 5

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
        row, col = divmod(action, 15)
        if self.board[row, col] != 0:
            return self.board.copy(), -10, False, {}    
        self.board[row, col] = self.current_player
        done = self.check_win()
        reward = 0 
        if self.check_win() == 1:
            reward = 10
        elif self.check_win() == -1:
            reward = -10
        else:
            reward += self.evaluate_move(row, col, self.current_player)
        self.current_player *= -1
        return self.board.copy(), reward, done, {}
    
    def evaluate_move(self, row, col, current_player):
        if current_player == 1:
            return 1 if self.board[row, col] == 0 else -1
        return 0


    def check_win(self):
        for i in range(self.size):
            for j in range(self.size - WIN_SIZE + 1):
                if (self.board[i, j] == self.board[i, j + 1] == self.board[i, j + 2] == self.board[i, j + 3] == self.board[i, j + 4]):
                    return self.board[i, j]

        for i in range(self.size):
            for j in range(self.size - WIN_SIZE + 1):
                if (self.board[j, i] == self.board[j + 1, i] == self.board[j + 2, i] == self.board[j + 3, i] == self.board[j + 4, i]):
                    return self.board[j, i]

        for i in range(self.size - WIN_SIZE + 1):
            for j in range(self.size - WIN_SIZE + 1):
                if (self.board[i, j] == self.board[i + 1, j + 1] == self.board[i + 2, j + 2] == self.board[i + 3, j + 3] == self.board[i + 4, j + 4]):
                    return self.board[i, j]
        
        for i in range(self.size - WIN_SIZE + 1):
            for j in range(WIN_SIZE - 1, self.size):
                if (self.board[i, j] == self.board[i + 1, j - 1] == self.board[i + 2, j - 2] == self.board[i + 3, j - 3] == self.board[i + 4, j - 4]):
                    return self.board[i, j]

        return 0


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
