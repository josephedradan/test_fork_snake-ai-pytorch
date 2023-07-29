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
from typing import Generic
from typing import Union

from constants import TYPEVAR_WRAPPER
from constants import TYPE_ACTION_POSSIBLE
from data.data_game import DataGame
from data.data_play_step_result import DataPlayStepResult
from data.data_player import DataPlayer
from wrapper.wrapper import Wrapper


class Player(ABC, Generic[TYPEVAR_WRAPPER]):
    wrapper: Union[Wrapper, None]
    action: TYPE_ACTION_POSSIBLE

    data_player: DataPlayer

    def __init__(self):
        """
        """

        self.wrapper = None
        self.action = None

        self.data_player = DataPlayer()

    def get_data_player(self) -> DataPlayer:
        return self.data_player

    def set_action(self, action: TYPE_ACTION_POSSIBLE):
        self.action = action

    def get_action(self) -> TYPE_ACTION_POSSIBLE:
        return self.action

    def set_wrapper(self, wrapper: TYPEVAR_WRAPPER):
        self.wrapper = wrapper

    def get_wrapper(self) -> TYPEVAR_WRAPPER:
        return self.wrapper

    def receive_feedback_of_step(self,
                                 data_game: DataGame,
                                 data_player: DataPlayStepResult,
                                 ):
        """
        Essentially a callback that receives feedback after a play step has happened

        Notes:
            This method is used for subclasses that do post analysis such as AI agents

        :param data_player:
        :param data_game:
        :return:
        """
        pass

    @abstractmethod
    def get_action_new(self, data_game: DataGame) -> TYPE_ACTION_POSSIBLE:
        """
        It is up to the subclasses to figure out what to do with LogicGameSnake because
        subclasses might interpret the LogicGameSnake differently.

        Notes:
            You probably want to make a game game_state of some kind given LogicGameSnake

        :param data_game:
        :return:
        """
        ...

    # def reset(self,
    #           action_initial: TYPE_ACTION_POSSIBLE = None,
    #           chunk_initial: Union[Chunk, None] = None,
    #           iterable_chunk_additional: Union[Sequence[Chunk], None] = None
    #           ):
    #     self.set_action(action_initial)
    #
    #     if self.wrapper is not None:
    #         self.wrapper.reset([chunk_initial, *iterable_chunk_additional])
    #
    #     self.score = 0

    # def _initialize(self, action_initial: Action, x_initial: int, y_initial: int):
    #     # init logic_game_snake game_state
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
    #     # self.counter_play_step_since_last_food = 0
