"""
Date created: 5/2/2023

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
from collections import deque
from typing import Iterable
from typing import Union

from chunk import Chunk
from container_chunk.container_chunk import ContainerChunk


class ContainerChunkSnake(ContainerChunk):

    def __init__(self,
                 iterable_chunk: Union[Iterable[Chunk], None] = None
                 ):
        super().__init__(iterable_chunk)

        # self._deque_chunk = deque([
        #     chunk_initial,
        #     # Chunk(self.chunk_head.x - BLOCK_SIZE, self.chunk_head.y),
        #     # Chunk(self.chunk_head.x - (2 * BLOCK_SIZE), self.chunk_head.y)
        # ])

        self._deque_chunk = deque()

        if iterable_chunk:
            self._deque_chunk.extend(iterable_chunk)

    def reset(self, iterable_chunk: Union[Iterable[Chunk], None] = None):
        super(ContainerChunkSnake, self).reset(iterable_chunk)
        self._deque_chunk.clear()

    def add_new_chunk(self, chunk: Chunk):
        super(ContainerChunkSnake, self).add_new_chunk(chunk)
        self._deque_chunk.append(chunk)

    def add_new_chunk_front(self, chunk: Chunk):
        super(ContainerChunkSnake, self).add_new_chunk(chunk)
        self._deque_chunk.appendleft(chunk)

    def remove_chunk(self, chunk: Chunk):
        super(ContainerChunkSnake, self).remove_chunk(chunk)
        self._deque_chunk.remove(chunk)

    def get_chunk_first(self) -> Chunk:
        return self._deque_chunk[0]

    def pop_chunk_last(self) -> Chunk:
        chunk_popped = self._deque_chunk.pop()
        self._dict_k_chunk_v_chunk.pop(chunk_popped)
        return chunk_popped

    def __getitem__(self, item: int) -> Chunk:
        return self._deque_chunk[item]

    def __setitem__(self, key: int, value: Chunk):
        self._deque_chunk[key] = value

    def __iter__(self):
        return self._deque_chunk.__iter__()

    def __str__(self):
        return f"{type(self).__name__}"
