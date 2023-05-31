"""
Date created: 4/27/2023

Purpose:

Details:

Description:

Notes:

IMPORTANT NOTES:

Explanation:

Tags:

Contributors: 
    https://github.com/josephedradan
    
Reference:

"""
from abc import ABC
from abc import abstractmethod
from typing import Union

from util import TYPE_ACTION_POSSIBLE
from util import Action


class Player(ABC):
    action: TYPE_ACTION_POSSIBLE

    def __init__(self, action_initial: TYPE_ACTION_POSSIBLE = None):
        self.action = action_initial

    def set_action(self, action: TYPE_ACTION_POSSIBLE):
        self.action = action

    def get_action_current(self) -> TYPE_ACTION_POSSIBLE:
        return self.action

    @abstractmethod
    def get_action_new(self) -> TYPE_ACTION_POSSIBLE:
        ...

    # def reset(self, action_initial: Action, x_initial: int, y_initial: int):
    #     # init game_snake state
    #     self.action_current = action_initial
    #
    #     self.head = Chunk(x_initial, y_initial)
    #
    #     self.list_point_snake = [
    #         self.head,
    #         Chunk(self.head.x - BLOCK_SIZE, self.head.y),
    #         Chunk(self.head.x - (2 * BLOCK_SIZE), self.head.y)
    #     ]
    #
    #     # self.score = 0
    #     # self.chunk_food = None
    #     # self._place_food()
    #     # self.index_frame = 0
