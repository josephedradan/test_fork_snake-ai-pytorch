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

from logic_game_snake import LogicGameSnake
from player import Player


class GeneratorGameState(ABC):

    @staticmethod
    @abstractmethod
    def get_game_state(game_snake: LogicGameSnake, player: Player):
        ...
