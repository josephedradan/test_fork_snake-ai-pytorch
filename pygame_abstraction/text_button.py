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
from pygame_abstraction.text import Text


class TextButton(Text):
    surface_text: pygame.Surface
    surface_text_hover: pygame.Surface

    def __init__(self,
                 text: str,
                 position_center: TYPE_POSITION,
                 font_text: pygame.font.Font,
                 color_text: ColorRGB,
                 color_text_hover: ColorRGB,
                 color_background: ColorRGB = ColorRGB.BLACK,
                 color_background_hover: ColorRGB = ColorRGB.WHITE):

        super().__init__(text,
                         position_center,
                         font_text,
                         color_text,
                         color_text_hover,
                         color_background,
                         color_background_hover)

        self.surface_text = self.font_text.render(self.text, True, self.color_text)
        self.surface_text_hover = self.font_text.render(self.text, True, self.color_text_hover)

        # Rectangle used for positioning
        self.pygame_rect_positioning = self.surface_text.get_rect(
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
                position[0] in range(self.pygame_rect_positioning.left, self.pygame_rect_positioning.right)
                and position[1] in range(self.pygame_rect_positioning.top, self.pygame_rect_positioning.bottom)
        )


    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface_text, self.pygame_rect_positioning)

    def draw_hover(self, surface: pygame.Surface):
        surface.blit(self.surface_text_hover, self.pygame_rect_positioning)
