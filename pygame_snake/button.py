"""
Date created: 5/19/2023

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
    HOW TO MAKE A MENU SCREEN IN PYGAME!
        Notes:
        Reference:
            https://www.youtube.com/watch?v=GMBqjxcKogA
            https://github.com/baraltech/Menu-System-PyGame/blob/main/button.py
"""

import pygame

from constants import ColorRGB
from constants import TYPE_POSITION


class Button:
    text: str
    position_center: TYPE_POSITION
    font: pygame.font
    color: ColorRGB
    color_hover: ColorRGB

    surface_text: pygame.Surface

    def __init__(self,
                 text: str,
                 position_center: TYPE_POSITION,
                 font_text: pygame.font.Font,
                 color: ColorRGB,
                 color_hover: ColorRGB
                 ):
        self.text = text
        self.position_center = position_center
        self.font = font_text

        self.color = color
        self.color_hover = color_hover

        self.surface_text = self.font.render(self.text, True, self.color)
        self.surface_text_hover = self.font.render(self.text, True, self.color_hover)

        # Rectangle where to place the text onto
        self.rectangle_button = self.surface_text.get_rect(
            center=(
                self.position_center[0],
                self.position_center[1]
            )
        )

    def is_position_colliding(self, position: TYPE_POSITION) -> bool:
        """
        Check if a given position is in this object's hit box basically

        :param position:
        :return:
        """
        return (
                position[0] in range(self.rectangle_button.left, self.rectangle_button.right)
                and position[1] in range(self.rectangle_button.top, self.rectangle_button.bottom)
        )

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface_text, self.rectangle_button)

    def draw_hover(self, surface: pygame.Surface):
        surface.blit(self.surface_text_hover, self.rectangle_button)
