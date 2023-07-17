"""
Date created: 6/13/2023

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
from _settings import Settings
from game.game_snake_pygame import GameSnakePygame


def main():
    # settings = Settings(800, 600, amount_food=1)
    settings = Settings(200, 200, amount_food=1)

    game = GameSnakePygame(settings)

    game.run()


if __name__ == '__main__':
    main()
