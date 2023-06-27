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

from singleton_data.singleton_singleton_data_game import SingletonDataGame
from player.player import Player
from constants import TYPE_GAME_STATE


class GeneratorGameState(ABC):

    @staticmethod
    @abstractmethod
    def get_game_state(singleton_data_game: SingletonDataGame, player: Player) -> TYPE_GAME_STATE:
        ...
