"""
Date created: 6/26/2023

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
import itertools
from collections import deque
from typing import Iterable
from typing import Set
from typing import Union

import numpy as np

from chunk import Chunk
from constants import Action
from constants import DICT_K_ACTION_V_INDEX_ACTION_CYCLE_CLOCKWISE
from constants import LIST_ACTION_CYCLE_CLOCKWISE
from constants import T
from constants import TUPLE_INT_ACTION_LEFT
from constants import TUPLE_INT_ACTION_RIGHT
from constants import TUPLE_INT_ACTION_FORWARD
from constants import TYPE_ACTION_POSSIBLE
from constants import TYPE_TUPLE_INT_ACTION
from data.data_game import DataGame
from wrapper.wrapper import Wrapper


def get_wrapper_from_chunk_that_collided(data_game: DataGame, chunk: Chunk) -> Union[Wrapper, None]:
    """
    Notes:
        If chunk collided with a wrapper, return that wrapper

    :param data_game:
    :param chunk:
    :return:
    """
    wrapper: Wrapper
    for wrapper in itertools.chain(data_game.list_wrapper_snake,
                                   data_game.list_wrapper_food,
                                   data_game.list_wrapper_wall):
        if chunk in wrapper.get_container_chunk():
            return wrapper

    return None


def get_bool_wrapper_from_chunk_that_collided(data_game: DataGame, chunk: Chunk) -> bool:
    return True if get_wrapper_from_chunk_that_collided(data_game, chunk) else False


def get_action_from_tuple_int_action_relative(action: Action,
                                              tuple_int_action_relative: TYPE_TUPLE_INT_ACTION) -> TYPE_ACTION_POSSIBLE:
    """

    Notes:
        Convert Action to be based on

    :param action:
    :param tuple_int_action_relative:
    :return:
    """
    index_action_cycle_clockwise = DICT_K_ACTION_V_INDEX_ACTION_CYCLE_CLOCKWISE.get(action)

    if index_action_cycle_clockwise is None:
        return action

    if np.array_equal(tuple_int_action_relative, TUPLE_INT_ACTION_FORWARD):
        # Action is the same so no change is needed
        # torch_tensor_action = LIST_ACTION_CYCLE_CLOCKWISE[index_action_cycle_clockwise]
        pass

    elif np.array_equal(tuple_int_action_relative, TUPLE_INT_ACTION_RIGHT):
        next_idx = (index_action_cycle_clockwise + 1) % 4

        # Action will turn right relative to current Action (r -> d -> l -> u)
        action = LIST_ACTION_CYCLE_CLOCKWISE[next_idx]

    elif np.array_equal(tuple_int_action_relative, TUPLE_INT_ACTION_LEFT):  # [0, 0, 1]
        next_idx = (index_action_cycle_clockwise - 1) % 4

        # Action will turn left relative to current Action (r -> u -> l -> d)
        action = LIST_ACTION_CYCLE_CLOCKWISE[next_idx]

    return action


class DequeFastLookUp(deque[T]):
    """

    Notes:
        Since self.set_ uses hashing, if an object is added to this object
        then the object added to self.set_ will be overwritten
    """
    set_: Set[T]

    def __init__(self, iterable: Iterable, maxlen: Union[int, None] = None):
        super().__init__(iterable, maxlen)

        self.set_ = set()

        self.set_.update(iterable)

    def append(self, x: T) -> None:
        super().append(x)
        self.set_.add(x)

    def appendleft(self, x: T) -> None:
        super().appendleft(x)
        self.set_.add(x)

    def copy(self) -> deque[[T]]:
        return DequeFastLookUp(self)

    def clear(self) -> None:
        super().clear()
        self.set_.clear()

    def extend(self, iterable: Iterable[T]) -> None:
        super().extend(iterable)
        self.set_.update(iterable)

    def extendleft(self, iterable: Iterable[T]) -> None:
        super().extendleft(iterable)
        self.set_.update(iterable)

    def insert(self, i: int, x: T) -> None:
        super().insert(i, x)
        self.set_.update(x)

    def pop(self) -> T:
        self.set_.pop()
        return super(DequeFastLookUp, self).pop()

    def popleft(self) -> T:
        self.set_.pop()
        return super(DequeFastLookUp, self).popleft()

    def __contains__(self, item: T):
        return item in self.set_
