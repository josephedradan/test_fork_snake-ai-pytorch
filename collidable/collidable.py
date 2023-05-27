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
    class typing.TypeVar
        Notes:
            How to use TypeVar and what is bound=...

        Reference:
            https://docs.python.org/3/library/typing.html#typing.TypeVar

    Defining subclasses of generic classes
        Notes:
            Example of TypeVar

        Reference:
            https://mypy.readthedocs.io/en/stable/generics.html#defining-subclasses-of-generic-classes
"""
from abc import ABC
from typing import Generic
from typing import TypeVar

from container_chunk.container_chunk import ContainerChunk

TYPEVAR_CONTAINER_CHUNK = TypeVar('TYPEVAR_CONTAINER_CHUNK', bound=ContainerChunk)


class Collidable(ABC, Generic[TYPEVAR_CONTAINER_CHUNK]):
    """
    Wrapper around a ContainerChunk that stores additional information related to
    a ContainerChunk

    """
    container_chunk: ContainerChunk

    def __init__(self, container_chunk: ContainerChunk):
        self.container_chunk = container_chunk

    def get_container_chunk(self) -> TYPEVAR_CONTAINER_CHUNK:
        return self.container_chunk

    def reset(self, iterable_chunk_additional):
        self.container_chunk.reset(
            iterable_chunk_additional
        )
