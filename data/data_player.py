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
        self.score = 0
        self.counter_play_step = 0

    def reset(self):
        self.score = 0
        self.counter_play_step = 0
