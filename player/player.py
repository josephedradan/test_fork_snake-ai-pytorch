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
from typing import Sequence
from typing import Union

from chunk import Chunk
from constants import TYPE_ACTION_POSSIBLE
from singleton_data.singleton_data_game import SingletonDataGame
from singleton_data.singleton_data_player import SingletonDataPlayer
from wrapper.wrapper import Wrapper


class Player(ABC):
    wrapper: Wrapper
    action: TYPE_ACTION_POSSIBLE

    score: int

    def __init__(self, wrapper: Wrapper, action_initial: TYPE_ACTION_POSSIBLE = None):
        """
        :param action_initial: Starting action (direction) the player will have
        """

        self.wrapper = wrapper
        self.action = action_initial

        self.score = 0

    def set_action(self, action: TYPE_ACTION_POSSIBLE):
        self.action = action

    def get_action_current(self) -> TYPE_ACTION_POSSIBLE:
        return self.action

    def get_wrapper(self) -> Wrapper:
        return self.wrapper

    def send_feedback_play_step(self,
                                singleton_data_game: SingletonDataGame,
                                singleton_data_player: SingletonDataPlayer,
                                ):
        """
        Essentially a callback that receives feedback after a play step has happened

        Notes:
            This method is used for subclasses that do post analysis such as AI agents

        :param singleton_data_player:
        :param singleton_data_game:
        :return:
        """
        pass

    @abstractmethod
    def get_action_new(self, singleton_data_game: SingletonDataGame) -> TYPE_ACTION_POSSIBLE:
        """
        It is up to the subclasses to figure out what to do with LogicGameSnake because
        subclasses might interpret the LogicGameSnake differently.

        Notes:
            You probably want to make a game game_state_current of some kind given LogicGameSnake

        :param singleton_data_game:
        :return:
        """
        ...

    def reset(self,
              action_initial: TYPE_ACTION_POSSIBLE,
              chunk_initial: Chunk,
              iterable_chunk_additional: Union[Sequence[Chunk], None] = None
              ):
        self.set_action(action_initial)
        self.score = 0

        self.wrapper.reset([chunk_initial, *iterable_chunk_additional])

    # def reset(self, action_initial: Action, x_initial: int, y_initial: int):
    #     # init game_snake game_state_current
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
