import random
from collections import deque
from typing import Tuple

import torch

from constants import TYPE_TUPLE_ACTION_RELATIVE
from model import LinearQNet
from model import QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class AgentQLearning:
    amount_games: int

    def __init__(self):  # TODO: ADD INSTANCE VARS AS PARAMETERS
        self.amount_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate (Must be smaller than 1)
        self.deque_memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, learning_rate=LR, gamma=self.gamma)


    def remember(self, state, action, reward, next_state, done):
        """
        Deque that stores the game game_state_current essentially and will pop old game states when more game states are added

        Notes:
            Used to train long memory
        """
        self.deque_memory.append(
            (state, action, reward, next_state, done)
        )  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.deque_memory) > BATCH_SIZE:
            mini_sample = random.sample(self.deque_memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.deque_memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)

        self.trainer.train_step(states, actions, rewards, next_states, dones)

        # for game_state_current, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(game_state_current, action, reward, state_next, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_tuple_action_relative(self, game_state) -> TYPE_TUPLE_ACTION_RELATIVE:
        """

        Notes:
            More games leads to smaller epsilon which leads to more exploitation

        :param game_state:
        :return:
        """
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.amount_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:  # Exploration
            index_move = random.randint(0, 2)
            final_move[index_move] = 1

        else:  # Exploitation
            state0 = torch.tensor(game_state, dtype=torch.float)
            prediction = self.model(state0)  # Prediction (tensorflow would be model.predict)
            index_move = torch.argmax(prediction).item()

            final_move[index_move] = 1

        return final_move  # FIXME FIGURE OUT TYPE LATER IDK
