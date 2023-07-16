"""
Date created: 6/15/2023

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
from __future__ import annotations

from typing import Deque
from typing import List
from typing import TYPE_CHECKING
from typing import Union

import pygame

from _settings import Settings

if TYPE_CHECKING:
    from player.player import Player
    from wrapper.wrapper_food import WrapperFood
    from wrapper.wrapper_snake import WrapperSnake
    from wrapper.wrapper_wall import WrapperWall

class DataGame:
    """
    A lite container of the variables in LogicGameSnake

    Notes:
        It's all the data that can be used to make the game game_state.
        This object exists because different AI agents have different interpretations of
        what a game game_state is.

    """
    settings: Settings

    list_player: List[Player]

    list_wrapper_snake: List[WrapperSnake]
    list_wrapper_food: List[WrapperFood]
    list_wrapper_wall: List[WrapperWall]

    #####

    list_pygame_event: List[pygame.event.Event]
    index_frame: int
    deque_player: Union[Deque[Player], None]
    bool_game_over: bool

    def __init__(self, settings: Settings):
        self.settings = settings

        self.list_player = []

        self.list_wrapper_snake = []
        self.list_wrapper_food = []
        self.list_wrapper_wall = []

        #####

        self.list_pygame_event = []

        self.index_frame = 0

        self.deque_player = None

        self.bool_game_over = False

    def __str__(self):
        return "\n".join(f"Player {index} Score: {player.score}" for index, player in enumerate(self.list_player))
