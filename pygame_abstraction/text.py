"""
Date created: 7/15/2023

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

import pygame

from constants import ColorRGB
from constants import TYPE_POSITION


class Text(ABC):
    text: str
    position_center: TYPE_POSITION
    font_text: pygame.font
    color_text: ColorRGB
    color_hover: ColorRGB
    color_background: ColorRGB
    color_background_hover: ColorRGB

    # surface_text: pygame.Surface

    def __init__(self,
                 text: str,
                 position_center: TYPE_POSITION,
                 font_text: pygame.font.Font,
                 color_text: ColorRGB,
                 color_text_hover: ColorRGB,
                 color_background: ColorRGB,
                 color_background_hover: ColorRGB
                 ):

        self.text = text
        self.position_center = position_center
        self.font_text = font_text

        self.color_text = color_text
        self.color_text_hover = color_text_hover
        self.color_background_hover = color_background_hover
        self.color_background = color_background

    @abstractmethod
    def is_position_colliding(self, position: TYPE_POSITION) -> bool:
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface):
        ...

    @abstractmethod
    def draw_hover(self, surface: pygame.Surface):
        ...

    # def is_position_colliding(self, position: TYPE_POSITION) -> bool:
    #     """
    #     Check if a given position is in this object's hit box basically
    #
    #     :param position:
    #     :return:
    #     """
    #     return (
    #             position[0] in range(self.pygame_rect_positioning.left, self.pygame_rect_positioning.right)
    #             and position[1] in range(self.pygame_rect_positioning.top, self.pygame_rect_positioning.bottom)
    #     )
    #
    #
    # def draw(self, surface: pygame.Surface):
    #     surface.blit(self.surface_text, self.pygame_rect_positioning)
    #
    # def draw_hover(self, surface: pygame.Surface):
    #     surface.blit(self.surface_text_hover, self.pygame_rect_positioning)
