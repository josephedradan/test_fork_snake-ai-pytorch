"""
Date created: 6/15/2023

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
from abc import ABC
from abc import abstractmethod

from _settings import Settings


class GameSnake(ABC):
    settings: Settings

    def __init__(self, settings: Settings):
        self.settings = settings

    @abstractmethod
    def run(self):
        ...
