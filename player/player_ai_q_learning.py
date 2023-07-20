from typing import Dict
from typing import Type
from typing import Union

from agent.agent_q_learning import AgentQLearning
from constants import Action
from constants import TYPE_ACTION_POSSIBLE
from constants import TYPE_GAME_STATE
from constants import TYPE_TUPLE_INT_ACTION
from data.data_game import DataGame
from data.data_play_step_result import DataPlayStepResult
from game_state.generator_game_state import GeneratorGameState
from game_state.generator_game_state_food_single import GeneratorGameStateFoodSingle
from helper import plot
from player.player import Player
from utility import get_action_from_tuple_int_action_relative
from wrapper.wrapper import Wrapper
from wrapper.wrapper_food import WrapperFood
from wrapper.wrapper_snake import WrapperSnake
from wrapper.wrapper_wall import WrapperWall

# pygame.init()
# font_text = pygame.font_text.Font('../arial.ttf', 25)

DICT_K_TYPE_WRAPPER_V_REWARD: Dict[Type[Wrapper], int] = {
    WrapperFood: 10,
    WrapperSnake: -10,
    WrapperWall: -10
}


class PlayerAIQLearning(Player[WrapperSnake]):
    window_width: int
    window_height: int

    direction: Action

    frame_iteration: int

    def __init__(self, generator_game_state: Type[GeneratorGameState] = GeneratorGameStateFoodSingle):

        super().__init__()

        self.generator_game_state = generator_game_state
        self.agent_q_learning = AgentQLearning()

        """
        ####################
        Varying variables
        ####################
        """

        self.game_state: Union[TYPE_GAME_STATE, None] = None
        self.tuple_int_action_relative: Union[TYPE_TUPLE_INT_ACTION, None] = None

        #####

        self.plot_scores = []
        self.plot_scores_mean = []

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
        # PlayerKeyboard game_state related stuff
        # ####################
        # """
        #
        # self._initialize()

    def get_action_new(self, data_game: DataGame) -> TYPE_ACTION_POSSIBLE:

        # Get game game_state based on DataGame
        self.game_state = self.generator_game_state.get_game_state(data_game, self)

        # Get a custom tuple_int_action representation from the agent
        self.tuple_int_action_relative = self.agent_q_learning.get_tuple_int_action_relative(self.game_state)

        # Return the the correct Action object based on the custom tuple_int_action representation
        self.action = get_action_from_tuple_int_action_relative(self.action, self.tuple_int_action_relative)

        return self.action

    def _respond_to_data_play_step_result(self,
                                          data_game: DataGame,
                                          data_play_step_result: DataPlayStepResult,
                                          ) -> int:

        # If player collided
        if data_play_step_result.wrapper_object_that_collided is not None:

            # Assign the reward based on the collision
            reward = (
                DICT_K_TYPE_WRAPPER_V_REWARD.get(type(data_play_step_result.wrapper_object_that_collided), 0)
            )

        # Kill the player if the player is stalling
        elif self.get_data_player().counter_play_step_since_last_food > 100 * len(
                self.wrapper.get_container_chunk()):  # TODO CHANGE 100 TO SOMETHING ELSE
            data_play_step_result.bool_dead = True
            reward = -10

        else:
            reward = 0

        return reward

    def _do_reinforcement_learning_logic(self,
                                         data_game: DataGame,
                                         data_play_step_result: DataPlayStepResult,
                                         reward: int
                                         ):

        game_state_new = self.generator_game_state.get_game_state(data_game, self)

        self.agent_q_learning.train_short_memory(
            self.game_state,
            self.tuple_int_action_relative,
            reward,
            game_state_new,
            data_play_step_result.bool_dead,
        )

        self.agent_q_learning.remember(
            self.game_state,
            self.tuple_int_action_relative,
            reward,
            game_state_new,
            data_play_step_result.bool_dead,
        )

        if data_play_step_result.bool_dead:

            self.agent_q_learning.amount_games += 1
            self.agent_q_learning.train_long_memory()

            if self.data_player.score > self.data_player.score_highest:
                self.data_player.score_highest = self.data_player.score

                print("SAVE CALLED")
                # Save
                self.agent_q_learning.model.save()

            self.plot_scores.append(self.data_player.score)  # BLUE LINE
            self.data_player.score_total += self.data_player.score  # ORANGE LINE
            score_mean = self.data_player.score_total / self.agent_q_learning.amount_games
            self.plot_scores_mean.append(score_mean)
            plot(self.plot_scores, self.plot_scores_mean)

    def send_feedback_of_step(self,
                              data_game: DataGame,
                              data_play_step_result: DataPlayStepResult,
                              ):
        """

        :param data_game:
        :param data_play_step_result:
        :return:
        """

        reward = self._respond_to_data_play_step_result(data_game, data_play_step_result)

        self._do_reinforcement_learning_logic(data_game, data_play_step_result, reward)

    # def _place_food(self):
    #     x = random.randint(0, (self.window_width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    #     y = random.randint(0, (self.window_height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    #     self.food = Chunk(x, y)
    #     if self.food in self.list_point_snake:
    #         self._place_food()
    #
    # def play_step(self, torch_tensor_action):  # FIXME: ACTION IS IN FORMAT [0,0,0]
    #     self.frame_iteration += 1
    #
    #     # 1. collect user input
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             quit()
    #
    #     # 2. move
    #     self._move(torch_tensor_action)  # draw the chunk_head
    #     self.list_point_snake.insert(0, self.head)
    #
    #     # 3. check if logic_game_snake over
    #     torch_tensor_reward = 0
    #     game_over = False
    #     if self.is_collision() or self.frame_iteration > 100 * len(self.list_point_snake):
    #         game_over = True
    #         torch_tensor_reward = -10
    #         return torch_tensor_reward, game_over, self.score
    #
    #     # 4. place new chunk_food or just move
    #     if self.head == self.food:
    #         self.score += 1
    #         torch_tensor_reward = 10
    #         self._place_food()
    #     else:
    #         self.list_point_snake.pop_chunk_last()
    #
    #     # 5. draw ui and clock
    #     self._update_ui()
    #     self.clock.tick(GAME_SPEED)
    #
    #     # 6. return logic_game_snake over and score
    #     return torch_tensor_reward, game_over, self.score
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
    #     text = font_text.render("Score: " + str(self.score), True, ColorRGB.WHITE)
    #     self.display.blit(text, [0, 0])
    #     pygame.display.flip()
    #
    # def _move(self, torch_tensor_action):  # FIXME: ACTION IS IN FORMAT [0,0,0]
    #     """
    #     torch_tensor_action is a List of 3 ints representing [straight, right, left] WHICH IS [0,0,0]
    #
    #     :param torch_tensor_action:
    #     :return:
    #     """
    #
    #     clock_wise = [Action.RIGHT, Action.DOWN, Action.LEFT, Action.UP]
    #     idx = clock_wise.index(self.direction)
    #
    #     if np.array_equal(torch_tensor_action, [1, 0, 0]):
    #         new_dir: Action = clock_wise[idx]  # no change
    #     elif np.array_equal(torch_tensor_action, [0, 1, 0]):
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
