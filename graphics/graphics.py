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
from data.data_game import DataGame


class Graphics(ABC):
    settings: Settings

    logic_game_snake: LogicGameSnake

    def __init__(self,
                 settings: Settings,
                 logic_game_snake: LogicGameSnake
                 ):
        self.settings = settings
        self.logic_game_snake = logic_game_snake

    def get_logic_game_snake(self) -> LogicGameSnake:
        return self.logic_game_snake

    @abstractmethod
    def draw_graphics(self):
        """
        Default draw graphics is to not do anything

        :return:
        """
        pass

    @abstractmethod
    def run_loop(self) -> DataGame:  # TODO: MAYBE RETURN SOMETHING ELSE? MORE GAME DATA???
        """

        Notes:
            You can override this method to implement a custom loop

        :return:
        """
        pass
        # while not self.logic_game_snake.data_game.bool_game_over:  # Fixme: self.logic_game_snake is a little too powerful?
        #     game_data = self.logic_game_snake.get_generator_run_step()
        #     self.draw_graphics()
        #
        # return self.logic_game_snake.data_game
