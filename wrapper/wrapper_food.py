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
from typing import Iterable
from typing import Union

from chunk import Chunk
from wrapper.wrapper import Wrapper
from wrapper.wrapper import TYPEVAR_CONTAINER_CHUNK
from container_chunk.container_chunk import ContainerChunk


class WrapperFood(Wrapper[TYPEVAR_CONTAINER_CHUNK]):

    def __init__(self,
                 iterable_chunk: Union[Iterable[Chunk], None] = None
                 ):
        super().__init__(
            ContainerChunk(
                iterable_chunk
            )
        )
