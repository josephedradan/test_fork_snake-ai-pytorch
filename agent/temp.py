"""
Date created: 6/26/2023

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
import itertools
from typing import Union

from chunk import Chunk
from agent.data.data_game import DataGame
from wrapper.wrapper import Wrapper


def get_wrapper_from_chunk_that_collided(data_game: DataGame, chunk: Chunk) -> Union[Wrapper, None]:
    """
    Notes:
        If chunk collided with a wrapper, return that wrapper

    :param data_game:
    :param chunk:
    :return:
    """
    wrapper: Wrapper
    for wrapper in itertools.chain(data_game.list_wrapper_snake,
                                   data_game.list_wrapper_food,
                                   data_game.list_wrapper_wall):
        if chunk in wrapper.get_container_chunk():
            return wrapper

    return None


def get_bool_wrapper_from_chunk_that_collided(data_game: DataGame, chunk: Chunk) -> bool:
    return True if get_wrapper_from_chunk_that_collided(data_game, chunk) else False
