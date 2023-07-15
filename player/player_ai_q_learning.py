from typing import Type
from typing import Type
from typing import Union

from agent.agent_q_learning import AgentQLearning
from constants import Action
from constants import TYPE_ACTION_POSSIBLE
from constants import TYPE_GAME_STATE
from constants import TYPE_TUPLE_INT_ACTION
from data.data_game import DataGame
from data.data_player import DataPlayer
from game_state.generator_game_state import GeneratorGameState
from game_state.generator_game_state_food_single import GeneratorGameStateFoodSingle
from helper import plot
from player.player import Player
# def get_action_new
from utility import get_action_from_tuple_int_action_relative


# pygame.init()
# font_text = pygame.font_text.Font('../arial.ttf', 25)


class PlayerAIQLearning(Player):
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

        self.game_state_current: Union[TYPE_GAME_STATE, None] = None
        self.tuple_action_relative_current: Union[TYPE_TUPLE_INT_ACTION, None] = None

        #####

        self.plot_scores = []
        self.plot_scores_mean = []
        self.score_total = 0
        self.score_highest = 0

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
        # PlayerKeyboard game_state_current related stuff
        # ####################
        # """
        #
        # self._initialize()

    # def _initialize(self):
    #     # init logic_game_snake game_state_current
    #     self.action_current = Action.RIGHT
    #
    #     self.head = Chunk(self.window_width / 2, self.window_height / 2)
    #
    #     self.list_point_snake = [
    #         self.head,
    #         Chunk(self.head.x - BLOCK_SIZE, self.head.y),
    #         Chunk(self.head.x - (2 * BLOCK_SIZE), self.head.y)
    #     ]
    #
    #     self.score = 0
    #     self.chunk_food = None
    #     self._place_food()
    #     self.index_frame = 0

    def get_action_new(self, data_game: DataGame) -> TYPE_ACTION_POSSIBLE:

        # Get game game_state based on DataGame
        self.game_state_current = self.generator_game_state.get_game_state(data_game, self)

        # Get a custom torch_tensor_action representation from the agent
        self.tuple_action_relative_current = self.agent_q_learning.get_tuple_int_action_relative(self.game_state_current)

        # Return the the correct Action object based on the custom torch_tensor_action representation
        self.action = get_action_from_tuple_int_action_relative(self.action, self.tuple_action_relative_current)

        return self.action

    def send_feedback_of_step(self,
                              data_game: DataGame,
                              data_player: DataPlayer,
                              ):

        game_state_new = self.generator_game_state.get_game_state(data_game, self)

        self.agent_q_learning.train_short_memory(
            self.game_state_current,
            self.get_action_current(),
            data_player.reward,
            game_state_new,
            data_player.bool_dead,
        )

        self.agent_q_learning.remember(
            self.game_state_current,
            self.get_action_current(),
            data_player.reward,
            game_state_new,
            data_player.bool_dead,
        )

        print("####### data_player.bool_dead", data_player.bool_dead)

        if data_player.bool_dead:

            self.agent_q_learning.amount_games += 1
            self.agent_q_learning.train_long_memory()

            if self.score > self.score_highest:
                self.score_highest = self.score

                print("SAVE CALLED")
                # Save
                self.agent_q_learning.model.save()

            self.plot_scores.append(self.score)
            self.score_total += self.score
            score_mean = self.score_total / self.agent_q_learning.amount_games
            self.plot_scores_mean.append(score_mean)
            plot(self.plot_scores, self.plot_scores_mean)

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
    #     self.clock.tick(FPS)
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
