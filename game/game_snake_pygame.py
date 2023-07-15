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

    How to create a text input box with Pygame?
        Reference:
            https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/

"""
from typing import Union

import pygame

from _settings import Settings
from constants import ColorRGB
from constants import Condition
from constants import TYPE_POSITION
from data.data_game import DataGame
from game.game_snake import GameSnake
from graphics.graphics_pygame import GraphicsPygame
from logic_game_snake import LogicGameSnake
from player.player_ai_q_learning import PlayerAIQLearning
from player.player_keyboard import PlayerKeyboard
from pygame_abstraction.text_box import TextBox
from pygame_abstraction.text_button import TextButton


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

        #####

        self.player_ai_q_learning = PlayerAIQLearning()

    def run(self):
        button_play = TextButton(
            "Play",
            (self.settings.width // 2, self.settings.height // 2),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        button_quit = TextButton(
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

        ####################
        position_mouse: TYPE_POSITION = pygame.mouse.get_pos()

        """
        IMPORTANT NOTES:
            Do not double draw on the same location, whatever drew first will take priority...
            
        """
        while True:

            # Clear screen because so old data
            self.pygame_surface_main.fill(ColorRGB.BLACK)

            # TODO: Find better menu displaying solution, button to a new loop seems kind of cringe

            event: pygame.event.Event
            for event in pygame.event.get():
                position_mouse = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                # Play button
                if button_play.is_position_colliding(position_mouse):

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        data_game = self._menu_play(amount_of_block_width, amount_of_block_height)

                        button_play.draw(self.pygame_surface_main)

                # Quit button
                if button_quit.is_position_colliding(position_mouse):

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        exit(0)

            #########################
            # Drawing
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

            # Text post game data
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

        button_play_keyboard = TextButton(
            "Keyboard",
            (self.settings.width // 2, (self.settings.height // 2)),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        button_play_ai = TextButton(
            "AI",
            (self.settings.width // 2, ((self.settings.height // 2) + self.settings.text_line_spacing_amount)),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        button_play_back = TextButton(
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

            event: pygame.event.Event
            for event in pygame.event.get():
                position_mouse = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

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
                    self._menu_ai_deep_q_learning()

                    # if event.type == pygame.MOUSEBUTTONDOWN:
                    #     # Set initial Action because the AI will crash without it
                    #     action_random = random.choice(LIST_ACTION_CYCLE_CLOCKWISE)
                    #
                    #     self.player_ai_q_learning.set_action(action_random)
                    #
                    #     logic_game_snake = LogicGameSnake(
                    #         [self.player_ai_q_learning],
                    #         self.settings,
                    #         amount_of_block_width,
                    #         amount_of_block_height
                    #     )
                    #
                    #     # Make pygame graphics for the logic_game_snake
                    #     graphics_pygame = GraphicsPygame(
                    #         self.settings,
                    #         logic_game_snake,
                    #         self.pygame_surface_main,
                    #         self.pygame_font_text,
                    #         self.pygame_font_fps,
                    #     )
                    #
                    #     data_game = graphics_pygame.run_loop()
                    #
                    #     return data_game

                # Go back
                if button_play_back.is_position_colliding(position_mouse):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        return None

            #########################
            # Drawing
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

    def _menu_ai_deep_q_learning(self):

        button_play_ai = TextButton(
            "Play AI (Deep Q Learning)",
            (self.settings.width // 2, ((self.settings.height // 2) + self.settings.text_line_spacing_amount)),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN
        )

        text_box = TextBox(
            "100",
            (self.settings.width // 2, ((self.settings.height // 2) + (2 * self.settings.text_line_spacing_amount))),
            self.pygame_font_text,
            ColorRGB.WHITE,
            ColorRGB.GREEN,
            ColorRGB.BLACK,
            ColorRGB.BLACK,
            ColorRGB.GOLD,
            ColorRGB.BLACK,
        )

        #####

        condition_amount_run: Condition = Condition.STATE_1
        bool_amount_run = False

        #####

        position_mouse: TYPE_POSITION = pygame.mouse.get_pos()
        while True:
            self.pygame_surface_main.fill(ColorRGB.BLACK)

            event: pygame.event.Event
            for event in pygame.event.get():
                position_mouse = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

                # Handling bool_amount_run if NOT True
                if not bool_amount_run:

                    if text_box.is_position_colliding(position_mouse):
                        condition_amount_run = Condition.STATE_2
                    else:
                        condition_amount_run = Condition.STATE_1

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if text_box.is_position_colliding(position_mouse):

                        # Setting bool_amount_run to True
                        if condition_amount_run == Condition.STATE_1 or condition_amount_run == Condition.STATE_2:
                            condition_amount_run = Condition.STATE_3
                            bool_amount_run = True
                        else:
                            condition_amount_run = Condition.STATE_2
                            bool_amount_run = False

                    else:
                        bool_amount_run = False

                if event.type == pygame.KEYDOWN:

                    # Handling bool_amount_run if True
                    if bool_amount_run:

                        # event.unicode only exists when event.type == pygame.KEYDOWN  # It's also a string
                        if event.unicode.isnumeric():
                            text_box.add_list_char_input_amount_run(event.unicode)

                    if event.key == pygame.K_BACKSPACE:
                        text_box.pop_list_char_input_amount_run()

            # # Using pygame.key than using event.key (This way can handle if the key is held down)
            # scan_code_wrapper_keys: ScancodeWrapper = pygame.key.get_pressed()
            # if condition_amount_run:
            #     if scan_code_wrapper_keys[pygame.K_BACKSPACE]:
            #         text_box.pop_list_char_input_amount_run()

            #########################
            # Drawing
            #########################

            if condition_amount_run == Condition.STATE_1:
                text_box.draw(self.pygame_surface_main)

            elif condition_amount_run == Condition.STATE_2:
                text_box.draw_hover(self.pygame_surface_main)

            elif condition_amount_run == Condition.STATE_3:
                text_box.draw_active(self.pygame_surface_main)

            pygame.display.flip()
