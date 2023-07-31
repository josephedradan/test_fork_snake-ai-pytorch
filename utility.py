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
from typing import Sequence
from typing import Set
from typing import TYPE_CHECKING
from typing import Tuple
from typing import Type
from typing import Union
from typing import get_type_hints

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
from constants import TYPE_NP_NDARRAY_GAME_STATE_GENERIC
from constants import TYPE_TUPLE_INT_ACTION
from game_state.generator_game_state import GeneratorGameState

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


def get_chunk_possible_from_wrappers(list_wrapper: Sequence[Wrapper]) -> Union[Chunk, None]:
    if list_wrapper:
        wrapper_food_arbitrary = list_wrapper[0]

        container_chunk_food = wrapper_food_arbitrary.get_container_chunk()

        _dict_k_chunk_v_chunk = container_chunk_food.get_dict_k_chunk_v_chunk()

        try:
            return container_chunk_food.get_chunk_first()

        except IndexError as e:
            pass

    return None


def initialize_easy_player_wrapper_snake(
        settings: Settings,
        logic_game_snake: LogicGameSnake,
        player_wrapper_snake: Player[WrapperSnake],
        action_initial: Action,
        amount_chunk_to_add: int) -> None:
    """
    You can only call this once a game is created but not ran

    Notes:
        This will:
            1. Get the snake position
            2. Get snake direction (Action)
            3. Add new chunks to the snake that a valid and will most likely not collide with the snake
            going in its initial direction (Action)

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

    chunk_current = player_wrapper_snake.get_wrapper().get_container_chunk().get_chunk_first()

    action_reverse = DICT_K_ACTION_V_ACTION_REVERSE.get(action_initial)

    list_action = list(dict_k_action_v_position_delta.keys())
    list_position_delta = list(dict_k_action_v_position_delta.values())

    index_action_reverse = list_action.index(action_reverse)

    list_chunk_new_to_add: List[Chunk] = []

    for _index in range(amount_chunk_to_add):

        for index_selected in range(len(list_position_delta)):
            index_selected_corrected = (index_action_reverse + index_selected) % len(list_position_delta)

            position_delta = list_position_delta[index_selected_corrected]

            chunk_new = Chunk(
                chunk_current.x + position_delta[0],
                chunk_current.y + position_delta[1]
            )

            # Check if placement of chunk is valid
            if not (get_bool_wrapper_from_chunk_that_collided(logic_game_snake.data_game, chunk_new) and
                    chunk_new not in list_chunk_new_to_add):
                list_chunk_new_to_add.append(chunk_new)

                # Set chunk to extend onto
                chunk_current = chunk_new
                break

    # Add new chunks to snake
    for chunk_new in list_chunk_new_to_add:
        player_wrapper_snake.get_wrapper().get_container_chunk().add_new_chunk(chunk_new)


"""
####################
Meta python stuff
####################
"""


def get_type_return_from_generator_game_state(
        class_generator_game_state: Type[GeneratorGameState]) -> TYPE_NP_NDARRAY_GAME_STATE_GENERIC:
    """
    Get the return type from a GeneratorGameState.get_game_state call

    :param class_generator_game_state:
    :return:
    """
    dict_k_key_v_type = get_type_hints(
        class_generator_game_state.get_game_state,
        include_extras=True  # Will capture the full typing.Annotated type
    )

    type_return = dict_k_key_v_type.get("return")

    return type_return


def get_shape_from_generator_game_state(class_generator_game_state: Type[GeneratorGameState]) -> Tuple[int, ...]:
    """
    This is used to get the return shape of a GeneratorGameState.get_game_state call.
    The shape returned is the shape of the np.ndarray object as a tuple.
    The result of this callable is probably used as an arg in a neural network's input layer so the model can
    work properly.

    Note that if the return type of a GeneratorGameState.get_game_state call does not match what is actually
    returned from that callable, then its possible that crash may occur.

    Reference:
        What is the right way to check if a type hint is annotated?
            Notes:
                using typing.get_type_hints how to show Annotated
            Reference:
                https://stackoverflow.com/questions/68275615/what-is-the-right-way-to-check-if-a-type-hint-is-annotated

                typing.get_type_hints(obj, globalns=None, localns=None, include_extras=False)
                    Reference:
                        https://docs.python.org/3/library/typing.html#typing.get_type_hints

    :param class_generator_game_state:
    :return:
    """

    type_return = get_type_return_from_generator_game_state(class_generator_game_state)

    shape = type_return.__dict__.get("__metadata__")[0].__dict__.get("__args__")

    return shape


"""
####################
Miscellaneous
####################
"""


class DequeSet(deque[TYPEVAR_ANY]):
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
        return DequeSet(self)

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
        return super(DequeSet, self).pop()

    def popleft(self) -> TYPEVAR_ANY:
        self.set_.pop()
        return super(DequeSet, self).popleft()

    def __contains__(self, item: TYPEVAR_ANY):
        return item in self.set_
