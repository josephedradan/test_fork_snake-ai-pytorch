"""
Date created: 5/5/2023

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


class ContainerChunkWall(ContainerChunk):

    def __init__(self, iterable_chunk: Union[Iterable[Chunk], None] = None):
        super().__init__(iterable_chunk)


