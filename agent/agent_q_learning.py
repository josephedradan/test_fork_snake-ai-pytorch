import random
from collections import deque
from typing import Deque
from typing import List
from typing import Tuple

import numpy as np
import torch
from torch import nn

from constants import LIST_TUPLE_INT_ACTION_ORDERED
from constants import TYPE_GAME_STATE
from constants import TYPE_TUPLE_INT_ACTION
from model import LinearQNet
from model import QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class AgentQLearning:
    amount_games: int

    def __init__(self):  # TODO: ADD INSTANCE VARS AS PARAMETERS
        self.amount_games: int = 0
        self.epsilon: float = 0  # randomness
        self.gamma: float = 0.9  # discount rate (Must be smaller than 1)
        self.deque_memory: Deque[Tuple[TYPE_GAME_STATE, TYPE_TUPLE_INT_ACTION, int, TYPE_GAME_STATE, bool]] = (
            deque(maxlen=MAX_MEMORY)
        )

        self.model: nn.Module = LinearQNet(11, 256, 3)  # FIXME MODEL INPUT MAKE IT DYNAMIC
        self.trainer = QTrainer(self.model, learning_rate=LR, gamma=self.gamma)

    def remember(self,
                 game_state: TYPE_GAME_STATE,
                 action: TYPE_TUPLE_INT_ACTION,
                 reward: int,
                 game_state_next: TYPE_GAME_STATE,
                 done: bool):
        """
        Deque that stores the game game_state essentially and will pop old game states when more game states
        are added

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

        list_game_state: List[TYPE_GAME_STATE]
        list_tuple_int_action: List[TYPE_TUPLE_INT_ACTION]
        list_reward: List[int]
        list_game_states_next: List[TYPE_GAME_STATE]
        list_tuple_bool_player_dead: List[bool]

        list_game_state, list_tuple_int_action, list_reward, list_game_states_next, list_tuple_bool_player_dead = (
            zip(*mini_sample)
        )

        np_ndarray_game_states = np.array(list_game_state)
        np_ndarray_game_states_next = np.array(list_game_states_next)

        # print("#" * 100)
        # print("states", list_game_state)
        # print("actions", list_tuple_int_action)
        # print("rewards", list_reward)
        # print("next_states", list_game_states_next)
        # print("dones", list_tuple_bool_player_dead)
        # print("#" * 100)

        self.trainer.train_step_input_multiple(
            np_ndarray_game_states,
            list_tuple_int_action,
            list_reward,
            np_ndarray_game_states_next,
            list_tuple_bool_player_dead
        )

        # for game_state, torch_tensor_action, torch_tensor_reward, nexrt_state, sequence_bool_player_dead in mini_sample:
        #    self.trainer.train_step_input_single(game_state, torch_tensor_action, torch_tensor_reward, torch_tensor_game_states_next, sequence_bool_player_dead)

    def train_short_memory(self,
                           game_state: TYPE_GAME_STATE,
                           tuple_int_action: TYPE_TUPLE_INT_ACTION,
                           reward: int,
                           game_state_next: TYPE_GAME_STATE,
                           done: bool
                           ):

        self.trainer.train_step_input_single(game_state, tuple_int_action, reward, game_state_next, done)

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
            torch_tensor_game_state = torch.tensor(game_state, dtype=torch.float)

            # Prediction (tensorflow would be model.predict)
            torch_tensor_action_prediction = self.model(torch_tensor_game_state)

            index_action_to_take = torch.argmax(torch_tensor_action_prediction).item()

            tuple_int_action = LIST_TUPLE_INT_ACTION_ORDERED[index_action_to_take]

        return tuple_int_action
