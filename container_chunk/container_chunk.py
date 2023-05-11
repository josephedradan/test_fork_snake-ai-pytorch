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
from typing import Dict
from typing import Iterable
from typing import Union

from chunk import Chunk


class ContainerChunk:
    _dict_k_chunk_v_chunk: Dict[Chunk, Chunk]

    def __init__(self,
                 iterable_chunk: Union[Iterable[Chunk], None] = None
                 ):
        """
        Do not call self.reset(...) here because

        Notes:
            Recall that python dictionaries past 3.6 are ordered by insertion

        :param chunk_initial:
        :param iterable_chunk:
        """
        self._dict_k_chunk_v_chunk = {}

        # self.reset(chunk_initial, iterable_chunk)  # Don't call this

        if isinstance(iterable_chunk, Iterable):
            self._dict_k_chunk_v_chunk.update(zip(iterable_chunk,
                                                  iterable_chunk))

    def add_new_chunk(self, chunk: Chunk):
        self._dict_k_chunk_v_chunk[chunk] = chunk

    def remove_chunk(self, chunk: Chunk) -> Chunk:
        return self._dict_k_chunk_v_chunk.pop(chunk)

    def reset(self, iterable_chunk_additional: Union[Iterable[Chunk], None] = None):
        self._dict_k_chunk_v_chunk.clear()

        if isinstance(iterable_chunk_additional, Iterable):
            self._dict_k_chunk_v_chunk.update(zip(iterable_chunk_additional,
                                                  iterable_chunk_additional))

    def __contains__(self, chunk: Chunk):
        return chunk in self._dict_k_chunk_v_chunk

    def __iter__(self):
        return self._dict_k_chunk_v_chunk.__iter__()

    def __len__(self):
        return self._dict_k_chunk_v_chunk.__len__()