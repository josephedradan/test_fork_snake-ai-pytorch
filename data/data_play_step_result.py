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

from data.data import Data


class DataPlayStepResult(Data):
    """
    A lite container for player data stuff

    """
    bool_dead: Union[bool, None]
    wrapper_object_that_collided: Union[bool, None]
    reward: Union[int]

    def __init__(self):
        self.bool_dead = None
        self.wrapper_object_that_collided = None
        self.reward = 9

    def reset(self):
        self.bool_dead = None
        self.wrapper_object_that_collided = None
        self.reward = 0
