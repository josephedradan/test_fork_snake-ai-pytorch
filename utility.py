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
from __future__ import annotations

import itertools
from collections import deque
from typing import Iterable
from typing import List
from typing import Set
from typing import TYPE_CHECKING
from typing import Union

import numpy as np

from _settings import Settings
from chunk import Chunk
from constants import Action
from constants import DICT_K_ACTION_V_ACTION_REVERSE
from constants import DICT_K_ACTION_V_INDEX_ACTION_CYCLE_CLOCKWISE
from constants import LIST_ACTION_CYCLE_CLOCKWISE
from constants import TUPLE_INT_ACTION_FORWARD
from constants import TUPLE_INT_ACTION_LEFT
from constants import TUPLE_INT_ACTION_RIGHT
from constants import TYPEVAR_ANY
from constants import TYPE_ACTION_POSSIBLE
from constants import TYPE_TUPLE_INT_ACTION

if TYPE_CHECKING:
    from data.data_game import DataGame
    from logic_game_snake import LogicGameSnake
    from player.player import Player
    from wrapper.wrapper import Wrapper
    from wrapper.wrapper_snake import WrapperSnake


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

    elif np.array_equal(tuple_int_action_relative, TUPLE_INT_ACTION_LEFT):  # (0, 0, 1)
        next_idx = (index_action_cycle_clockwise - 1) % 4

        # Action will turn left relative to current Action (r -> u -> l -> d)
        action = LIST_ACTION_CYCLE_CLOCKWISE[next_idx]

    return action


def initialize_easy_player_wrapper_snake(
        settings: Settings,
        logic_game_snake: LogicGameSnake,
        player_wrapper_snake: Player[WrapperSnake],
        action_initial: Action,
        amount_chunk_to_add: int) -> None:
    """
    You can only call this once a game is created but not ran

    :param settings:
    :param logic_game_snake:
    :param player_wrapper_snake:
    :param action_initial:
    :param amount_chunk_to_add:
    :return:
    """

    dict_k_action_v_position_delta = {
        Action.RIGHT: (settings.block_size, 0),
        Action.LEFT: (-settings.block_size, 0),
        Action.UP: (0, settings.block_size),
        Action.DOWN: (0, -settings.block_size),

    }

    player_wrapper_snake.set_action(action_initial)

    chunk_selected = player_wrapper_snake.get_wrapper().get_container_chunk().get_chunk_first()

    list_chunk_new: List[Chunk] = []

    for index in range(amount_chunk_to_add):

        action_reverse = DICT_K_ACTION_V_ACTION_REVERSE.get(action_initial)

        position_delta = dict_k_action_v_position_delta.get(action_reverse)

        chunk_new = Chunk(
            chunk_selected.x + position_delta[0],
            chunk_selected.y + position_delta[1]
        )

        # Check if placement of chunk is valid
        if (get_bool_wrapper_from_chunk_that_collided(logic_game_snake.data_game, chunk_new) and
                chunk_new not in list_chunk_new):

            list_chunk_new.append(chunk_new)
            chunk_selected = chunk_new

        # Fallback, use an alternative position_delta
        else:
            for action, position_delta in dict_k_action_v_position_delta.items():
                if action == action_initial:  # Skip already tried action
                    continue

                chunk_new.x = position_delta[0]
                chunk_new.y = position_delta[1]

                if (get_bool_wrapper_from_chunk_that_collided(
                        logic_game_snake.data_game,chunk_new) and
                        chunk_new not in list_chunk_new):
                    list_chunk_new.append(chunk_new)
                    chunk_selected = chunk_new
                    break

    for chunk_new in list_chunk_new:
        player_wrapper_snake.get_wrapper().get_container_chunk().add_new_chunk(chunk_new)


class DequeFastLookUp(deque[TYPEVAR_ANY]):
    """

    Notes:
        Since self.set_ uses hashing, if an object is added to this object
        then the object added to self.set_ will be overwritten
    """
    set_: Set[TYPEVAR_ANY]

    def __init__(self, iterable: Iterable, maxlen: Union[int, None] = None):
        super().__init__(iterable, maxlen)

        self.set_ = set()

        self.set_.update(iterable)

    def append(self, x: TYPEVAR_ANY) -> None:
        super().append(x)
        self.set_.add(x)

    def appendleft(self, x: TYPEVAR_ANY) -> None:
        super().appendleft(x)
        self.set_.add(x)

    def copy(self) -> deque[[TYPEVAR_ANY]]:
        return DequeFastLookUp(self)

    def clear(self) -> None:
        super().clear()
        self.set_.clear()

    def extend(self, iterable: Iterable[TYPEVAR_ANY]) -> None:
        super().extend(iterable)
        self.set_.update(iterable)

    def extendleft(self, iterable: Iterable[TYPEVAR_ANY]) -> None:
        super().extendleft(iterable)
        self.set_.update(iterable)

    def insert(self, i: int, x: TYPEVAR_ANY) -> None:
        super().insert(i, x)
        self.set_.update(x)

    def pop(self) -> TYPEVAR_ANY:
        self.set_.pop()
        return super(DequeFastLookUp, self).pop()

    def popleft(self) -> TYPEVAR_ANY:
        self.set_.pop()
        return super(DequeFastLookUp, self).popleft()

    def __contains__(self, item: TYPEVAR_ANY):
        return item in self.set_
