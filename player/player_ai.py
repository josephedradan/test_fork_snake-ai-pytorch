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

from constants import TYPE_ACTION_POSSIBLE
from player.player import Player


class PlayerAI(Player, ABC):

    def __init__(self,
                 action_initial: TYPE_ACTION_POSSIBLE = None
                 ):
        super().__init__()

        # self.generator_game_state = generator_game_state
