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

from constants import TYPEVAR_WRAPPER
from player.player import Player


class PlayerAI(Player[TYPEVAR_WRAPPER], ABC):

    def __init__(self,
                 ):
        super().__init__()
