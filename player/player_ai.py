"""
Date created: 6/21/2023

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
from abc import ABC

from player.player import Player
from constants import TYPE_ACTION_POSSIBLE
from wrapper.wrapper import Wrapper


class PlayerAI(Player, ABC):

    def __init__(self, wrapper: Wrapper,
                 action_initial: TYPE_ACTION_POSSIBLE = None,
                 # generator_game_state  # FIXME: IDK if this should be above the above parameter
                 ):
        super().__init__(wrapper, action_initial)

        # self.generator_game_state = generator_game_state
