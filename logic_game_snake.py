"""
Date created: 4/27/2023

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
import random
from collections import deque
from typing import Generator
from typing import List
from typing import Tuple
from typing import Union

from _settings import Settings
from chunk import Chunk
from constants import Action
from container_chunk.container_chunk_snake import ContainerChunkSnake
from data.data_game import DataGame
from data.data_player import DataPlayer
from player.player import Player
from utility import get_wrapper_from_chunk_that_collided
from wrapper.wrapper import Wrapper
from wrapper.wrapper_food import WrapperFood
from wrapper.wrapper_snake import WrapperSnake
from wrapper.wrapper_wall import WrapperWall


class LogicGameSnake:
    settings: Settings
    amount_of_block_width: int
    amount_of_block_height: int

    def __init__(self,
                 # pygame_surface_main: pygame.display,
                 # window_width: int,
                 # window_height: int,
                 # pygame_font_text: pygame.font_text.Font,
                 # pygame_font_fps: pygame.font_text.Font
                 list_player: List[Player],
                 settings: Settings,
                 amount_of_block_width: int,
                 amount_of_block_height: int,
                 ):

        self.settings = settings

        self.amount_of_block_width = amount_of_block_width
        self.amount_of_block_height = amount_of_block_height

        """ 
        #################### 
        GameSnakePygame related stuff 
        #################### 
        """

        self.data_game = DataGame(self.settings)

        # This is a data container about the current player
        self.data_player = DataPlayer()

        self._initialize(list_player)

    def _initialize(self, list_player: List[Player]):

        wrapper_wall_border: WrapperWall = WrapperWall()

        # Create horizontal walls
        for i in range(self.amount_of_block_width + 1):
            x_start = i * self.settings.block_size
            y_start = self.amount_of_block_height * self.settings.block_size

            wrapper_wall_border.get_container_chunk().add_new_chunk(Chunk(x_start, 0))
            wrapper_wall_border.get_container_chunk().add_new_chunk(Chunk(x_start, y_start))

        # Create vertical walls
        for i in range(1, self.amount_of_block_height):
            x_start = self.amount_of_block_width * self.settings.block_size
            y_start = i * self.settings.block_size

            wrapper_wall_border.get_container_chunk().add_new_chunk(Chunk(0, y_start))
            wrapper_wall_border.get_container_chunk().add_new_chunk(Chunk(x_start, y_start))

        self.data_game.list_wrapper_wall.append(wrapper_wall_border)

        ##########
        # Create players

        for player in list_player:
            wrapper_snake: WrapperSnake = WrapperSnake(
                [Chunk(self.settings.width // 2, self.settings.height // 2)]  # Initial position_center
            )

            player.set_wrapper(wrapper_snake)

            self.data_game.list_player.append(player)

            self.data_game.list_wrapper_snake.append(wrapper_snake)

        self.data_game.deque_player = deque(self.data_game.list_player)

        ##########
        # Create food

        for i in range(self.settings.amount_food):
            wrapper_food: WrapperFood = WrapperFood()

            self.data_game.list_wrapper_food.append(wrapper_food)

        for wrapper_food in self.data_game.list_wrapper_food:
            self._place_food(wrapper_food)

    def _place_food(self,
                    wrapper_food: WrapperFood,
                    chunk_that_collided_with_wrapper: Union[Chunk, None] = None) -> Chunk:
        """
        Place food by reusing the same food object
        
        :param wrapper_food:
        :param chunk_that_collided_with_wrapper:
        :return: 
        """
        if chunk_that_collided_with_wrapper is None:
            chunk_food = Chunk(0, 0)

        else:
            # Slight optimization by reusing the food chunk that was collided rather than making a new chunk
            chunk_food = wrapper_food.get_container_chunk().pop_chunk(
                chunk_that_collided_with_wrapper
            )

        # n amount of tries (3 in this case) to add a new chunk to wrapper_food via randomness
        for _ in range(3):

            x = random.randint(0, self.amount_of_block_width) * self.settings.block_size
            y = random.randint(0, self.amount_of_block_height) * self.settings.block_size

            chunk_food.x = x
            chunk_food.y = y

            # If chunk_food not in all list_wrapper, then chunk_food can be added to the wrapper
            if all([chunk_food not in wrapper_selected.get_container_chunk()
                    for wrapper_selected in itertools.chain(self.data_game.list_wrapper_snake,
                                                            self.data_game.list_wrapper_food,
                                                            self.data_game.list_wrapper_wall)]):
                wrapper_food.get_container_chunk().add_new_chunk(chunk_food)
                return chunk_food

        # Fallback if randomness can't find a valid position to add chunk_food to a wrapper_food
        for width in range(self.amount_of_block_width):
            for height in range(self.amount_of_block_height):

                chunk_food.x = width * self.settings.block_size
                chunk_food.y = height * self.settings.block_size

                # If chunk_food not in all list_wrapper, then chunk_food can be added to the wrapper
                if all([chunk_food not in wrapper_selected.get_container_chunk()
                        for wrapper_selected in itertools.chain(self.data_game.list_wrapper_snake,
                                                                self.data_game.list_wrapper_food,
                                                                self.data_game.list_wrapper_wall)]):
                    wrapper_food.get_container_chunk().add_new_chunk(chunk_food)
                    return chunk_food

    def play_step_player(self,
                         player: Player,
                         action_from_player: Action) -> DataPlayer:

        self.data_game.index_frame += 1

        self.data_player.bool_dead = False
        self.data_player.wrapper_object_that_collided = None
        self.data_player.reward = 0

        # time_previous = time.time()

        wrapper_from_player: Wrapper = player.get_wrapper()

        container_chunk_snake = wrapper_from_player.get_container_chunk()

        chunk_snake_to_move_possible, x_chunk_snake_last_old, y_chunk_snake_last_old = self.get_chunk_snake_to_move_possible(
            # time_previous,
            container_chunk_snake,
            action_from_player
        )

        # TODO: MOVE THIS CHECKING SOMEWHERELSE + REDESIGN
        ####################
        # Collision checking
        ####################
        wrapper_object_that_collided: Union[Wrapper, None] = get_wrapper_from_chunk_that_collided(
            self.data_game,
            chunk_snake_to_move_possible
        )

        # Move the player by placing chunk_snake_to_move_possible at the front of container_chunk_snake
        container_chunk_snake.add_new_chunk_front(chunk_snake_to_move_possible)

        # Check collision player with food
        if isinstance(wrapper_object_that_collided, WrapperFood):
            player.add_to_score(1)

            self.data_player.reward = 108

            self._place_food(wrapper_object_that_collided, chunk_snake_to_move_possible)

            # Extend the current player
            wrapper_from_player.get_container_chunk().add_new_chunk(
                Chunk(x_chunk_snake_last_old, y_chunk_snake_last_old)

            )
            return self.data_player

        # Collision player with player (Does not care about which player)
        if isinstance(wrapper_object_that_collided, WrapperSnake):
            self.data_player.bool_dead = True
            self.data_player.wrapper_object_that_collided = wrapper_object_that_collided
            self.data_player.reward = -10  # FIXME: MODEL IS VERY SENSITIVE TO HIGH REQARD
            print("Hit Snake")

            return self.data_player

        # Check collision player with wall
        if isinstance(wrapper_object_that_collided, WrapperWall):
            self.data_player.bool_dead = True
            self.data_player.wrapper_object_that_collided = wrapper_object_that_collided
            self.data_player.reward = -10

            print("Hit wall")
            return self.data_player

        return self.data_player

    def get_chunk_snake_to_move_possible(self,
                                         container_chunk_snake: ContainerChunkSnake,
                                         action: Action) -> Tuple[Chunk, int, int]:
        """
        Move the WrapperSnake optimally by moving the last chunk of container_chunk_snake to be the first chunk

        :param container_chunk_snake:
        :param action:
        :return:
        """

        chunk_snake_first: Chunk = container_chunk_snake.get_chunk_first()

        # print(container_chunk_snake._deque_chunk)
        # print(chunk_snake_first)
        # print()

        x_chunk_head_new = chunk_snake_first.x
        y_chunk_head_new = chunk_snake_first.y

        chunk_snake_last_to_move_possible: Chunk = container_chunk_snake.pop_chunk_last()

        # print(chunk_snake_last_to_move_possible)
        # print()

        # time_delta = time.time() - time_previous

        if action == Action.RIGHT:
            x_chunk_head_new += self.settings.block_size
        elif action == Action.LEFT:
            x_chunk_head_new -= self.settings.block_size
        elif action == Action.DOWN:
            y_chunk_head_new += self.settings.block_size
        elif action == Action.UP:
            y_chunk_head_new -= self.settings.block_size

        # Save x and y position of chunk_snake_last_to_move_possible
        x_chunk_last_old = chunk_snake_last_to_move_possible.x
        y_chunk_last_old = chunk_snake_last_to_move_possible.y

        chunk_snake_last_to_move_possible.x = x_chunk_head_new
        chunk_snake_last_to_move_possible.y = y_chunk_head_new

        return chunk_snake_last_to_move_possible, x_chunk_last_old, y_chunk_last_old

    # def get_collided(self, chunk: Chunk) -> bool:
    #     """
    #     Check if a chunk has collided with something in the logic_game_snake
    #
    #     Notes:
    #         1. Check if the chunk_front is colliding
    #
    #     :param chunk:
    #     :return:
    #     """
    #
    #     # Collision with boundary
    #     if (chunk.x > self.window_width - self.settings.block_size or
    #             chunk.x < 0 or
    #             chunk.y > self.window_height - self.settings.block_size or
    #             chunk.y < 0):
    #         return True
    #
    #     # for snake in self.data_game.list_wrapper_snake:
    #     #     if snake.get_container_chunk_snake().is_chunk_in_snake(chunk):
    #     #         return True
    #
    #     return False

    def get_generator_run_step(self) -> Generator[DataGame, None, None]:
        """

        :param callback_for_iteration_end: Callback function to run_loop
        :return:
        """
        # self.data_game.deque_player = deque(self.data_game.list_player)

        #
        # if callback_for_iteration_end is None:
        #     def callback_does_nothing():
        #         pass
        #
        #     callback_for_iteration_end = callback_does_nothing
        #

        # Loop control over WrapperSnake for fine control
        while self.data_game.deque_player:

            player: Player = self.data_game.deque_player.popleft()

            action_from_player: Action = player.get_action_new(self.data_game)

            print("ACTION FROM PLAYER", action_from_player)

            data_player = self.play_step_player(
                player,
                action_from_player
            )

            # This call must be made before the continue
            player.send_feedback_of_step(self.data_game, data_player)

            if data_player.bool_dead is True:
                # Continue will skip re-adding player back to the deque
                continue

            self.data_game.deque_player.append(player)

            yield self.data_game

        # for player in self.data_game.list_player:
        #
        #     action_from_player: Action = player.get_action_new(self.data_game)
        #
        #     print("ACTION FROM PLAYER", action_from_player)
        #
        #     data_player = self.play_step_player(
        #         player,
        #         action_from_player
        #     )
        #
        #     callback_for_iteration_end()
        #
        #     if data_player.bool_dead is True:
        #         # Continue will skip re-adding deque_player back
        #         continue
        #
        #     player.send_feedback_of_step(self.data_game, data_player)
        #
        #     yield self.data_game

        # return self.data_game

# def main():
#     game = LogicGameSnake()
#
#     game.run_loop()
#
#
# if __name__ == '__main__':
#     main()
#     # print(type(pygame))
