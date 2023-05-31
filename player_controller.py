from typing import Dict
from typing import Union

import pygame

from player import Player
from util import Action
from util import DICT_K_ACTION_V_ACTION_REVERSE

pygame.init()

font = pygame.font.Font('arial.ttf', 25)

# pygame_font_text = pygame.pygame_font_text.SysFont('arial', 25)

DICT_K_KEY_MOVEMENT_V_ACTION: Dict[int, Action] = {
    pygame.K_a: Action.LEFT,
    pygame.K_d: Action.RIGHT,
    pygame.K_w: Action.UP,
    pygame.K_s: Action.DOWN,
}


class PlayerController(Player):
    window_width: int
    window_height: int

    direction: Action

    def __init__(self, action_initial: Union[Action, None] = None):
        """
        :param width:
        :param height:
        """
        super().__init__(action_initial)
        # super().__init__(action_initial, x_initial, y_initial)

    #     # self.window_width = width
    #     # self.window_height = height
    #
    #     # Initialize Display
    #     self.pygame_surface_main: pygame.pygame_surface_main = pygame.pygame_surface_main.set_mode(
    #         (640, 480)
    #     )
    #
    #     pygame.pygame_surface_main.set_caption('Player')
    #     self.clock = pygame.time.Clock()
    #
    #     """
    #     ####################
    #     PlayerController state related stuff
    #     ####################
    #     """
    #
    #     # Initialize PlayerController State
    #     self.action_current: Action = Action.RIGHT
    #
    #     self.chunk_head: Chunk = Chunk(640 / 2, 480 / 2)
    #
    #     self.list_point_snake: List[Chunk] = [
    #         self.chunk_head,
    #         Chunk(self.chunk_head.x - BLOCK_SIZE, self.chunk_head.y),
    #         Chunk(self.chunk_head.x - (2 * BLOCK_SIZE), self.chunk_head.y)
    #     ]
    #
    #     self.score: int = 0
    #     self.chunk_food = None
    #     self._place_food()
    #
    # def _place_food(self):
    #     x = random.randint(0, (640 - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    #     y = random.randint(0, (480 - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    #     self.chunk_food = Chunk(x, y)
    #     if self.chunk_food in self.list_point_snake:
    #         self._place_food()

    def get_action_new(self) -> Action:

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_a:
            #         self.action_current = Action.LEFT
            #     elif event.key == pygame.K_d:
            #         self.action_current = Action.RIGHT
            #     elif event.key == pygame.K_w:
            #         self.action_current = Action.UP
            #     elif event.key == pygame.K_s:
            #         self.action_current = Action.DOWN

            if event.type == pygame.KEYDOWN:

                action_selected = DICT_K_KEY_MOVEMENT_V_ACTION.get(event.key, None)

                print("key", action_selected)

                """
                If the action_selected is not self.action and action_selected is not None
                
                Notes:
                    This should prevent moving back into yourself and 
                    not reassigning a unregistered action to self.action  
                """
                if DICT_K_ACTION_V_ACTION_REVERSE.get(action_selected) != self.action and action_selected is not None:
                    self.action = action_selected

        return self.action

#     def play_step(self):
#
#         # 1. collect user input
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_a:
#                     self.action_current = Action.LEFT
#                 elif event.key == pygame.K_d:
#                     self.action_current = Action.RIGHT
#                 elif event.key == pygame.K_w:
#                     self.action_current = Action.UP
#                 elif event.key == pygame.K_s:
#                     self.action_current = Action.DOWN
#
#         # 2. move
#         self.get_chunk_snake_to_move_possible(self.action_current)  # draw the chunk_head
#         self.list_point_snake.insert(0, self.chunk_head)
#
#         # 3. check if game_snake over
#         game_over = False
#         if self.get_collided():
#             game_over = True
#             return game_over, self.score
#
#         # 4. place new chunk_food or just move
#         if self.chunk_head == self.chunk_food:
#             self.score += 1
#             self._place_food()
#         else:
#             self.list_point_snake.pop_chunk_last()
#             print("POPPPED")
#
#         # 5. draw ui and clock
#         self.draw_graphics()
#         self.clock.tick(FPS)w
#
#         # 6. return game_snake over and score
#         return game_over, self.score
#
#     def draw_graphics(self):
#         self.pygame_surface_main.fill(ColorRGB.BLACK)
#
#         for pt in self.list_point_snake:
#             pygame.draw.rectangle_button(self.pygame_surface_main, ColorRGB.BLUE_1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
#             pygame.draw.rectangle_button(self.pygame_surface_main, ColorRGB.BLUE_2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
#
#         pygame.draw.rectangle_button(self.pygame_surface_main, ColorRGB.RED, pygame.Rect(self.chunk_food.x, self.chunk_food.y, BLOCK_SIZE, BLOCK_SIZE))
#
#         text = pygame_font_text.render("Score: " + str(self.score), True, ColorRGB.WHITE)
#         self.pygame_surface_main.blit(text, [0, 0])
#         pygame.pygame_surface_main.flip()
#
#     def get_collided(self) -> bool:
#
#         # hits boundary
#         if (self.chunk_head.x > 640 - BLOCK_SIZE or
#                 self.chunk_head.x < 0 or
#                 self.chunk_head.y > 480 - BLOCK_SIZE or
#                 self.chunk_head.y < 0):
#             return True
#
#         # hits itself
#         if self.chunk_head in self.list_point_snake[1:]:
#             return True
#
#         return False
#
#     def get_chunk_snake_to_move_possible(self, action_current: Action):
#
#         x = self.chunk_head.x
#         y = self.chunk_head.y
#         if action_current == Action.RIGHT:
#             x += BLOCK_SIZE
#         elif action_current == Action.LEFT:
#             x -= BLOCK_SIZE
#         elif action_current == Action.DOWN:
#             y += BLOCK_SIZE
#         elif action_current == Action.UP:
#             y -= BLOCK_SIZE
#
#         self.chunk_head = Chunk(x, y)
#
# if __name__ == '__main__':
#     game_snake = PlayerController(
#         Action.RIGHT,
#         640 // 2,
#         480 // 2,
#     )
#
#     # game_snake loop
#     while True:
#         game_over, score = game_snake.play_step()
#
#         if game_over == True:
#             break
#
#     print('Final Score', score)
#
#     pygame.quit()
