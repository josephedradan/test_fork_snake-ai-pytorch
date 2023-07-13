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
from typing import Union

import pygame

from _settings import Settings
from constants import Action
from constants import ColorRGB
from constants import TYPE_POSITION
from game.game_snake import GameSnake
from graphics.graphics_pygame import GraphicsPygame
from logic_game_snake import LogicGameSnake
from player.player_ai_q_learning import PlayerAIQLearning
from player.player_keyboard import PlayerKeyboard
from pygame_abstraction.button import Button
from agent.data.data_game import DataGame


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

        pygame.display.set_caption('Snake logic_game_snake')

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

        data_game: Union[DataGame, None] = None

        """ 
        #################### 
        Pre calculated stuff 
        #################### 
        """

        # Amount of blocks available for width and height
        amount_of_block_width = (self.settings.width - self.settings.block_size) // self.settings.block_size
        amount_of_block_height = (self.settings.height - self.settings.block_size) // self.settings.block_size


        ##########
        position_mouse: TYPE_POSITION = pygame.mouse.get_pos()
        ##########

        """
        
        IMPORTANT NOTES:
            Do not double draw on the same location, whatever drew first will take priority...
            
        """
        while True:

            # Clear screen because so old data
            self.pygame_surface_main.fill(ColorRGB.BLACK)

            # print(position_mouse)

            #########################
            # Buttons
            #########################

            # TODO: Find better menu displaying solution, button to a new loop seems kind of cringe
            for event in pygame.event.get():
                position_mouse = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    pygame.quit()

                # Play button
                if button_play.is_position_colliding(position_mouse):

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        data_game = self._menu_play(amount_of_block_width, amount_of_block_height)

                        button_play.draw(self.pygame_surface_main)

                # Quit button
                if button_quit.is_position_colliding(position_mouse):

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        sys.exit()

            #########################

            # Play button
            if button_play.is_position_colliding(position_mouse):
                button_play.draw_hover(self.pygame_surface_main)

            else:
                button_play.draw(self.pygame_surface_main)

            # Quit button
            if button_quit.is_position_colliding(position_mouse):
                button_quit.draw_hover(self.pygame_surface_main)

            else:
                button_quit.draw(self.pygame_surface_main)


            #########################
            # Text post game data
            #########################

            if data_game:
                for index, player in enumerate(data_game.list_player):
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

    def _menu_play(self, amount_of_block_width, amount_of_block_height):

        #####

        button_play_keyboard = Button(
            "Keyboard",
            (self.settings.width // 2, (self.settings.height // 2)),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        button_play_ai = Button(
            "AI (Deep Q Learning)",
            (self.settings.width // 2, ((self.settings.height // 2) + self.settings.text_line_spacing_amount)),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        button_play_back = Button(
            "Back",
            (self.settings.width // 2, ((self.settings.height // 2) + (2 * self.settings.text_line_spacing_amount))),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        #####

        position_mouse: TYPE_POSITION = pygame.mouse.get_pos()

        while True:
            self.pygame_surface_main.fill(ColorRGB.BLACK)

            for event in pygame.event.get():
                position_mouse = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    pygame.quit()

                # Play using keyboard
                if button_play_keyboard.is_position_colliding(position_mouse):
                    clock = pygame.time.Clock()
                    if event.type == pygame.MOUSEBUTTONDOWN:

                        # Make new logic_game_snake
                        logic_game_snake = LogicGameSnake(
                            [PlayerKeyboard()],
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
                            self.pygame_font_fps,
                        )

                        data_game = graphics_pygame.run_loop()

                        return data_game

                # Play using AI
                if button_play_ai.is_position_colliding(position_mouse):

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        player_ai_q_learning = PlayerAIQLearning()

                        player_ai_q_learning.set_action(Action.RIGHT)  # Set initial Action so no crash for AI  # TODO FIX

                        logic_game_snake = LogicGameSnake(
                            [player_ai_q_learning],
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
                            self.pygame_font_fps,
                        )

                        data_game = graphics_pygame.run_loop()

                        return data_game

                # Go back
                if button_play_back.is_position_colliding(position_mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        return None

            #########################

            # Play button
            if button_play_keyboard.is_position_colliding(position_mouse):
                button_play_keyboard.draw_hover(self.pygame_surface_main)

            else:
                button_play_keyboard.draw(self.pygame_surface_main)

            # AI button
            if button_play_ai.is_position_colliding(position_mouse):
                button_play_ai.draw_hover(self.pygame_surface_main)
            else:
                button_play_ai.draw(self.pygame_surface_main)

            # Quit button
            if button_play_back.is_position_colliding(position_mouse):
                button_play_back.draw_hover(self.pygame_surface_main)

            else:
                button_play_back.draw(self.pygame_surface_main)

            pygame.display.flip()
