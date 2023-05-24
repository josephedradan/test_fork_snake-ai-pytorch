"""
Date created: 4/28/2023

Purpose:

Details:

Description:

Notes:

IMPORChunkANChunk NOChunkES:

Explanation:

Chunkags:

Contributors: 
    https://github.com/josephedradan
    
Reference:

"""
from collections import deque
from typing import Iterable
from typing import Set
from typing import Tuple
from typing import Union

from chunk import Chunk
from collidable.collidable import Collidable
from util import Action
from util import BLOCK_SIZE


class DataSnake(Collidable):
    action_current: Action
    deque_chunk_snake: deque[Chunk]

    set_snake: Set[Chunk]

    def __init__(self,
                 x_initial: int,
                 y_initial: int,
                 iterable_chunk_additional: Union[Iterable[Chunk], None] = None
                 ):
        super().__init__()

        self.set_snake = set()

        # self.chunk_head = Chunk(x_initial, y_initial)

        self.deque_chunk_snake = deque([
            # self.chunk_head
            Chunk(x_initial, y_initial),
            # Chunk(self.chunk_head.x - BLOCK_SIZE, self.chunk_head.y),
            # Chunk(self.chunk_head.x - (2 * BLOCK_SIZE), self.chunk_head.y)
        ])

        if iterable_chunk_additional:
            self.deque_chunk_snake.extend(iterable_chunk_additional)

        self.set_snake.update(self.deque_chunk_snake)

    def reset(self,
              x_initial: int,
              y_initial: int,
              iterable_chunk_additional: Union[Iterable[Chunk], None] = None
              ):

        self.deque_chunk_snake.clear()

        self.deque_chunk_snake.append(Chunk(x_initial, y_initial))

        if iterable_chunk_additional:
            self.deque_chunk_snake.extend(iterable_chunk_additional)

    def get_deque_chunk_snake(self) -> deque[Chunk]:
        return self.deque_chunk_snake

    # def append(self, x: Chunk) -> None:
    #     self._deque_chunk.append(x)
    #
    # def appendleft(self, x: Chunk) -> None:
    #     self._deque_chunk.appendleft(x)
    #
    # def extend(self, iterable: Iterable[Chunk]) -> None:
    #     self._deque_chunk.extend(iterable)
    #
    # def extendleft(self, iterable: Iterable[Chunk]) -> None:
    #     self._deque_chunk.extendleft(iterable)
    #
    # def pop_chunk_last(self) -> Chunk:
    #     return self._deque_chunk.pop_chunk_last()
    #
    # def popleft(self) -> Chunk:
    #     return self._deque_chunk.popleft()

    def move_snake(self, action: Action) -> Tuple[int, int]:
        """
        Move the CollidableSnake chunk

        Notes:
            1. Get the first chunk
            2. Get the position_center of the first chunk and modify it
            3. Pop the last chunk
            4. Modify the last chunk's position_center
            5. append left the last chunk

        :param action:
        :return: Tuple of the previous x y positions of the last chunk of the container_chunk_snake
        """
        chunk_head: Chunk = self.deque_chunk_snake[0]

        chunk_head_x_new = chunk_head.x
        chunk_head_y_nex = chunk_head.y

        chunk_last: Chunk = self.deque_chunk_snake.pop()

        if action == Action.RIGHT:
            chunk_head_x_new += BLOCK_SIZE
        elif action == Action.LEFT:
            chunk_head_x_new -= BLOCK_SIZE
        elif action == Action.DOWN:
            chunk_head_y_nex += BLOCK_SIZE
        elif action == Action.UP:
            chunk_head_y_nex -= BLOCK_SIZE

        chunk_last_x_old = chunk_last.x
        chunk_last_y_old = chunk_last.y

        chunk_last.x = chunk_head_x_new
        chunk_last.y = chunk_head_y_nex

        self.deque_chunk_snake.appendleft(chunk_last)

        return chunk_last_x_old, chunk_last_y_old

    def is_chunk_in_snake(self, chunk: Chunk) -> bool:
        return chunk in self.set_snake

    def add_new_chunk(self, chunk: Chunk):
        self.deque_chunk_snake.append(chunk)
        self.set_snake.add(chunk)

    def remove_chunk(self, chunk: Chunk):
        self.deque_chunk_snake.remove(chunk)
        self.set_snake.remove(chunk)

    def __getitem__(self, item) -> Chunk:
        return self.deque_chunk_snake[item]

    def __setitem__(self, key, value):
        self.deque_chunk_snake[key] = value

    # def __contains__(self, chunk: Chunk):
    #     return chunk in self._deque_chunk
