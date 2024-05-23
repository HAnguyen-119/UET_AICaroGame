import random
import numpy as np
from collections import deque
import os

from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.optimizers import Adam
from Env import TicTacToeEnv

AGENT, RANDOM = 1, -1


#Code không nên sửa
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



if __name__ == "__main__":
    env = TicTacToeEnv()
    state_size = (env.size, env.size)
    action_size = env.size * env.size
    agent = DQNAgent(state_size, action_size)
    batch_size = 32

    episodes = 10000 #Code có thể sửa, số lần train

    #Code có thể sửa
    for e in range(episodes):
        state = env.reset()
        done = False
        total_reward = 0
        isFirstMove = True

        while not done:
            #Lần đầu của Agent sẽ là random
            if isFirstMove:
                action = random.choice([i for i in range(action_size)])
                row, col = divmod(action, env.size)
            else:
                action = agent.act(state)

            #Tính điểm của action
            next_state, reward, done, _ = env.step(action)
            total_reward += reward
            agent.remember(state, action, reward, next_state, done)
            state = next_state

            #Nếu đi không hợp lệ thì không cho người chơi RANDOM đi
            if reward == -1: 
                continue

            #action mang giá trị 0 -> 224 nên cần đổi về dạng toạ độ (row, col)
            x, y = divmod(action, 15)

            #Agent's move
            env.board[x, y] = AGENT
            print("action", action, sep=" ")
            env.render()

            #Random ra vị trí trống trên bàn cờ
            available_random_move = False
            while not available_random_move:
                random_action = random.choice([i for i in range(action_size)])
                print("random action: ", random_action, sep=" ")
                a, b = divmod(random_action, 15)
                if env.board[a, b] == 0: #Vị trí trống mang giá trị 0
                    available_random_move = True
                    env.board[a, b] = RANDOM
            
            #In ra bàn cờ
            env.render()

            #In ra thông số
            #Code không nên sửa
            if done:
                agent.update_target_model()
                print(f"Episode: {e+1}/{episodes}, Score: {total_reward}, Epsilon: {agent.epsilon:.2}")
                print("X wins!") if env.evaluate() == 10 else print("O wins!")

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
    # agent._build_model.save_model("traint_agent.h5")