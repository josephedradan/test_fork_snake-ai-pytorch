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
from typing import Callable
from typing import Deque
from typing import List
from typing import Tuple
from typing import Union

from _settings import Settings
from chunk import Chunk
from container_chunk.container_chunk_snake import ContainerChunkSnake
from player import Player
from player_controller import PlayerController
from util import Action
from wrapper.wrapper import Wrapper
from wrapper.wrapper_food import WrapperFood
from wrapper.wrapper_snake import WrapperSnake
from wrapper.wrapper_wall import WrapperWall


class GameSnake:
    settings: Settings
    amount_of_block_width: int
    amount_of_block_height: int

    list_wrapper_snake: List[WrapperSnake]
    list_wrapper_food: List[WrapperFood]
    list_wrapper_wall: List[WrapperWall]

    index_frame: int

    def __init__(self,
                 # pygame_surface_main: pygame.display,
                 # window_width: int,
                 # window_height: int,
                 # pygame_font_text: pygame.font.Font,
                 # pygame_font_fps: pygame.font.Font
                 settings: Settings,
                 amount_of_block_width,
                 amount_of_block_height,
                 ):
        """

        :param width:
        :param height:
        """

        self.settings = settings

        self.amount_of_block_width = amount_of_block_width
        self.amount_of_block_height = amount_of_block_height

        """ 
        #################### 
        Menu related stuff 
        #################### 
        """

        self.list_wrapper_snake = []
        self.list_wrapper_food = []
        self.list_wrapper_wall = []

        self.reset()

    def reset(self):

        self.list_wrapper_wall.clear()
        self.list_wrapper_snake.clear()
        self.list_wrapper_food.clear()

        ##########

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

        self.list_wrapper_wall.append(wrapper_wall_border)

        ##########

        player: Player = PlayerController(Action.RIGHT)  # TODO: REUSE OBJECTS

        snake: WrapperSnake = WrapperSnake(  # TODO: REUSE OBJECTS
            player,
            [Chunk(640 // 2, 480 // 2)]  # Initial position_center
        )

        self.list_wrapper_snake.append(snake)

        ##########

        wrapper_food: WrapperFood = WrapperFood()  # TODO: REUSE OBJECTS

        self.list_wrapper_food.append(wrapper_food)

        self.index_frame = 0

        for wrapper_food in self.list_wrapper_food:
            self._place_food(wrapper_food)

    def _place_food(self, wrapper_food: WrapperFood,
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
                    for wrapper_selected in itertools.chain(self.list_wrapper_snake,
                                                            self.list_wrapper_food,
                                                            self.list_wrapper_wall)]):
                wrapper_food.get_container_chunk().add_new_chunk(chunk_food)
                return chunk_food

        # Fallback if randomness can't find a valid position to add chunk_food to a wrapper_food
        for width in range(self.amount_of_block_width):
            for height in range(self.amount_of_block_height):

                chunk_food.x = width * self.settings.block_size
                chunk_food.y = height * self.settings.block_size

                # If chunk_food not in all list_wrapper, then chunk_food can be added to the wrapper
                if all([chunk_food not in wrapper_selected.get_container_chunk()
                        for wrapper_selected in itertools.chain(self.list_wrapper_snake,
                                                                self.list_wrapper_food,
                                                                self.list_wrapper_wall)]):
                    wrapper_food.get_container_chunk().add_new_chunk(chunk_food)
                    return chunk_food

    def play_step(self, wrapper_snake: WrapperSnake, action_from_player: Action):
        self.index_frame += 1
        bool_game_over = False
        reward = 0

        # time_previous = time.time()

        container_chunk_snake = wrapper_snake.get_container_chunk()

        chunk_snake_to_move_possible, x_chunk_snake_last_old, y_chunk_snake_last_old = self.get_chunk_snake_to_move_possible(
            # time_previous,
            container_chunk_snake,
            action_from_player
        )

        # TODO: MOVE THIS CHECKING SOMEWHERELSE + REDISGN
        ####################
        # Collision checking
        ####################
        wrapper_object_that_collided: Union[Wrapper, None] = self.get_wrapper_from_chunk_that_collided(
            chunk_snake_to_move_possible
        )

        # Check collision wrapper_snake with food
        if isinstance(wrapper_object_that_collided, WrapperFood):
            wrapper_snake.score += 1

            self._place_food(wrapper_object_that_collided, chunk_snake_to_move_possible)

            # Extend the current wrapper_snake
            wrapper_snake.get_container_chunk().add_new_chunk(
                Chunk(x_chunk_snake_last_old, y_chunk_snake_last_old)

            )

        # Collision wrapper_snake with wrapper_snake (Does not care about which wrapper_snake)
        if isinstance(wrapper_object_that_collided, WrapperSnake):
            bool_game_over = True
            reward = -10
            return bool_game_over, reward, wrapper_snake

        # Check collision wrapper_snake with wall
        if isinstance(wrapper_object_that_collided, WrapperWall):
            bool_game_over = True
            reward = -10
            print("DED")
            return bool_game_over, reward, wrapper_snake

        # Move the wrapper_snake by placing chunk_snake_to_move_possible at the front of container_chunk_snake
        container_chunk_snake.add_new_chunk_front(chunk_snake_to_move_possible)

        # 6. return game_snake over and score
        return bool_game_over, reward, None  # TODO MAKE THIS BETTER, SNAKE DOES NTO EXIST

    def get_chunk_snake_to_move_possible(self, container_chunk_snake: ContainerChunkSnake, action: Action) -> Tuple[
        Chunk, int, int]:
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

    def get_wrapper_from_chunk_that_collided(self, chunk: Chunk) -> Union[Wrapper, None]:
        """
        Notes:
            If chunk collided with a wrapper, return that wrapper
            
        :param chunk:
        :return:
        """
        wrapper: Wrapper
        for wrapper in itertools.chain(self.list_wrapper_snake,
                                       self.list_wrapper_food,
                                       self.list_wrapper_wall):
            if chunk in wrapper.get_container_chunk():
                return wrapper

        return None

    # def get_collided(self, chunk: Chunk) -> bool:
    #     """
    #     Check if a chunk has collided with something in the game_snake
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
    #     # for snake in self.list_wrapper_snake:
    #     #     if snake.get_container_chunk_snake().is_chunk_in_snake(chunk):
    #     #         return True
    #
    #     return False

    def run(self, callback_end_call_for_iteration: Union[Callable, None] = None):
        """


        :param callback_end_call_for_iteration: Callback function to run
        :return:
        """
        deque_wrapper: Deque[WrapperSnake] = deque(self.list_wrapper_snake)

        if callback_end_call_for_iteration is None:
            def callback_does_nothing():
                pass

            callback_end_call_for_iteration = callback_does_nothing

        while deque_wrapper:

            wrapper_snake: WrapperSnake = deque_wrapper.popleft()

            action_from_player: Action = wrapper_snake.get_player().get_action_new()

            game_over, _, _ = self.play_step(wrapper_snake, action_from_player)

            if game_over is True:
                continue

            deque_wrapper.append(wrapper_snake)

            callback_end_call_for_iteration()

        for snake in self.list_wrapper_snake:
            print('Final Score', snake.score)


def main():
    game = GameSnake()

    game.run()


if __name__ == '__main__':
    main()
    # print(type(pygame))
