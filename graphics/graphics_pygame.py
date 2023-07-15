"""
Date created: 5/21/2023

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
import itertools

import pygame

from _settings import Settings
from constants import BLOCK_SIZE
from constants import BLOCK_SIZE_OFFSET
from constants import ColorRGB
from constants import FONT_SIZE
from constants import FPS
from graphics.graphics import Graphics
from logic_game_snake import LogicGameSnake
from data.data_game import DataGame


class GraphicsPygame(Graphics):
    pygame_display: pygame.display
    font_text: pygame.font.Font
    font_fps: pygame.font.Font

    clock: pygame.time.Clock

    def __init__(self,
                 settings: Settings,
                 logic_game_snake: LogicGameSnake,
                 pygame_display: pygame.display,
                 pygame_font_text: pygame.font.Font,
                 pygame_font_fps: pygame.font.Font,
                 ):

        """
        ####################
        Pygame related stuff
        ####################
        """
        super().__init__(settings, logic_game_snake)

        self.pygame_display = pygame_display

        self.font_text = pygame_font_text
        self.font_fps = pygame_font_fps

        self.clock = pygame.time.Clock()

        ##########

    def draw_graphics(self):
        """
        Non generalized drawing pygame graphics

        Notes:
            The order of draws determines if something is drawn on top of something.

        :return:
        """
        self.clock.tick(FPS)  # Sets the FPS of the game

        self.pygame_display.fill(ColorRGB.BLACK)

        # Draw walls
        for wrapper_wall in self.logic_game_snake.data_game.list_wrapper_wall:
            for chunk_wall in wrapper_wall.get_container_chunk():
                pygame.draw.rect(
                    self.pygame_display,
                    ColorRGB.GRAY,
                    pygame.Rect(chunk_wall.x, chunk_wall.y, BLOCK_SIZE, BLOCK_SIZE)
                )

        # Draw snakes
        for index, player in enumerate(self.logic_game_snake.data_game.list_player):

            wrapper_from_player = player.get_wrapper()

            # Draw snake head
            pygame.draw.rect(
                self.pygame_display,
                ColorRGB.GREEN_KELLY,
                pygame.Rect(wrapper_from_player.get_container_chunk()[0].x + BLOCK_SIZE_OFFSET,
                            wrapper_from_player.get_container_chunk()[0].y + BLOCK_SIZE_OFFSET,
                            BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2),
                            BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2))
            )

            # Draw snake body
            for chunk in itertools.islice(
                    wrapper_from_player.get_container_chunk(),
                    1,
                    len(wrapper_from_player.get_container_chunk())):
                pygame.draw.rect(
                    self.pygame_display,
                    ColorRGB.GREEN,
                    pygame.Rect(
                        chunk.x + BLOCK_SIZE_OFFSET,
                        chunk.y + BLOCK_SIZE_OFFSET,
                        BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2),
                        BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2)
                    )
                )

                # Inner color_text
                # pygame.draw.pygame_rect_positioning(
                #     self.pygame_surface_main,
                #     ColorRGB.BLUE_2,
                #     pygame.Rect(chunk.x + 4, chunk.y + 4, 12, 12)
                # )

            # Create text score
            text = self.font_text.render(
                f"P{index} Score: {player.score}",
                True,
                ColorRGB.GREEN
            )

            # Draw text score
            self.pygame_display.blit(text, (0, FONT_SIZE * (index + 1)))  # Offset scores

        # Draw food
        for wrapper_food in self.logic_game_snake.data_game.list_wrapper_food:
            for chunk_food in wrapper_food.get_container_chunk():
                pygame.draw.rect(
                    self.pygame_display,
                    ColorRGB.RED,
                    pygame.Rect(
                        chunk_food.x + BLOCK_SIZE_OFFSET,
                        chunk_food.y + BLOCK_SIZE_OFFSET,
                        BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2),
                        BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2)
                    )
                )

        text_fps = self.font_fps.render(
            f"FPS: {self.clock.get_fps()}",
            True,
            ColorRGB.GREEN
        )
        self.pygame_display.blit(text_fps, (0, 0))

        pygame.display.flip()  # Draw on screen

    def run_loop(self) -> DataGame:

        generator_run_step = self.logic_game_snake.get_generator_run_step()

        self.logic_game_snake.data_game.list_pygame_event = pygame.event.get()

        for data_game in generator_run_step:

            list_pygame_event = pygame.event.get()

            data_game.list_pygame_event = list_pygame_event

            # This loop prevents the pygame window from hanging
            for event in list_pygame_event:
                pass


            self.draw_graphics()

        return self.logic_game_snake.data_game
