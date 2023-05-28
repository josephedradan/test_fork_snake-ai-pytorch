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

from game_snake import GameSnake
from player import Player


class GameState(ABC):

    @abstractmethod
    def generate_game_state(self, game_snake: GameSnake, player: Player):
        ...
