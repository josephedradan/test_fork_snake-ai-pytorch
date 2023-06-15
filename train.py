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
from agent import Agent
from game_state.generator_game_state import GeneratorGameState
from game_state.generator_game_state_food_single import GeneratorGameStateFoodSingle
from helper import plot
from player_ai import PlayerAI
from pygame_graphics_game_snake import GraphicsPygame


# TODO: Generalize to GraphicsGameSnake, might not need graphics too
def train(pygame_graphics_game_state: GraphicsPygame, generator_game_state: GeneratorGameState):
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = PlayerAI()


    while True:

        generator_game_state.get_game_state()

        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short deque_memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long deque_memory, plot result
            game.reset()
            agent.amount_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('PlayerController', agent.amount_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.amount_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train(GeneratorGameStateFoodSingle)
