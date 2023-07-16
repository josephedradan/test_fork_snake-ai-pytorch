"""
Date created: 5/19/2023

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
    How to efficiently hold a key in Pygame?
        Notes:
            event.get() VS key.get_pressed()

            Checkout
                pygame.key.set_repeat()  # Will register keys held down repeatedly as events

        IMPORTANT NOTES:
            pygame.key.set_repeat() IS NOT GOOD FOR MOVEMENT

        Reference:
            https://stackoverflow.com/questions/22093662/how-to-efficiently-hold-a-key-in-pygame

    pygame key.set_repeat not working
        Notes:
            "
            But note that you should not use set_repeat and the pygame.KEYDOWN event to implement movement.
            If you do, you won't be able to observe real single key strokes,
            since if the player presses a key, a whole bunch of pygame.KEYDOWN events would be created.

            Better use pygame.key.get_pressed().
            "
        Reference:
            https://stackoverflow.com/a/18998475
"""
from typing import Dict

import pygame
from pygame.key import ScancodeWrapper

from data.data_game import DataGame
from player.player import Player
from constants import Action
from constants import DICT_K_ACTION_V_ACTION_REVERSE

pygame.init()

# font_text = pygame.font_text.Font('../arial.ttf', 25)

# pygame_font_text = pygame.pygame_font_text.SysFont('arial', 25)

DICT_K_PYGAME_EVENT_KEY_V_ACTION: Dict[int, Action] = {
    pygame.K_a: Action.LEFT,
    pygame.K_d: Action.RIGHT,
    pygame.K_w: Action.UP,
    pygame.K_s: Action.DOWN,
}

LIST_K_PYGAME_EVENT_KEY = DICT_K_PYGAME_EVENT_KEY_V_ACTION.keys()


class PlayerKeyboard(Player):

    def __init__(self):
        """
        :param width:
        :param height:
        """
        super().__init__()

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
    #     PlayerKeyboard game_state related stuff
    #     ####################
    #     """
    #
    #     # Initialize PlayerKeyboard Condition
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

    # def get_action_new(self, data_game: DataGame) -> Action:  # FIXME HEAVILY TIED TO PYGAME
    #
    #     for event in data_game.list_pygame_event:
    #
    #         if event.type == pygame.KEYDOWN:
    #
    #             action_selected = DICT_K_PYGAME_EVENT_KEY_V_ACTION.get(event.key, None)
    #
    #             """
    #             If the action_selected is not self.tuple_int_action and action_selected is not None
    #
    #             Notes:
    #                 This should prevent moving back into yourself and
    #                 not reassigning a unregistered tuple_int_action to self.tuple_int_action
    #
    #                 Returning immediately will prevent an following events from being processed
    #                 e.g holding down 2 keys at the sametime
    #             """
    #             if DICT_K_ACTION_V_ACTION_REVERSE.get(action_selected) != self.tuple_int_action and action_selected is not None:
    #                 self.tuple_int_action = action_selected
    #                 return self.tuple_int_action
    #
    #     pygame.key.get_pressed()
    #
    #     return self.tuple_int_action

    def get_action_new(self, data_game: DataGame) -> Action:  # FIXME HEAVILY TIED TO PYGAME

        scan_code_wrapper_keys: ScancodeWrapper = pygame.key.get_pressed()

        # Order of events in LIST_K_PYGAME_EVENT_KEY determines priority
        for pygame_event_key in LIST_K_PYGAME_EVENT_KEY:

            if scan_code_wrapper_keys[pygame_event_key]:

                action_selected = DICT_K_PYGAME_EVENT_KEY_V_ACTION.get(pygame_event_key, None)

                """
                If the action_selected is not self.tuple_int_action and action_selected is not None
        
                Notes:
                    This should prevent moving back into yourself and
                    not reassigning a unregistered tuple_int_action to self.tuple_int_action
        
                    Returning immediately will prevent an following events from being processed
                    e.g holding down 2 keys at the sametime
                """
                if DICT_K_ACTION_V_ACTION_REVERSE.get(action_selected) != self.action and action_selected is not None:
                    self.action = action_selected
                    return self.action

        return self.action

# Old style
#     def play_step_player(self):
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
#         # 3. check if logic_game_snake over
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
#         self.clock.tick(GAME_SPEED)w
#
#         # 6. return logic_game_snake over and score
#         return game_over, self.score
#
#     def draw_graphics(self):
#         self.pygame_surface_main.fill(ColorRGB.BLACK)
#
#         for pt in self.list_point_snake:
#             pygame.draw.pygame_rect_positioning(self.pygame_surface_main, ColorRGB.BLUE_1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
#             pygame.draw.pygame_rect_positioning(self.pygame_surface_main, ColorRGB.BLUE_2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))
#
#         pygame.draw.pygame_rect_positioning(self.pygame_surface_main, ColorRGB.RED, pygame.Rect(self.chunk_food.x, self.chunk_food.y, BLOCK_SIZE, BLOCK_SIZE))
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
#     logic_game_snake = PlayerKeyboard(
#         Action.RIGHT,
#         640 // 2,
#         480 // 2,
#     )
#
#     # logic_game_snake loop
#     while True:
#         game_over, score = logic_game_snake.play_step_player()
#
#         if game_over == True:
#             break
#
#     print('Final Score', score)
#
#     pygame.quit()
