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
from singleton_data.singleton_data_game import SingletonDataGame
from game.game_snake import GameSnake
from graphics.graphics_pygame import GraphicsPygame
from logic_game_snake import LogicGameSnake
from pygame_snake.button import Button
from constants import ColorRGB
from constants import TYPE_POSITION


class GameSnakePygame(GameSnake):
    pygame_font_text: pygame.font.Font
    pygame_font_fps: pygame.font.Font

    def __init__(self, settings: Settings):
        """

        :param settings:
        """

        super().__init__(settings)

        """
        ####################
        Pygame related stuff
        ####################
        """

        pygame.init()

        # pygame_font_text = pygame.pygame_font_text.SysFont('arial', 25)
        # pygame_font_text = pygame.pygame_font_text.Font('arial.ttf', 25)

        self.pygame_font_text = pygame.font.Font('arial.ttf', self.settings.font_size)
        self.pygame_font_fps = pygame.font.Font('arial.ttf', self.settings.font_size)

        self.pygame_surface_main: pygame.Surface = pygame.display.set_mode(
            (self.settings.width, self.settings.height)
        )

        pygame.display.set_caption('Snake game_snake')

    def run(self):
        button_play = Button(
            "Play",
            (self.settings.width // 2, self.settings.height // 2),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        button_quit = Button(
            "Quit",
            (self.settings.width // 2, ((self.settings.height // 2) + self.settings.text_line_spacing_amount)),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        singleton_data_game = None

        """ 
        #################### 
        Pre calculated stuff 
        #################### 
        """

        # Amount of blocks available for width and height
        amount_of_block_width = (self.settings.width - self.settings.block_size) // self.settings.block_size
        amount_of_block_height = (self.settings.height - self.settings.block_size) // self.settings.block_size

        """
        
        IMPORTANT NOTES:
            Do not double draw on the same location, whatever drew first will take priority...
            
        """

        while True:

            position_mouse: TYPE_POSITION = pygame.mouse.get_pos()

            # print(position_mouse)

            ########################
            # Buttons
            ########################

            # TODO: Find better menu displaying solution, button to a new loop seems kind of cringe

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                # Play button
                if button_play.is_position_colliding(position_mouse):
                    button_play.draw_hover(self.pygame_surface_main)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Make new logic_game_snake
                        logic_game_snake = LogicGameSnake(
                            self.settings,
                            amount_of_block_width,
                            amount_of_block_height
                        )

                        # Make pygame graphics for the logic_game_snake
                        graphics_pygame = GraphicsPygame(
                            self.settings,
                            logic_game_snake,
                            self.pygame_surface_main,
                            self.pygame_font_text,
                            self.pygame_font_text,
                        )

                        singleton_data_game: SingletonDataGame = graphics_pygame.run()  # TODO: GET BETTER STATS

                        self.pygame_surface_main.fill(ColorRGB.BLACK)
                        button_play.draw(self.pygame_surface_main)

                        # FIXME: After the logic_game_snake is done, text font_text is not fully drawn

                else:
                    button_play.draw(self.pygame_surface_main)

                # Quit button
                if button_quit.is_position_colliding(position_mouse):
                    button_quit.draw_hover(self.pygame_surface_main)

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()

                else:
                    button_quit.draw(self.pygame_surface_main)

                ########################
                # Text post game data
                ########################

                if singleton_data_game:
                    for index, player in enumerate(singleton_data_game.list_player):
                        surface_text = self.pygame_font_text.render(
                            f"Snake {index} score: {player.score}",
                            True,
                            ColorRGB.WHITE)

                        rectangle = surface_text.get_rect(
                            center=(self.settings.width // 2,  # X
                                    ((self.settings.height // 2) +  # Y
                                     (self.settings.text_line_spacing_amount * 3) +  # Y Offset from other text
                                     self.settings.text_line_spacing_amount * index  # Y Spacing for each line
                                     ))
                        )

                        self.pygame_surface_main.blit(surface_text, rectangle)

            pygame.display.flip()
