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
from typing import Union


class DataPlayer:
    """
    A lite container for player data stuff

    """
    bool_snake_died: Union[bool, None]
    wrapper_object_that_collided: Union[bool, None]
    reward: Union[int, None]

    def __init__(self):
        self.bool_snake_died = None
        self.wrapper_object_that_collided = None
        self.reward = None
