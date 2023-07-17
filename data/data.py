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
from abc import ABC
from abc import abstractmethod


class Data(ABC):

    @abstractmethod
    def reset(self):
        ...