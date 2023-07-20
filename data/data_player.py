"""
Date created: 7/16/2023

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
from data.data import Data


class DataPlayer(Data):

    def __init__(self):
        """
        Simple Player data object container
        """

        """
        ####################
        variables that track
        ####################
        """

        self.score_highest = 0
        self.score_total = 0

        """
        ####################
        variables that change
        ####################
        """

        self.score = 0
        self.counter_play_step_since_last_food = 0

    def reset(self):
        self.score = 0
        self.counter_play_step_since_last_food = 0

