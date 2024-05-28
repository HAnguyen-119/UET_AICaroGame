import os
import tensorflow as tf

from tensorflow import keras
from DQNAgent import DQNAgent
from Env import TicTacToeEnv


if __name__ == '__main__':
  env = TicTacToeEnv()
  agent = DQNAgent((15, 15), 225)

  model = agent._build_model()
  model.save('./save/model.h5')

  



