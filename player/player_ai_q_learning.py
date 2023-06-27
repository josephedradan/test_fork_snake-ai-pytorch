from typing import Tuple
from typing import Type
from typing import Union

import numpy as np
import pygame

from agent.agent_q_learning import AgentQLearning
from constants import Action
from constants import DICT_K_ACTION_V_INDEX_ACTION_CYCLE_CLOCKWISE
from constants import LIST_ACTION_CYCLE_CLOCKWISE
from constants import TYPE_ACTION_POSSIBLE
from constants import TYPE_GAME_STATE
from constants import TYPE_TUPLE_ACTION_RELATIVE
from game_state.generator_game_state import GeneratorGameState
from game_state.generator_game_state_food_single import GeneratorGameStateFoodSingle
from player.player import Player
from singleton_data.singleton_data_game import SingletonDataGame
from singleton_data.singleton_data_player import SingletonDataPlayer
from wrapper.wrapper import Wrapper

pygame.init()
font = pygame.font.Font('../arial.ttf', 25)

NP_NDARRAY_ACTION_SAME = np.ndarray([1, 0, 0])
NP_NDARRAY_ACTION_RIGHT = np.ndarray([0, 1, 0])
NP_NDARRAY_ACTION_LEFT = np.ndarray([0, 0, 1])


# def get_action_new

