"""
Date created: 5/24/2023

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
from constants import TYPE_GAME_STATE
from data.data_game import DataGame
from game_state.generator_game_state import GeneratorGameState
from player.player import Player
from utility import get_bool_wrapper_from_chunk_that_collided
from utility import get_wrapper_from_chunk_that_collided
from wrapper.wrapper_food import WrapperFood


class GeneratorGameStateFoodSingle(GeneratorGameState):

    @staticmethod
    def get_game_state(data_game: DataGame, player: Player) -> TYPE_GAME_STATE:
        chunk_snake_head: Chunk = player.get_wrapper().get_container_chunk().get_chunk_first()

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
        chunk_food: Union[Chunk, None] = None

        if data_game.list_wrapper_food:
            wrapper_food_arbitrary: WrapperFood = data_game.list_wrapper_food[0]

            container_chunk_food = wrapper_food_arbitrary.get_container_chunk()

            _dict_k_chunk_v_chunk = container_chunk_food.get_dict_k_chunk_v_chunk()

            if _dict_k_chunk_v_chunk:
                # WARNING : Potentially slow if there are a lot of keys
                chunk_food = tuple(_dict_k_chunk_v_chunk.keys())[0]


        # print("PLAYER", chunk_snake_head)
        # print("CHUNK L", chunk_pseudo_left)
        # print("CHUNK R", chunk_pseudo_right)
        # print("CHUNK U", chunk_pseudo_up)
        # print("CHUNK D", chunk_pseudo_down)
        # print("FOOD", chunk_food)

        #####

        wrapper_from_chunk_that_collided_right = get_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_right)
        wrapper_from_chunk_that_collided_left = get_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_left)
        wrapper_from_chunk_that_collided_up = get_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_up)
        wrapper_from_chunk_that_collided_down = get_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_down)

        # COLLISIONS WITH NOT FOOD
        bool_right = (
            False if wrapper_from_chunk_that_collided_right is None or
                     isinstance(wrapper_from_chunk_that_collided_right, WrapperFood) else True
        )

        bool_left = (
            False if wrapper_from_chunk_that_collided_left is None or
                     isinstance(wrapper_from_chunk_that_collided_left, WrapperFood) else True
        )

        bool_up = (
            False if wrapper_from_chunk_that_collided_up is None or
                     isinstance(wrapper_from_chunk_that_collided_up, WrapperFood) else True
        )

        bool_down = (
            False if wrapper_from_chunk_that_collided_down is None or
                     isinstance(wrapper_from_chunk_that_collided_down, WrapperFood) else True
        )

        # bool_right = get_bool_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_right)
        # bool_left = get_bool_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_left)
        # bool_up = get_bool_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_up)
        # bool_down = get_bool_wrapper_from_chunk_that_collided(data_game, chunk_pseudo_down)
        # print("B R",bool_right)
        # print("B L",bool_left)
        # print("B U",bool_up)
        # print("B D",bool_down)

        #####
        """
        Notes:
            
            Shape is (11,)
        
            Output:
                [
                    Snake going forward (from snake's perspective), check if next move going forward will collide,
                    Snake going forward (from snake's perspective), check if next move going right will collide,
                    Snake going forward (from snake's perspective), check if next move going left will collide,
                    is Current direction (from global perspective) moving left,
                    is Current direction (from global perspective) moving right,
                    is Current direction (from global perspective) moving up,
                    is Current direction (from global perspective) moving down,
                    chunk_food is left of chunk_snake_head,
                    chunk_food is right of chunk_snake_head,
                    chunk_food is up of chunk_snake_head,
                    chunk_food is down of chunk_snake_head,
                ]
            
        """
        state = [
            # Snake going forward (from snake's perspective), check if next move going forward will collide
            (bool_action_right and bool_right) or
            (bool_action_left and bool_left) or
            (bool_action_up and bool_up) or
            (bool_action_down and bool_down),

            # Snake going forward (from snake's perspective), check if next move going right will collide
            (bool_action_up and bool_right) or
            (bool_action_down and bool_left) or
            (bool_action_left and bool_up) or
            (bool_action_right and bool_down),

            # Snake going forward (from snake's perspective), check if next move going left will collide
            (bool_action_down and bool_right) or
            (bool_action_up and bool_left) or
            (bool_action_right and bool_up) or
            (bool_action_left and bool_down),

            # Selected Action
            bool_action_left,
            bool_action_right,
            bool_action_up,
            bool_action_down,

            # chunk_snake_head global position relative to chunk_food
            chunk_food.x < chunk_snake_head.x if chunk_food is not None else False,
            chunk_food.x > chunk_snake_head.x if chunk_food is not None else False,
            chunk_food.y < chunk_snake_head.y if chunk_food is not None else False,
            chunk_food.y > chunk_snake_head.y if chunk_food is not None else False,
            # chunk_food.x == chunk_snake_head.x if chunk_food is not None else False,
            # chunk_food.y == chunk_snake_head.y if chunk_food is not None else False,

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
        print()

        return np.array(state, dtype=int)
