"""
Date created: 4/29/2023

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

from __future__ import annotations


class Chunk:
    __slots__ = ("x", "y")
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, chunk: Chunk):
        return self.x == chunk.x and self.y == chunk.y

    def __str__(self):
        return f"{Chunk.__name__}({self.x, self.y})"
