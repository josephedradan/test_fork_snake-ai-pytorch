"""
Date created: 4/28/2023

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
from container_chunk.container_chunk_snake import ContainerChunkSnake
from wrapper.wrapper import Wrapper


class WrapperSnake(Wrapper[ContainerChunkSnake]):

    def __init__(self,
                 iterable_chunk: Union[Iterable[Chunk], None] = None
                 ):
        """
        :param player:
        :param iterable_chunk:
        """

        # WARNING: Doing operations before the super call is uncommon and illegal other languages
        container_chunk_snake = ContainerChunkSnake(iterable_chunk)

        super().__init__(
            container_chunk_snake
        )

    # def reset_snake(self,
    #                 chunk_initial: Chunk,
    #                 iterable_chunk_additional: Union[Sequence[Chunk], None] = None
    #                 ):
    #     super().reset([chunk_initial, *iterable_chunk_additional])
    #
    #     self.player.set_action(action_initial)

    # def get_player(self) -> Player:
    #     return self.player
