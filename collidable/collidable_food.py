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
from collidable.collidable import Collidable
from collidable.collidable import TYPEVAR_CONTAINER_CHUNK
from container_chunk.container_chunk import ContainerChunk


class CollidableFood(Collidable[TYPEVAR_CONTAINER_CHUNK]):

    def __init__(self,
                 iterable_chunk: Union[Iterable[Chunk], None] = None
                 ):
        super().__init__(
            ContainerChunk(
                iterable_chunk
            )
        )
