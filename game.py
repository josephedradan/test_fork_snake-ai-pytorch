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
from typing import List
from typing import Tuple
from typing import Union

import pygame

from chunk import Chunk
from collidable.collidable import Collidable
from collidable.collidable_food import CollidableFood
from collidable.collidable_snake import CollidableSnake
from collidable.collidable_wall import CollidableWall
from container_chunk.container_chunk_snake import ContainerChunkSnake
from player import Player
from player_controller import PlayerController
from util import Action
from util import BLOCK_SIZE
from util import BLOCK_SIZE_OFFSET
from util import ColorRGB
from util import FONT_SIZE
from util import FPS


class GameSnake():
    window_width: int
    window_height: int

    pygame_display: pygame.display
    clock: pygame.time.Clock

    list_collidable_snake: List[CollidableSnake]
    list_collidable_food: List[CollidableFood]
    list_collidable_wall: List[CollidableWall]
    index_frame: int

    amount_of_block_width: int
    amount_of_block_height: int

    def __init__(self, width=640, height=480):
        """

        :param width:
        :param height:
        """

        """
        ####################
        Pygame related stuff
        ####################
        """

        self.window_width = width
        self.window_height = height

        pygame.init()

        # font_text = pygame.font_text.SysFont('arial', 25)
        # font_text = pygame.font_text.Font('arial.ttf', 25)

        self.font_text = pygame.font.Font('arial.ttf', FONT_SIZE)
        self.font_fps = pygame.font.Font('arial.ttf', FONT_SIZE)

        self.pygame_display: pygame.display = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )

        pygame.display.set_caption('Snake game')
        self.clock = pygame.time.Clock()

        """ 
        #################### 
        Pre calculated stuff 
        #################### 
        """

        # Amount of blocks available for width and height
        self.amount_of_block_width = (self.window_width - BLOCK_SIZE) // BLOCK_SIZE
        self.amount_of_block_height = (self.window_height - BLOCK_SIZE) // BLOCK_SIZE

        """ 
        #################### 
        Game related stuff 
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
            x_start = i * BLOCK_SIZE
            y_start = self.amount_of_block_height * BLOCK_SIZE

            collidable_wall_border.get_container_chunk().add_new_chunk(Chunk(x_start, 0))
            collidable_wall_border.get_container_chunk().add_new_chunk(Chunk(x_start, y_start))

        # Create vertical walls
        for i in range(1, self.amount_of_block_height):
            x_start = self.amount_of_block_width * BLOCK_SIZE
            y_start = i * BLOCK_SIZE

            collidable_wall_border.get_container_chunk().add_new_chunk(Chunk(0, y_start))
            collidable_wall_border.get_container_chunk().add_new_chunk(Chunk(x_start, y_start))

        self.list_collidable_wall.append(collidable_wall_border)

        ##########

        player: Player = PlayerController(Action.RIGHT)  # TODO: REUSE OBJECSTS

        snake: CollidableSnake = CollidableSnake(  # TODO: REUSE OBJECSTS
            player,
            [Chunk(self.window_width // 2, self.window_height // 2)]  # Initial position
        )

        self.list_collidable_snake.append(snake)

        ##########

        collidable_food: CollidableFood = CollidableFood()  # TODO: REUSE OBJECSTS

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

            x = random.randint(0, self.amount_of_block_width) * BLOCK_SIZE
            y = random.randint(0, self.amount_of_block_height) * BLOCK_SIZE

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

                chunk_food.x = width * BLOCK_SIZE
                chunk_food.y = height * BLOCK_SIZE

                # If chunk_food not in all list_collidable, then food can be created
                if all([chunk_food not in collidable_selected.get_container_chunk()
                        for collidable_selected in itertools.chain(self.list_collidable_snake,
                                                                   self.list_collidable_food,
                                                                   self.list_collidable_wall)]):
                    collidable_given.get_container_chunk().add_new_chunk(chunk_food)
                    return chunk_food

    def draw_graphics(self):
        """
        Draw collidable_snake game

        Notes:
            The order of draws determines if something is drawn on top of something.

        :return:
        """
        self.pygame_display.fill(ColorRGB.BLACK)

        # Draw walls
        for collidable_wall in self.list_collidable_wall:
            for chunk_wall in collidable_wall.get_container_chunk():
                pygame.draw.rect(
                    self.pygame_display,
                    ColorRGB.GRAY,
                    pygame.Rect(chunk_wall.x, chunk_wall.y, BLOCK_SIZE, BLOCK_SIZE)
                )

        # Draw snakes
        for index, collidable_snake in enumerate(self.list_collidable_snake):
            pygame.draw.rect(
                self.pygame_display,
                ColorRGB.GREEN_KELLY,
                pygame.Rect(collidable_snake.get_container_chunk()[0].x + BLOCK_SIZE_OFFSET,
                            collidable_snake.get_container_chunk()[0].y + BLOCK_SIZE_OFFSET,
                            BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2),
                            BLOCK_SIZE - (BLOCK_SIZE_OFFSET * 2))
            )

            for chunk in itertools.islice(collidable_snake.get_container_chunk(), 1,
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
                # pygame.draw.rect(
                #     self.pygame_display,
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
        for collidable_food in self.list_collidable_food:
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

        pygame.display.flip()

    def play_step(self):
        game_over = False

        # time_previous = time.time()

        for snake in self.list_collidable_snake:

            # Get Direction from player
            action: Action = snake.get_player().get_action()

            container_chunk_snake = snake.get_container_chunk()

            # Get chunk to move
            chunk_snake_to_move, x_chunk_last_old, y_chunk_last_old = self.do_get_chunk_thing(
                # time_previous,
                container_chunk_snake,
                action
            )

            # self.player_snake.list_point_snake.insert(0, point_head)
            # print(point_head, action)

            # 3. check if game over
            # if self.get_collided(container_chunk_snake):
            #     game_over = True
            #     return game_over, self.score

            # chunk_front = container_chunk_snake[0]

            ####################
            # Collision checking
            ####################

            collidable_object: Union[Collidable, None] = self.get_collidable_from_chunk(chunk_snake_to_move)

            # Check if collision with self

            # Collision with collidable_given
            if isinstance(collidable_object, CollidableFood):
                snake.score += 1

                self._place_food(collidable_object, chunk_snake_to_move)  # TODO HERE

                # Extend the current snake
                snake.get_container_chunk().add_new_chunk(
                    Chunk(x_chunk_last_old, y_chunk_last_old)

                )

            # Collision with snake (Does not care about which snake)
            if isinstance(collidable_object, CollidableSnake):
                game_over = True
                return game_over

            if isinstance(collidable_object, CollidableWall):
                game_over = True
                return game_over

            # Move the snake by placing chunk_snake_to_move at the front of container_chunk_snake
            container_chunk_snake.add_new_chunk_front(chunk_snake_to_move)

            # Update ui and clock
            self.draw_graphics()
            self.clock.tick(FPS)

        # 6. return game over and score
        return game_over

    def do_get_chunk_thing(self, container_chunk_snake: ContainerChunkSnake, action: Action) -> Tuple[Chunk, int, int]:
        """
        Move the CollidableSnake

        Notes:
            1. Get the first chunk
            2. Get the position of the first chunk and modify it
            3. Pop the last chunk
            4. Modify the last chunk's position
            5. append left the last chunk

        :param time_previous:
        :param action:
        :return: Tuple of the previous x y positions of the last chunk of the container_chunk_snake
        """

        chunk_head: Chunk = container_chunk_snake.get_chunk_first()

        print(container_chunk_snake._deque_chunk)
        print(chunk_head)
        print()

        x_chunk_head_new = chunk_head.x
        y_chunk_head_nex = chunk_head.y

        chunk_last: Chunk = container_chunk_snake.pop_chunk_last()

        print(chunk_last)
        print()

        # time_delta = time.time() - time_previous

        if action == Action.RIGHT:
            x_chunk_head_new += BLOCK_SIZE
        elif action == Action.LEFT:
            x_chunk_head_new -= BLOCK_SIZE
        elif action == Action.DOWN:
            y_chunk_head_nex += BLOCK_SIZE
        elif action == Action.UP:
            y_chunk_head_nex -= BLOCK_SIZE

        x_chunk_last_old = chunk_last.x
        y_chunk_last_old = chunk_last.y

        chunk_last.x = x_chunk_head_new
        chunk_last.y = y_chunk_head_nex

        return chunk_last, x_chunk_last_old, y_chunk_last_old

    def get_collidable_from_chunk(self, chunk: Chunk) -> Union[Collidable, None]:

        collidable: Collidable
        for collidable in itertools.chain(self.list_collidable_snake, self.list_collidable_food,
                                          self.list_collidable_wall):
            if chunk in collidable.get_container_chunk():
                return collidable

        return None

    def get_collided(self, chunk: Chunk) -> bool:
        """
        Check if a chunk has collided with something in the game

        Notes:
            1. Check if the chunk_front is colliding

        :param chunk:
        :return:
        """

        # Collision with boundary
        if (chunk.x > self.window_width - BLOCK_SIZE or
                chunk.x < 0 or
                chunk.y > self.window_height - BLOCK_SIZE or
                chunk.y < 0):
            return True

        # for snake in self.list_collidable_snake:
        #     if snake.get_container_chunk_snake().is_chunk_in_snake(chunk):
        #         return True

        return False

    def run(self):

        while True:
            game_over = self.play_step()

            if game_over is True:
                break

        for snake in self.list_collidable_snake:
            print('Final Score', snake.score)


def main():
    pygame.init()

    game = GameSnake()

    game.run()

    pygame.quit()


if __name__ == '__main__':
    main()
    # print(type(pygame))
