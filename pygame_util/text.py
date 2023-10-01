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
from typing import List

import pygame

from constants import ColorRGB
from constants import ColorRGBPossible
from constants import TYPE_POSITION


class Text(ABC):
    text: str

    position_center: TYPE_POSITION
    font_text: pygame.font

    bool_toggled: bool

    color_text: ColorRGB
    color_hover: ColorRGB
    color_text_clicked: ColorRGB
    color_text_toggled: ColorRGB

    color_background: ColorRGB
    color_background_hover: ColorRGB
    color_background_clicked: ColorRGB
    color_background_toggled: ColorRGB

    surface_text: pygame.Surface
    surface_text_hover: pygame.Surface
    surface_text_clicked: pygame.Surface
    surface_text_toggled: pygame.Surface

    # surface_text: pygame.Surface

    def __init__(self,
                 text: str,
                 position_center: TYPE_POSITION,
                 font_text: pygame.font.Font,
                 color_text: ColorRGB,
                 color_text_hover: ColorRGB,
                 color_text_clicked: ColorRGB,
                 color_text_toggled: ColorRGB,
                 color_background: ColorRGBPossible = None,
                 color_background_hover: ColorRGBPossible = None,
                 color_background_clicked: ColorRGBPossible = None,
                 color_background_toggled: ColorRGBPossible = None,

                 ):
        self.text = text

        self.position_center = position_center
        self.font_text = font_text

        self.color_text = color_text
        self.color_text_hover = color_text_hover
        self.color_text_clicked = color_text_clicked
        self.color_text_toggled = color_text_toggled

        self.color_background = color_background
        self.color_background_hover = color_background_hover
        self.color_background_clicked = color_background_clicked
        self.color_background_toggled = color_background_toggled

        self.surface_text = self.font_text.render(
            self.text,
            True,
            self.color_text,
            self.color_background
        )
        self.surface_text_hover = self.font_text.render(
            self.text,
            True,
            self.color_text_hover,
            self.color_background_hover
        )
        self.surface_text_clicked = self.font_text.render(
            self.text,
            True,
            self.color_text_clicked,
            self.color_background_clicked
        )
        self.surface_text_toggled = self.font_text.render(
            self.text,
            True,
            self.color_text_toggled,
            self.color_background_toggled
        )

        #####

        self.bool_toggled = False

        self.set_text(self.text)

    @abstractmethod
    def is_position_colliding(self, position: TYPE_POSITION) -> bool:
        ...

    @abstractmethod
    def draw(self, surface: pygame.Surface, list_event: List[pygame.event.Event], position: TYPE_POSITION):
        ...

    # @abstractmethod
    # def draw_hover(self, surface: pygame.Surface):
    #     ...

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

    def set_text(self, text: str):
        self.text = text

        self.surface_text = self.font_text.render(
            self.text,
            True,
            self.color_text,
            self.color_background
        )
        self.surface_text_hover = self.font_text.render(
            self.text,
            True,
            self.color_text_hover,
            self.color_background_hover
        )
        self.surface_text_clicked = self.font_text.render(
            self.text,
            True,
            self.color_text_clicked,
            self.color_background_clicked
        )
        self.surface_text_toggled = self.font_text.render(
            self.text,
            True,
            self.color_text_toggled,
            self.color_background_toggled
        )
