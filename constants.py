"""
Date created: 4/25/2023

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

from enum import IntEnum
from enum import auto
from typing import Callable
from typing import Dict
from typing import List
from typing import Tuple
from typing import TypeVar
from typing import Union

import numpy as np
import torch

from wrapper.wrapper import Wrapper

TYPE_TUPLE_INT_ACTION = Tuple[int, int, int]

TUPLE_INT_ACTION_FORWARD: TYPE_TUPLE_INT_ACTION = (1, 0, 0)
TUPLE_INT_ACTION_RIGHT: TYPE_TUPLE_INT_ACTION = (0, 1, 0)
TUPLE_INT_ACTION_LEFT: TYPE_TUPLE_INT_ACTION = (0, 0, 1)

LIST_TUPLE_INT_ACTION_ORDERED: List[TYPE_TUPLE_INT_ACTION] = [
    TUPLE_INT_ACTION_FORWARD,
    TUPLE_INT_ACTION_RIGHT,
    TUPLE_INT_ACTION_LEFT
]


class Action(IntEnum):
    RIGHT = auto()
    LEFT = auto()
    UP = auto()
    DOWN = auto()


LIST_ACTION_CYCLE_CLOCKWISE: List[Action] = [Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP]

DICT_K_ACTION_V_INDEX_ACTION_CYCLE_CLOCKWISE: Dict[Action, int] = {
    action: index for index, action in enumerate(LIST_ACTION_CYCLE_CLOCKWISE)
}

TYPE_ACTION_POSSIBLE = Union[Action, None]

DICT_K_ACTION_V_ACTION_REVERSE: Dict[Action, Action] = {
    Action.UP: Action.DOWN,
    Action.DOWN: Action.UP,
    Action.LEFT: Action.RIGHT,
    Action.RIGHT: Action.LEFT
}

TYPE_POSITION = Tuple[int, int]

TYPE_GAME_STATE = Union[Tuple[int, ...], np.ndarray, torch.Tensor]

TYPE_BOOL_SNAKE_DIED = bool
TYPE_WRAPPER_POSSIBLE = Union[Wrapper, None]
TYPE_CALLABLE_FOR_ITERATION_END = Callable[[TYPE_BOOL_SNAKE_DIED, TYPE_WRAPPER_POSSIBLE], None]


class ColorRGB(Tuple[int, int, int]):
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE_1 = (0, 0, 255)
    BLUE_2 = (0, 100, 255)
    BLACK = (0, 0, 0)
    GRAY = (168, 168, 168)
    GREEN = (0, 255, 0)
    GREEN_KELLY = (76, 187, 23)
    LIGHT_GOLDEN_ROD_YELLOW = (250, 250, 210)
    GOLD = (255, 215, 0)


class Condition(IntEnum):
    """
    Generic state container

    Notes:
        Basically when a boolean is not enough
    """
    STATE_1 = auto()
    STATE_2 = auto()
    STATE_3 = auto()


BLOCK_SIZE = 20
BLOCK_SIZE_OFFSET = 1
GAME_SPEED = 20

FONT_SIZE = 20
TEXT_LINE_SPACING_AMOUNT = FONT_SIZE + 5

T = TypeVar('T')
