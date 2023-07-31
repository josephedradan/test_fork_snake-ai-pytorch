"""
Date created: 5/24/2023

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
from abc import abstractmethod

from constants import TYPE_NP_NDARRAY_GAME_STATE_GENERIC
from player.player import Player
from data.data_game import DataGame


class GeneratorGameState(ABC):

    @staticmethod
    @abstractmethod
    def get_game_state(data_game: DataGame, player: Player) -> TYPE_NP_NDARRAY_GAME_STATE_GENERIC:
        ...
