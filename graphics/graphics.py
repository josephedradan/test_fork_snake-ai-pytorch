"""
Date created: 6/13/2023

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

from _settings import Settings
from logic_game_snake import LogicGameSnake


class Graphics(ABC):
    settings: Settings

    game_snake: LogicGameSnake

    def __init__(self,
                 settings: Settings,
                 game_snake: LogicGameSnake
                 ):
        self.settings = settings
        self.game_snake = game_snake

    @abstractmethod
    def draw_graphics(self):
        ...

    def get_game_snake(self) -> LogicGameSnake:
        return self.game_snake

    def run(self):
        def callback_draw_game():
            """
            This callable contains pygame drawing related stuff

            :return:
            """
            nonlocal self

            self.draw_graphics()

        self.game_snake.run(callback_draw_game)
