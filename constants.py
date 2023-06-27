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
import itertools
from collections import deque
from enum import Enum
from enum import auto
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Set
from typing import Tuple
from typing import TypeVar
from typing import Union
from typing import Union

from wrapper.wrapper import Wrapper
from wrapper.wrapper import Wrapper
from wrapper.wrapper import Wrapper


class Action(Enum):
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

TYPE_GAME_STATE = Tuple[int, ...]

TYPE_BOOL_SNAKE_DIED = bool
TYPE_WRAPPER_POSSIBLE = Union[Wrapper, None]
TYPE_CALLABLE_FOR_ITERATION_END = Callable[[TYPE_BOOL_SNAKE_DIED, TYPE_WRAPPER_POSSIBLE], None]

TYPE_TUPLE_ACTION_RELATIVE = Tuple[int, int, int]

class ColorRGB(Tuple[int, int, int]):
    WHITE = (255, 255, 255)
    RED = (200, 0, 0)
    BLUE_1 = (0, 0, 255)
    BLUE_2 = (0, 100, 255)
    BLACK = (0, 0, 0)
    GRAY = (168, 168, 168)
    GREEN = (0, 255, 0)
    GREEN_KELLY = (76, 187, 23)


BLOCK_SIZE = 20
BLOCK_SIZE_OFFSET = 1
FPS = 20

FONT_SIZE = 20
TEXT_LINE_SPACING_AMOUNT = FONT_SIZE + 5

T = TypeVar('T')


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


