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
from collections import deque
from typing import Deque

import pygame

from _settings import Settings
from collidable.collidable_snake import CollidableSnake
from game_snake import GameSnake
from util import Action
from util import BLOCK_SIZE
from util import BLOCK_SIZE_OFFSET
from util import ColorRGB
from util import FONT_SIZE
from util import FPS


class PygameGraphicsGameSnake:
    settings: Settings
    pygame_display: pygame.display
    font_text: pygame.font.Font
    font_fps: pygame.font.Font

    game_snake: GameSnake

    clock: pygame.time.Clock

    amount_of_block_width: int
    amount_of_block_height: int

    def __init__(self,
                 settings: Settings,
                 pygame_display: pygame.display,
                 pygame_font_text: pygame.font.Font,
                 pygame_font_fps: pygame.font.Font,
                 game_snake: GameSnake
                 ):

        """
        ####################
        Pygame related stuff
        ####################
        """
        self.settings = settings
        self.pygame_display = pygame_display

        self.font_text = pygame_font_text
        self.font_fps = pygame_font_fps

        self.clock = pygame.time.Clock()

        ##########

        self.game_snake = game_snake

    def draw_graphics(self):
        """
        Draw collidable_snake game_snake

        Notes:
            The order of draws determines if something is drawn on top of something.

        :return:
        """
        self.pygame_display.fill(ColorRGB.BLACK)

        # Draw walls
        for collidable_wall in self.game_snake.list_collidable_wall:
            for chunk_wall in collidable_wall.get_container_chunk():
                pygame.draw.rect(
                    self.pygame_display,
                    ColorRGB.GRAY,
                    pygame.Rect(chunk_wall.x, chunk_wall.y, BLOCK_SIZE, BLOCK_SIZE)
                )

        # Draw snakes
        for index, collidable_snake in enumerate(self.game_snake.list_collidable_snake):

            print(collidable_snake.get_container_chunk())
            # Snake head
            pygame.draw.rect(
                self.pygame_display,
                ColorRGB.GREEN_KELLY,
                pygame.Rect(collidable_snake.get_container_chunk()[0].x + BLOCK_SIZE_OFFSET,
                            collidable_snake.get_container_chunk()[0].y + BLOCK_SIZE_OFFSET,
                            BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2),
                            BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2))
            )

            # Snake body
            for chunk in itertools.islice(
                    collidable_snake.get_container_chunk(),
                    1,
                    len(collidable_snake.get_container_chunk())):

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

                # Inner color
                # pygame.draw.rectangle_button(
                #     self.pygame_surface_main,
                #     ColorRGB.BLUE_2,
                #     pygame.Rect(chunk.x + 4, chunk.y + 4, 12, 12)
                # )

            text = self.font_text.render(
                f"P{index} Score: {collidable_snake.score}",
                True,
                ColorRGB.GREEN
            )

            self.pygame_display.blit(text, (0, FONT_SIZE * (index + 1)))  # Offset scores

        # Draw food
        for collidable_food in self.game_snake.list_collidable_food:
            for chunk_food in collidable_food.get_container_chunk():
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

    def run(self):

        deque_collidable: Deque[CollidableSnake] = deque(self.game_snake.list_collidable_snake)

        while deque_collidable:

            collidable_snake: CollidableSnake = deque_collidable.popleft()

            action_from_player: Action = collidable_snake.get_player().get_action()

            game_over, _, _ = self.game_snake.play_step(collidable_snake, action_from_player)

            self.clock.tick(FPS)
            self.draw_graphics()  # Drawing must be after the check

            if game_over is True:
                continue

            deque_collidable.append(collidable_snake)

        for snake in self.game_snake.list_collidable_snake:
            print('Final Score', snake.score)

        # while True:
        #     bool_game_over, reward, snake = self.game_snake.play_step()
        #     print(bool_game_over)
        #     # Update ui and clock
        #
        #     if bool_game_over is True:
        #         break
        #
        #     self.clock.tick(FPS)
        #     self.draw_graphics()  # Drawing must be after the check
        #
        # for snake in self.game_snake.list_collidable_snake:
        #     print('Final Score', snake.score)
