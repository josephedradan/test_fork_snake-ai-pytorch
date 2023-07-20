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
from wrapper.wrapper import Wrapper


class DataPlayStepResult(Data):
    """
    A lite container for player data stuff

    """
    bool_dead: bool
    wrapper_object_that_collided: Union[Wrapper, None]

    def __init__(self):
        self.bool_dead = False
        self.wrapper_object_that_collided = None

    def reset(self):
        self.bool_dead = False
        self.wrapper_object_that_collided = None
