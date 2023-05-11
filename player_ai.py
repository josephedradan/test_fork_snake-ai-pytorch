import random
from typing import List

import numpy as np
import pygame

from player import Player
from util import BLOCK_SIZE
from util import Action
from util import Chunk
from util import ColorRGB
from util import FPS

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


class SnakeGameAI(Player):
    window_width: int
    window_height: int

    direction: Action

    frame_iteration: int

    def __init__(self, window_width: int = 640, window_height: int = 480):
        """

        :param window_width:
        :param window_height:
        """

        """
        ####################
        Pygame related stuff
        ####################
        """
        self.window_width = window_width
        self.window_height = window_height

        # init pygame_display
        self.display = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Player')
        self.clock = pygame.time.Clock()

        """ 
        #################### 
        PlayerController state related stuff 
        #################### 
        """

        self.reset()

    # def reset(self):
    #     # init game state
    #     self.action_current = Action.RIGHT
    #
    #     self.head = Chunk(self.window_width / 2, self.window_height / 2)
    #
    #     self.list_point_snake = [
    #         self.head,
    #         Chunk(self.head.x - BLOCK_SIZE, self.head.y),
    #         Chunk(self.head.x - (2 * BLOCK_SIZE), self.head.y)
    #     ]
    #
    #     self.score = 0
    #     self.chunk_food = None
    #     self._place_food()
    #     self.index_frame = 0

    def _place_food(self):
        x = random.randint(0, (self.window_width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.window_height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Chunk(x, y)
        if self.food in self.list_point_snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. move
        self._move(action)  # update the chunk_head
        self.list_point_snake.insert(0, self.head)

        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.list_point_snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new chunk_food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.list_point_snake.pop_chunk_last()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(FPS)

        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head

        # hits boundary
        if pt.x > self.window_width - BLOCK_SIZE or pt.x < 0 or pt.y > self.window_height - BLOCK_SIZE or pt.y < 0:
            return True

        # hits itself
        if pt in self.list_point_snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(ColorRGB.BLACK)

        for pt in self.list_point_snake:
            pygame.draw.rect(self.display, ColorRGB.BLUE_1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, ColorRGB.BLUE_2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, ColorRGB.RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, ColorRGB.WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action: List[int]):
        # [straight, right, left]

        clock_wise = [Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]  # right turn r -> d -> l -> u
        else:  # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]  # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Action.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Action.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Action.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Action.UP:
            y -= BLOCK_SIZE

        self.head = Chunk(x, y)
