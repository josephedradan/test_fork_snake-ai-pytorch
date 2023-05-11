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
from collidable.collidable import Collidable
from container_chunk.container_chunk_wall import ContainerChunkWall


class CollidableWall(Collidable[ContainerChunkWall]):
    def __init__(self, iterable_chunk_additional: Union[Iterable[Chunk], None] = None):
        super().__init__(ContainerChunkWall(
            iterable_chunk_additional
        ))
