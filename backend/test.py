import random
import numpy as np
from collections import deque
import os

from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam

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
      if self.board[row, col] != 0:
          return self.board.copy(), -10, False, {}

      self.board[row, col] = self.current_player
      done = self.check_win(row, col)
      reward = 0 
      if self.check_win(row, col):
          reward = 10 if self.current_player == 1 else -10
      else:
          reward += self.evaluate_move(row, col, self.current_player)
      self.current_player *= -1
      return self.board.copy(), reward, done, {}

  def check_win(self, row, col):
      for i in range(15):
          for j in range(11):
              if (self.board[i, j] == self.board[i, j + 1] == self.board[i, j + 2] == self.board[i, j + 3] == self.board[i, j + 4]):
                  return True

      for i in range(15):
          for j in range(11):
              if  (self.board[j, i] == self.board[j + 1, i] == self.board[j + 2, i] == self.board[j + 3, i] == self.board[j + 4, i]):
                  return True

      for i in range(11):
          for j in range(11):
              if (self.board[i, j] == self.board[i + 1, j + 1] == self.board[i + 2, j + 2] == self.board[i + 3, j + 3] == self.board[i + 4, j + 4]):
                  return True
      
      for i in range(11):
          for j in range(11):
              if (self.board[i, 15 - j] == self.board[i + 1, 14 - j] == self.board[i + 2, 13 - j] == self.board[i + 3, 12 - j] == self.board[i + 4, 11 - j]):
                  return True

      return False


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

class DQNAgent:
  def __init__(self, state_size, action_size):
      self.state_size = state_size
      self.action_size = action_size
      self.memory = deque(maxlen=2000)
      self.gamma = 0.95
      self.epsilon = 1.0 
      self.epsilon_min = 0.01
      self.epsilon_decay = 0.995
      self.learning_rate = 0.001
      self.model = self._build_model()
      self.target_model = self._build_model()
      self.update_target_model()

  def _build_model(self):
      model = Sequential()
      model.add(Dense(256, activation='relu', input_shape=(15, 15)))
      model.add(Dense(256, activation='relu'))
      model.add(Dense(256, activation='relu'))
      model.add(Dense(self.action_size, activation='linear'))
      model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
      return model

  def update_target_model(self):
      self.target_model.set_weights(self.model.get_weights())

  def remember(self, state, action, reward, next_state, done):
      self.memory.append((state, action, reward, next_state, done))

  def act(self, state):
      if np.random.rand() <= self.epsilon:
          return random.randrange(self.action_size)
      act_values = self.model.predict(np.expand_dims(state, axis=0), verbose=0)
      return np.argmax(act_values[0])

  def replay(self, batch_size):
      minibatch = random.sample(self.memory, batch_size)
      for state, action, reward, next_state, done in minibatch:
          target = reward
          if not done:
              target = (reward + self.gamma *
                        np.amax(self.target_model.predict(np.expand_dims(next_state, axis=0), verbose=0)[0]))
          target_f = self.model.predict(state.reshape(1, 15, 15), verbose=0)
          row, col = divmod(action, 15)
          target_f[0][row, col] = target
          self.model.fit(np.expand_dims(state, axis=0), target_f, epochs=1, verbose=0)
      if self.epsilon > self.epsilon_min:
          self.epsilon *= self.epsilon_decay

  def save_model(self, agent):
      agent.model.save_weights("dqn_model.weights.h5")

  def load_model_weights(self, agent):
      if os.path.exists("dqn_model.weights.h5"):
          agent.model.load_weights("dqn_model.weights.h5")
          agent.update_target_model()
          print(f"Loaded model weights from {"dqn_model.weights.h5"}")
      else:
          print(f"No model weights found at {"dqn_model.weights.h5"}, starting from scratch.")

# if __name__ == "__main__":
#     env = TicTacToeEnv()
#     state_size = (15, 15)
#     action_size = 15 * 15  # 225 possible actions (15x15 board)
#     agent = DQNAgent(state_size, action_size)
#     batch_size = 32
#     episodes = 50

#       load_model_weights(agent)

#     for e in range(episodes):
#         state = env.reset()
#         done = False
#         total_reward = 0

#         while not done:
#             action = agent.act(state)
#             next_state, reward, done, _ = env.step(action)
#             total_reward += reward
#             agent.remember(state, action, reward, next_state, done)
#             state = next_state
#             x, y = divmod(action, 15)
#             env.board[x, y] = 1
#             env.render()

#             a = int(input())
#             b = int(input())
#             env.board[a, b] = -1
#             env.render()

#             if done:
#                 agent.update_target_model()
#                 print(f"Episode: {e+1}/{episodes}, Score: {total_reward}, Epsilon: {agent.epsilon:.2}")

#             if len(agent.memory) > batch_size:
#                 agent.replay(batch_size)
            


#     save_model(agent)

#     env.render()