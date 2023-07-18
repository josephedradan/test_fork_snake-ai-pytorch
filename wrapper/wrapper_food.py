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
from container_chunk.container_chunk import ContainerChunk
from container_chunk.container_chunk_food import ContainerChunkFood
from wrapper.wrapper import Wrapper


class WrapperFood(Wrapper[ContainerChunkFood]):

    def __init__(self,
                 iterable_chunk: Union[Iterable[Chunk], None] = None
                 ):
        super().__init__(
            ContainerChunk(
                iterable_chunk
            )
        )