class PlayerAIQLearning(Player):
    window_width: int
    window_height: int

    direction: Action

    frame_iteration: int

    def __init__(self,
                 wrapper: Wrapper,
                 action_initial: TYPE_ACTION_POSSIBLE = None,
                 generator_game_state: Type[GeneratorGameState] = GeneratorGameStateFoodSingle
                 ):

        super().__init__(wrapper, action_initial)

        self.generator_game_state = generator_game_state
        self.agent_q_learning = AgentQLearning()

        """
        ####################
        Varying variables
        ####################
        """

        self.game_state_current: Union[TYPE_GAME_STATE, None] = None
        self.tuple_action_relative_current: Union[TYPE_TUPLE_ACTION_RELATIVE, None] = None

        # """
        # ####################
        # Pygame related stuff
        # ####################
        # """
        # self.window_width = window_width
        # self.window_height = window_height
        #
        # # init pygame_surface_main
        # self.display = pygame.display.set_mode((self.window_width, self.window_height))
        # pygame.display.set_caption('Player')
        # self.clock = pygame.time.Clock()
        #
        # """
        # ####################
        # PlayerController game_state_current related stuff
        # ####################
        # """
        #
        # self.reset()

    # def reset(self):
    #     # init game_snake game_state_current
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

    def get_action_new(self, singleton_data_game: SingletonDataGame) -> TYPE_ACTION_POSSIBLE:

        self.game_state_current = self.generator_game_state.get_game_state(singleton_data_game, self)

        self.tuple_action_relative_current = self.agent_q_learning.get_tuple_action_relative(self.game_state_current)

        return self.get_action_from_tuple_action_relative(self.tuple_action_relative_current)

    def send_feedback_play_step(self,
                                singleton_data_game: SingletonDataGame,
                                singleton_data_player: SingletonDataPlayer,
                                ):

        game_state_new = self.generator_game_state.get_game_state(singleton_data_game, self)

        self.agent_q_learning.train_short_memory(
            self.game_state_current,
            self.get_action_current(),
            singleton_data_player.reward,
            game_state_new,
            singleton_data_player.bool_snake_died,
        )



    # def _place_food(self):
    #     x = random.randint(0, (self.window_width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    #     y = random.randint(0, (self.window_height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    #     self.food = Chunk(x, y)
    #     if self.food in self.list_point_snake:
    #         self._place_food()
    #
    # def play_step(self, action):  # FIXME: ACTION IS IN FORMAT [0,0,0]
    #     self.frame_iteration += 1
    #
    #     # 1. collect user input
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #
    #     # 2. move
    #     self._move(action)  # draw the chunk_head
    #     self.list_point_snake.insert(0, self.head)
    #
    #     # 3. check if game_snake over
    #     reward = 0
    #     game_over = False
    #     if self.is_collision() or self.frame_iteration > 100 * len(self.list_point_snake):
    #         game_over = True
    #         reward = -10
    #         return reward, game_over, self.score
    #
    #     # 4. place new chunk_food or just move
    #     if self.head == self.food:
    #         self.score += 1
    #         reward = 10
    #         self._place_food()
    #     else:
    #         self.list_point_snake.pop_chunk_last()
    #
    #     # 5. draw ui and clock
    #     self._update_ui()
    #     self.clock.tick(FPS)
    #
    #     # 6. return game_snake over and score
    #     return reward, game_over, self.score
    #
    # def is_collision(self, pt=None):
    #     if pt is None:
    #         pt = self.head
    #
    #     # hits boundary
    #     if pt.x > self.window_width - BLOCK_SIZE or pt.x < 0 or pt.y > self.window_height - BLOCK_SIZE or pt.y < 0:
    #         return True
    #
    #     # hits itself
    #     if pt in self.list_point_snake[1:]:
    #         return True
    #
    #     return False
    #
    # def _update_ui(self):
    #     self.display.fill(ColorRGB.BLACK)
    #
    #     for pt in self.list_point_snake:
    #         pygame.draw.rect(self.display, ColorRGB.BLUE_1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
    #         pygame.draw.rect(self.display, ColorRGB.BLUE_2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
    #
    #     pygame.draw.rect(self.display, ColorRGB.RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
    #
    #     text = font.render("Score: " + str(self.score), True, ColorRGB.WHITE)
    #     self.display.blit(text, [0, 0])
    #     pygame.display.flip()
    #
    # def _move(self, action):  # FIXME: ACTION IS IN FORMAT [0,0,0]
    #     """
    #     action is a List of 3 ints representing [straight, right, left] WHICH IS [0,0,0]
    #
    #     :param action:
    #     :return:
    #     """
    #
    #     clock_wise = [Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP]
    #     idx = clock_wise.index(self.direction)
    #
    #     if np.array_equal(action, [1, 0, 0]):
    #         new_dir: Action = clock_wise[idx]  # no change
    #     elif np.array_equal(action, [0, 1, 0]):
    #         next_idx = (idx + 1) % 4
    #         new_dir: Action = clock_wise[next_idx]  # right turn r -> d -> l -> u
    #     else:  # [0, 0, 1]
    #         next_idx = (idx - 1) % 4
    #         new_dir: Action = clock_wise[next_idx]  # left turn r -> u -> l -> d
    #
    #     self.direction: Action = new_dir
    #
    #     x = self.head.x
    #     y = self.head.y
    #     if self.direction == Action.RIGHT:
    #         x += BLOCK_SIZE
    #     elif self.direction == Action.LEFT:
    #         x -= BLOCK_SIZE
    #     elif self.direction == Action.DOWN:
    #         y += BLOCK_SIZE
    #     elif self.direction == Action.UP:
    #         y -= BLOCK_SIZE
    #
    #     self.head = Chunk(x, y)

    def get_action_from_tuple_action_relative(self,
                                              tuple_action_relative: Tuple[int, int, int]) -> TYPE_ACTION_POSSIBLE:

        index_action_cycle_clockwise = DICT_K_ACTION_V_INDEX_ACTION_CYCLE_CLOCKWISE.get(self.action)

        if index_action_cycle_clockwise is None:
            return self.action

        if np.array_equal(tuple_action_relative, NP_NDARRAY_ACTION_SAME):

            # Action is the same so no change is needed
            # self.action = LIST_ACTION_CYCLE_CLOCKWISE[index_action_cycle_clockwise]
            pass

        elif np.array_equal(tuple_action_relative, NP_NDARRAY_ACTION_RIGHT):
            next_idx = (index_action_cycle_clockwise + 1) % 4

            # Action will turn right relative to current Action (r -> d -> l -> u)
            self.action = LIST_ACTION_CYCLE_CLOCKWISE[next_idx]

        elif np.array_equal(tuple_action_relative, NP_NDARRAY_ACTION_LEFT):  # [0, 0, 1]
            next_idx = (index_action_cycle_clockwise - 1) % 4

            # Action will turn left relative to current Action (r -> u -> l -> d)
            self.action = LIST_ACTION_CYCLE_CLOCKWISE[next_idx]

        return self.action
