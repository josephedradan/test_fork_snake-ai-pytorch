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
from typing import Sequence
from typing import Union

from chunk import Chunk
from collidable.collidable import Collidable
from container_chunk.container_chunk_snake import ContainerChunkSnake
from player import Player
from util import Action


class CollidableSnake(Collidable[ContainerChunkSnake]):
    player: Player
    score: int

    def __init__(self,
                 player: Player,
                 iterable_chunk: Union[Iterable[Chunk], None] = None
                 ):
        """
        :param player:
        :param iterable_chunk:
        """
        super().__init__(
            ContainerChunkSnake(
                iterable_chunk
            )
        )

        self.player = player

        self.score = 0

    def reset_snake(self,
                    action_initial: Action,
                    chunk_initial: Chunk,
                    iterable_chunk_additional: Union[Sequence[Chunk], None] = None
                    ):
        super().reset([chunk_initial, *iterable_chunk_additional])

        self.player.set_action(action_initial)

        self.score = 0

    def get_player(self) -> Player:
        return self.player
