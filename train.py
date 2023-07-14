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
from typing import Type

from _settings import Settings
from agent import Agent
from game.game_snake import GameSnake
from game_state.generator_game_state import GeneratorGameState
from game_state.generator_game_state_food_single import GeneratorGameStateFoodSingle
from helper import plot
from player.player_ai_q_learning import PlayerAIQLearning


# TODO: Generalize to GraphicsGameSnake, might not need graphics too
def train(game_snake: GameSnake, settings: Settings,
          # generator_game_state: Type[GeneratorGameState]
          ):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    player = PlayerAIQLearning()

    game_snake = GameSnake(settings)



    while True:

        # get old game_state_current
        game_state = generator_game_state.get_game_state(game_snake, )  # TODO GET STATE

        # get old game_state_current
        # state_old = agent.get_state(game)

        # get move
        final_move = agent.get_tuple_int_action_relative(state_old)  # TODO GET ACTIOn

        # perform move and get new game_state_current
        reward, done, score = game.play_step(final_move) # TODO DO ACTION, GET SHIT FROM IT
        state_new = agent.get_state(game)  #

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)  # TODO THIS  state_new

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)  # TODO THIS  state_new

        if done:
            # train long deque_memory, plot result
            game._initialize()
            agent.amount_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('PlayerKeyboard', agent.amount_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.amount_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

#
# def callback():
#
#
#     state_previous:
#
#     def callback_body()



if __name__ == '__main__':
    train(GeneratorGameStateFoodSingle)
