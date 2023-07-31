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

        Notes:
            Recall that python dictionaries past 3.6 are ordered by insertion.

        :param iterable_chunk:
        """

        """
        Notes:
            A dict is used instead of a set because the value of the dict is the chunk 
            in THIS object and the key is used for the hash of the chunk. Recall that the hash
            of the chunk uses the position of the chunk
        """
        self._dict_k_chunk_v_chunk = {}

        if isinstance(iterable_chunk, Iterable):
            self._dict_k_chunk_v_chunk.update(zip(iterable_chunk,
                                                  iterable_chunk))

    def add_new_chunk(self, chunk: Chunk):
        self._dict_k_chunk_v_chunk[chunk] = chunk

    def pop_chunk(self, chunk: Chunk) -> Chunk:
        """
        This will return the chunk of this object assuming that the given chunk has the same hash
        of the object that will be returned

        :param chunk:
        :return:
        """
        return self._dict_k_chunk_v_chunk.pop(chunk)

    def get_chunk_first(self) -> Chunk:
        """
        Get the the first chunk of this object

        Notes:
            This function should crash if there is no chunk

        :return:
        """

        # WARNING : Potentially slow if there are a lot of keys
        return self._dict_k_chunk_v_chunk[tuple(self._dict_k_chunk_v_chunk.keys())[0]]

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

    def get_dict_k_chunk_v_chunk(self) -> Dict[Chunk, Chunk]:
        return self._dict_k_chunk_v_chunk
