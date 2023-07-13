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

from player.player import Player
from constants import TYPE_GAME_STATE
from agent.data.data_game import DataGame


class GeneratorGameState(ABC):

    @staticmethod
    @abstractmethod
    def get_game_state(data_game: DataGame, player: Player) -> TYPE_GAME_STATE:
        ...
