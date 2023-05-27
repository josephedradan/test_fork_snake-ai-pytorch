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
from collidable.collidable_snake import CollidableSnake
from game_snake import GameSnake
from game_state.game_state import GameState
from player import Player


class GameStateSingleFood(GameState):

    def __init__(self, game_snake: GameSnake):
        super().__init__(game_snake)

    def generate_game_state(self, collidable_snake: CollidableSnake):



        head = self.game_state.list_point_snake[0]
        point_l = Chunk(head.x - 20, head.y)
        point_r = Chunk(head.x + 20, head.y)
        point_u = Chunk(head.x, head.y - 20)
        point_d = Chunk(head.x, head.y + 20)

        dir_l = self.game_state.direction == Action.LEFT
        dir_r = self.game_state.direction == Action.RIGHT
        dir_u = self.game_state.direction == Action.UP
        dir_d = self.game_state.direction == Action.DOWN

        """
        Notes:
            dir_ is the current direction relative to the global
            point_ is relative to dir_ and is the direction that will lead to the comment "Danger ..."

            so,

            [
                Snake going forward (from snake's perspective), check if next move going forward will collide
                Snake going forward (from snake's perspective), check if next move going right will collide 
                Snake going forward (from snake's perspective), check if next move going left will collide
                is Current direction (from global perspective) moving left,
                is Current direction (from global perspective) moving right,
                is Current direction (from global perspective) moving up,
                is Current direction (from global perspective) moving down,
                food


        """
        state = [
            # Snake going forward (from snake's perspective), check if next move going forward will collide
            (dir_r and self.game_state.is_collision(point_r)) or
            (dir_l and self.game_state.is_collision(point_l)) or
            (dir_u and self.game_state.is_collision(point_u)) or
            (dir_d and self.game_state.is_collision(point_d)),

            # Snake going forward (from snake's perspective), check if next move going right will collide
            (dir_u and self.game_state.is_collision(point_r)) or
            (dir_d and self.game_state.is_collision(point_l)) or
            (dir_l and self.game_state.is_collision(point_u)) or
            (dir_r and self.game_state.is_collision(point_d)),

            # Snake going forward (from snake's perspective), check if next move going left will collide
            (dir_d and self.game_state.is_collision(point_r)) or
            (dir_u and self.game_state.is_collision(point_l)) or
            (dir_r and self.game_state.is_collision(point_u)) or
            (dir_l and self.game_state.is_collision(point_d)),

            # Move action_current
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # CollidableFood location
            self.game_state.food.x < self.game_state.point_head.x,  # chunk_food left
            self.game_state.food.x > self.game_state.point_head.x,  # chunk_food right
            self.game_state.food.y < self.game_state.point_head.y,  # chunk_food up
            self.game_state.food.y > self.game_state.point_head.y  # chunk_food down
        ]

        return np.array(state, dtype=int)