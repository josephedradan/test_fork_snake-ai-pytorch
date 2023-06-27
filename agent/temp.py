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
from singleton_data.singleton_data_game import SingletonDataGame
from wrapper.wrapper import Wrapper


def get_wrapper_from_chunk_that_collided(singleton_data_game: SingletonDataGame, chunk: Chunk) -> Union[Wrapper, None]:
    """
    Notes:
        If chunk collided with a wrapper, return that wrapper

    :param singleton_data_game:
    :param chunk:
    :return:
    """
    wrapper: Wrapper
    for wrapper in itertools.chain(singleton_data_game.list_wrapper_snake,
                                   singleton_data_game.list_wrapper_food,
                                   singleton_data_game.list_wrapper_wall):
        if chunk in wrapper.get_container_chunk():
            return wrapper

    return None
