"""
Date created: 7/29/2023

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
from typing import Union

import numpy as np

from chunk import Chunk
from constants import Action
from constants import TYPE_NP_NDARRAY_GAME_STATE_13
from data.data_game import DataGame
from game_state.generator_game_state import GeneratorGameState
from player.player import Player
from utility import get_bool_wrapper_from_chunk_that_collided
from utility import get_chunk_possible_from_wrappers
from wrapper.wrapper import Wrapper


class GeneratorGameStateFoodSingle_ExperimentalV1(GeneratorGameState):  # NOQA

    @staticmethod
    def get_game_state(data_game: DataGame, player: Player[Wrapper]) -> TYPE_NP_NDARRAY_GAME_STATE_13:
        """

        Notes:
            7/31/2023
                Indicating that a possible action that will result in a collision on food will probably
                make a model/agent that uses this game state avoid food. The previous statement may
                not be entirely true, more tests need to be conducted.

        :param data_game:
        :param player:
        :return:
        """
        chunk_snake_head: Chunk = player.get_wrapper().get_container_chunk().get_chunk_first()  # NOQA

        chunk_pseudo_left = Chunk(chunk_snake_head.x - data_game.settings.block_size, chunk_snake_head.y)
        chunk_pseudo_right = Chunk(chunk_snake_head.x + data_game.settings.block_size, chunk_snake_head.y)
        chunk_pseudo_up = Chunk(chunk_snake_head.x, chunk_snake_head.y - data_game.settings.block_size)
        chunk_pseudo_down = Chunk(chunk_snake_head.x, chunk_snake_head.y + data_game.settings.block_size)

        bool_action_left = player.get_action() == Action.LEFT
        bool_action_right = player.get_action() == Action.RIGHT
        bool_action_up = player.get_action() == Action.UP
        bool_action_down = player.get_action() == Action.DOWN

        #####

        # Selecting a food to target
        chunk_food_possible: Union[Chunk, None] = get_chunk_possible_from_wrappers(data_game.list_wrapper_food)

        #####

        # Collisions with anything
        bool_collision_right = get_bool_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_right)
        bool_collision_left = get_bool_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_left)
        bool_collision_up = get_bool_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_up)
        bool_collision_down = get_bool_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_down)

        #####
        """
        Notes:
            Shape is (13,)

            Output:
                [
                    Snake going forward (from snake's perspective), check if next move going forward will collide,
                    Snake going forward (from snake's perspective), check if next move going right will collide,
                    Snake going forward (from snake's perspective), check if next move going left will collide,
                    is Current direction (from global perspective) moving left,
                    is Current direction (from global perspective) moving right,
                    is Current direction (from global perspective) moving up,
                    is Current direction (from global perspective) moving down,
                    chunk_food_possible is left of chunk_snake_head,
                    chunk_food_possible is right of chunk_snake_head,
                    chunk_food_possible is up of chunk_snake_head,
                    chunk_food_possible is down of chunk_snake_head,
                    chunk_food_possible is on chunk_snake_head on horizontal,
                    chunk_food_possible is on chunk_snake_head on vertical
                ]

        """
        state = [
            # Snake going forward (from snake's perspective), check if next move going forward will collide
            (bool_action_right and bool_collision_right) or
            (bool_action_left and bool_collision_left) or
            (bool_action_up and bool_collision_up) or
            (bool_action_down and bool_collision_down),

            # Snake going forward (from snake's perspective), check if next move going right will collide
            (bool_action_up and bool_collision_right) or
            (bool_action_down and bool_collision_left) or
            (bool_action_left and bool_collision_up) or
            (bool_action_right and bool_collision_down),

            # Snake going forward (from snake's perspective), check if next move going left will collide
            (bool_action_down and bool_collision_right) or
            (bool_action_up and bool_collision_left) or
            (bool_action_right and bool_collision_up) or
            (bool_action_left and bool_collision_down),

            # Selected Action
            bool_action_left,
            bool_action_right,
            bool_action_up,
            bool_action_down,

            # chunk_snake_head global position relative to chunk_food_possible
            chunk_food_possible.x < chunk_snake_head.x if chunk_food_possible is not None else False,
            chunk_food_possible.x > chunk_snake_head.x if chunk_food_possible is not None else False,
            chunk_food_possible.y < chunk_snake_head.y if chunk_food_possible is not None else False,
            chunk_food_possible.y > chunk_snake_head.y if chunk_food_possible is not None else False,
            chunk_food_possible.x == chunk_snake_head.x if chunk_food_possible is not None else False,
            chunk_food_possible.y == chunk_snake_head.y if chunk_food_possible is not None else False,

        ]

        print("*** DEBUG STATE ****")
        print("F Collide", state[0])
        print("R Collide", state[1])
        print("L Collide", state[2])
        print("L Going", state[3])
        print("R Going", state[4])
        print("U Going", state[5])
        print("D Going", state[6])
        print("FOOD X < HEAD X", state[7])
        print("FOOD X > HEAD X", state[8])
        print("FOOD Y < HEAD Y", state[9])
        print("FOOD Y > HEAD Y", state[10])
        print("FOOD X == HEAD X", state[11])
        print("FOOD Y == HEAD Y", state[12])
        print()

        return np.array(state, dtype=int)
