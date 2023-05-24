"""
Date created: 5/19/2023

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
    HOW TO MAKE A MENU SCREEN IN PYGAME!
        Notes:
        Reference:
            https://www.youtube.com/watch?v=GMBqjxcKogA
            https://github.com/baraltech/Menu-System-PyGame/blob/main/main.py
"""
import sys

import pygame

from _settings import Settings
from custom.button import Button
from game_snake import GameSnake
from pygame_graphics_game_snake import PygameGraphicsGameSnake
from util import ColorRGB
from util import TYPE_POSITION


class Menu:
    settings: Settings

    font_text: pygame.font.Font
    font_fps: pygame.font.Font

    def __init__(self, settings: Settings):
        """

        :param settings:
        """
        """
        ####################
        Pygame related stuff
        ####################
        """

        self.settings = settings

        pygame.init()

        # font_text = pygame.font_text.SysFont('arial', 25)
        # font_text = pygame.font_text.Font('arial.ttf', 25)

        self.font_text = pygame.font.Font('arial.ttf', self.settings.font_size)
        self.font_fps = pygame.font.Font('arial.ttf', self.settings.font_size)

        self.pygame_surface_main: pygame.Surface = pygame.display.set_mode(
            (self.settings.width, self.settings.height)
        )

        pygame.display.set_caption('Snake game')

    def run(self):
        button_game_snake = Button(
            "Play",
            (self.settings.width // 2, self.settings.height // 2),
            self.font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        button_quit = Button(
            "Quit",
            (self.settings.width // 2, ((self.settings.height // 2) + self.settings.text_line_spacing_amount)),
            self.font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        """ 
        #################### 
        Pre calculated stuff 
        #################### 
        """

        # Amount of blocks available for width and height
        amount_of_block_width = (self.settings.width - self.settings.block_size) // self.settings.block_size
        amount_of_block_height = (self.settings.height - self.settings.block_size) // self.settings.block_size


        while True:
            position_mouse: TYPE_POSITION = pygame.mouse.get_pos()

            # print(position_mouse)

            # TODO: Find better menu displaying solution, button to a new loop seems kind of cringe

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Play button
                if button_game_snake.is_position_colliding(position_mouse):
                    button_game_snake.draw_hover(self.pygame_surface_main)

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        # Make new game
                        game_snake = GameSnake(
                            self.settings,
                            amount_of_block_width,
                            amount_of_block_height
                        )

                        # Make pygame graphics for snake
                        pygame_graphics_game_snake = PygameGraphicsGameSnake(
                            self.settings,
                            self.pygame_surface_main,
                            self.font_text,
                            self.font_text,
                            game_snake
                        )

                        pygame_graphics_game_snake.run()

                else:
                    button_game_snake.draw(self.pygame_surface_main)

                # Quit button
                if button_quit.is_position_colliding(position_mouse):
                    button_quit.draw_hover(self.pygame_surface_main)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()
                else:
                    button_quit.draw(self.pygame_surface_main)

            pygame.display.flip()


def main():
    settings = Settings(800, 600)

    game = Menu(settings)

    game.run()


if __name__ == '__main__':
    main()
