import random
from collections import deque
from typing import Deque
from typing import Tuple

import torch
from torch import nn

from constants import Action
from constants import LIST_TUPLE_INT_ACTION_ORDERED
from constants import TYPE_GAME_STATE
from constants import TYPE_TUPLE_INT_ACTION
from model import LinearQNet
from model import QTrainer

import numpy as np

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class AgentQLearning:
    amount_games: int

    def __init__(self):  # TODO: ADD INSTANCE VARS AS PARAMETERS
        self.amount_games: int = 0
        self.epsilon: float = 0  # randomness
        self.gamma: float = 0.9  # discount rate (Must be smaller than 1)
        self.deque_memory: Deque[Tuple[TYPE_GAME_STATE, Action, int, TYPE_GAME_STATE, bool]] = deque(maxlen=MAX_MEMORY)
        self.model: nn.Module = LinearQNet(11, 256, 3)
        self.trainer = QTrainer(self.model, learning_rate=LR, gamma=self.gamma)

    def remember(self, game_state: TYPE_GAME_STATE, action: Action, reward: int, game_state_next: TYPE_GAME_STATE,
                 done: bool):
        """
        Deque that stores the game game_state_current essentially and will pop old game states when more game states are added

        Notes:
            Used to train long memory
        """

        # popleft if MAX_MEMORY is reached
        self.deque_memory.append(
            (game_state, action, reward, game_state_next, done)
        )

    def train_long_memory(self):
        if len(self.deque_memory) > BATCH_SIZE:
            mini_sample = random.sample(self.deque_memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.deque_memory

        game_states, tuple_action, tuple_reward, game_states_next, tuple_bool_player_dead = zip(*mini_sample)

        np_ndarray_game_states = np.array(game_states)
        np_ndarray_game_states_next = np.array(game_states_next)

        self.trainer.train_step_input_multiple(
            np_ndarray_game_states,
            tuple_action,
            tuple_reward,
            np_ndarray_game_states_next,
            tuple_bool_player_dead
        )

        # for game_state_current, torch_tensor_action, torch_tensor_reward, nexrt_state, sequence_bool_player_dead in mini_sample:
        #    self.trainer.train_step_input_single(game_state_current, torch_tensor_action, torch_tensor_reward, torch_tensor_game_states_next, sequence_bool_player_dead)

    def train_short_memory(self,
                           game_state: TYPE_GAME_STATE,
                           action: Action,
                           reward: int,
                           game_state_next: TYPE_GAME_STATE,
                           done: bool
                           ):

        self.trainer.train_step_input_single(game_state, action, reward, game_state_next, done)

    def get_tuple_int_action_relative(self, game_state: TYPE_GAME_STATE) -> TYPE_TUPLE_INT_ACTION:
        """

        Notes:
            More games leads to smaller epsilon which leads to more exploitation

        :param game_state:
        :return:
        """
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.amount_games

        if random.randint(0, 200) < self.epsilon:  # Exploration
            tuple_int_action = random.choice(LIST_TUPLE_INT_ACTION_ORDERED)

        else:  # Exploitation
            state0 = torch.tensor(game_state, dtype=torch.float)
            prediction = self.model(state0)  # Prediction (tensorflow would be model.predict)

            index_move = torch.argmax(prediction).item()

            tuple_int_action = LIST_TUPLE_INT_ACTION_ORDERED[index_move]

        return tuple_int_action  # FIXME FIGURE OUT TYPE LATER IDK
