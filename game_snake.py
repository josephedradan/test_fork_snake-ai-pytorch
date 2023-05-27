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
from typing import Deque
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union

from _settings import Settings
from chunk import Chunk
from collidable.collidable import Collidable
from collidable.collidable_food import CollidableFood
from collidable.collidable_snake import CollidableSnake
from collidable.collidable_wall import CollidableWall
from container_chunk.container_chunk_snake import ContainerChunkSnake
from player import Player
from player_controller import PlayerController
from util import Action


class GameSnake:
    settings: Settings
    amount_of_block_width: int
    amount_of_block_height: int

    list_collidable_snake: List[CollidableSnake]
    list_collidable_food: List[CollidableFood]
    list_collidable_wall: List[CollidableWall]

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

        self.list_collidable_snake = []
        self.list_collidable_food = []
        self.list_collidable_wall = []

        self.reset()

    def reset(self):

        self.list_collidable_wall.clear()
        self.list_collidable_snake.clear()
        self.list_collidable_food.clear()

        ##########

        collidable_wall_border: CollidableWall = CollidableWall()

        # Create horizontal walls
        for i in range(self.amount_of_block_width + 1):
            x_start = i * self.settings.block_size
            y_start = self.amount_of_block_height * self.settings.block_size

            collidable_wall_border.get_container_chunk().add_new_chunk(Chunk(x_start, 0))
            collidable_wall_border.get_container_chunk().add_new_chunk(Chunk(x_start, y_start))

        # Create vertical walls
        for i in range(1, self.amount_of_block_height):
            x_start = self.amount_of_block_width * self.settings.block_size
            y_start = i * self.settings.block_size

            collidable_wall_border.get_container_chunk().add_new_chunk(Chunk(0, y_start))
            collidable_wall_border.get_container_chunk().add_new_chunk(Chunk(x_start, y_start))

        self.list_collidable_wall.append(collidable_wall_border)

        ##########

        player: Player = PlayerController(Action.RIGHT)  # TODO: REUSE OBJECTS

        snake: CollidableSnake = CollidableSnake(  # TODO: REUSE OBJECTS
            player,
            [Chunk(640 // 2, 480 // 2)]  # Initial position_center
        )

        self.list_collidable_snake.append(snake)

        ##########

        collidable_food: CollidableFood = CollidableFood()  # TODO: REUSE OBJECTS

        self.list_collidable_food.append(collidable_food)

        self.index_frame = 0

        for collidable_food in self.list_collidable_food:
            self._place_food(collidable_food)

    def _place_food(self, collidable_given: Collidable, chunk_collided_opposing: Union[Chunk, None] = None) -> Chunk:
        """
        Place food by reusing the same food object
        
        :param collidable_given:
        :param chunk_collided_opposing:
        :return: 
        """
        if chunk_collided_opposing is None:
            chunk_food = Chunk(0, 0)

        else:
            chunk_food = collidable_given.get_container_chunk().remove_chunk(chunk_collided_opposing)

        # n amount of tries to add a new chunk to collidable_given
        for _ in range(3):

            x = random.randint(0, self.amount_of_block_width) * self.settings.block_size
            y = random.randint(0, self.amount_of_block_height) * self.settings.block_size

            chunk_food.x = x
            chunk_food.y = y

            # If chunk_food not in all list_collidable, then food can be created
            if all([chunk_food not in collidable_selected.get_container_chunk()
                    for collidable_selected in itertools.chain(self.list_collidable_snake,
                                                               self.list_collidable_food,
                                                               self.list_collidable_wall)]):
                collidable_given.get_container_chunk().add_new_chunk(chunk_food)
                return chunk_food

        # Fallback, add chunk_food to a collidable_given via double for loop
        for width in range(self.amount_of_block_width):
            for height in range(self.amount_of_block_height):

                chunk_food.x = width * self.settings.block_size
                chunk_food.y = height * self.settings.block_size

                # If chunk_food not in all list_collidable, then food can be created
                if all([chunk_food not in collidable_selected.get_container_chunk()
                        for collidable_selected in itertools.chain(self.list_collidable_snake,
                                                                   self.list_collidable_food,
                                                                   self.list_collidable_wall)]):
                    collidable_given.get_container_chunk().add_new_chunk(chunk_food)
                    return chunk_food

    def play_step(self, collidable_snake: Collidable, action_from_player: Action):
        self.index_frame += 1
        bool_game_over = False
        reward = 0

        # time_previous = time.time()

        container_chunk_snake = collidable_snake.get_container_chunk()

        chunk_snake_to_move_possible, x_chunk_snake_last_old, y_chunk_snake_last_old = self.get_chunk_snake_to_move_possible(
            # time_previous,
            container_chunk_snake,
            action_from_player
        )

        # TODO: MOVE THIS CHECKING SOMEWHERELSE + REDISGN
        ####################
        # Collision checking
        ####################
        collidable_object: Union[Collidable, None] = self.get_collidable_from_chunk_that_collided(
            chunk_snake_to_move_possible
        )

        # Check collision collidable_snake with food
        if isinstance(collidable_object, CollidableFood):
            collidable_snake.score += 1

            self._place_food(collidable_object, chunk_snake_to_move_possible)

            # Extend the current collidable_snake
            collidable_snake.get_container_chunk().add_new_chunk(
                Chunk(x_chunk_snake_last_old, y_chunk_snake_last_old)

            )

        # Collision collidable_snake with collidable_snake (Does not care about which collidable_snake)
        if isinstance(collidable_object, CollidableSnake):
            bool_game_over = True
            reward = -10
            return bool_game_over, reward, collidable_snake

        # Check collision collidable_snake with wall
        if isinstance(collidable_object, CollidableWall):
            bool_game_over = True
            reward = -10
            print("DED")
            return bool_game_over, reward, collidable_snake

        # Move the collidable_snake by placing chunk_snake_to_move_possible at the front of container_chunk_snake
        container_chunk_snake.add_new_chunk_front(chunk_snake_to_move_possible)

        # 6. return game_snake over and score
        return bool_game_over, reward, None  # TODO MAKE THIS BETTER, SNAKE DOES NTO EXIST

    def get_chunk_snake_to_move_possible(self, container_chunk_snake: ContainerChunkSnake, action: Action) -> Tuple[
        Chunk, int, int]:
        """
        Move the CollidableSnake optimally by moving the last chunk of container_chunk_snake to be the first chunk

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

    def get_collidable_from_chunk_that_collided(self, chunk: Chunk) -> Union[Collidable, None]:
        """
        Notes:
            If chunk collided with a collidable, return that collidable
            
        :param chunk:
        :return:
        """
        collidable: Collidable
        for collidable in itertools.chain(self.list_collidable_snake,
                                          self.list_collidable_food,
                                          self.list_collidable_wall):
            if chunk in collidable.get_container_chunk():
                return collidable

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
    #     # for snake in self.list_collidable_snake:
    #     #     if snake.get_container_chunk_snake().is_chunk_in_snake(chunk):
    #     #         return True
    #
    #     return False

    def run(self):

        deque_collidable: Deque[CollidableSnake] = deque(self.list_collidable_snake)

        while deque_collidable:

            collidable_snake: CollidableSnake = deque_collidable.popleft()

            action_from_player: Action = collidable_snake.get_player().get_action()

            game_over, _, _ = self.play_step(collidable_snake, action_from_player)

            if game_over is True:
                continue

            deque_collidable.append(collidable_snake)

        for snake in self.list_collidable_snake:
            print('Final Score', snake.score)


def main():
    game = GameSnake()

    game.run()


if __name__ == '__main__':
    main()
    # print(type(pygame))
