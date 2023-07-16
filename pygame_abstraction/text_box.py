"""
Date created: 7/14/2023

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
from typing import List
from typing import Sequence
from typing import Union

import pygame

from constants import ColorRGB
from constants import TYPE_POSITION
from pygame_abstraction.text import Text


class TextBox(Text):
    color_text_active: ColorRGB
    color_background_active: ColorRGB

    def __init__(self,
                 text: str,
                 position_center: TYPE_POSITION,
                 font_text: pygame.font.Font,
                 color_text: ColorRGB,
                 color_text_hover: ColorRGB,
                 color_background: ColorRGB,
                 color_background_hover: ColorRGB,
                 color_text_active: ColorRGB,
                 color_background_active: ColorRGB,
                 ):
        super().__init__(text,
                         position_center,
                         font_text,
                         color_text,
                         color_text_hover,
                         color_background,
                         color_background_hover)

        self.color_text_active = color_text_active
        self.color_background_active = color_background_active

        self.list_char: List[str] = []

        #####

        self.surface_text = self.font_text.render(f"{self.text}{''.join(self.list_char)}",
                                                  True,
                                                  self.color_text
                                                  )

        # Rectangle used for positioning
        self.pygame_rect_positioning = self.surface_text.get_rect(
            center=(
                self.position_center[0],
                self.position_center[1]
            )
        )

    def is_position_colliding(self, position: TYPE_POSITION) -> bool:
        return (
                position[0] in range(self.pygame_rect_positioning.left, self.pygame_rect_positioning.right)
                and position[1] in range(self.pygame_rect_positioning.top, self.pygame_rect_positioning.bottom)
        )

    def draw(self, surface: pygame.Surface):
        self._draw_helper(
            surface,
            self.color_text,
            self.color_background,
        )

    def draw_hover(self, surface: pygame.Surface):
        self._draw_helper(
            surface,
            self.color_text_hover,
            self.color_background_hover,
        )

    def draw_active(self, surface: pygame.Surface):
        self._draw_helper(
            surface,
            self.color_text_active,
            self.color_background_active,
        )

    def _draw_helper(self,
                     surface: pygame.Surface,
                     color_foreground: ColorRGB,
                     color_background: ColorRGB
                     ):
        self.surface_text = self.font_text.render(f"{self.text}{''.join(self.list_char)}",
                                                  True,
                                                  color_foreground
                                                  )

        # Rectangle used for positioning
        self.pygame_rect_positioning = self.surface_text.get_rect(
            center=(
                self.position_center[0],
                self.position_center[1]
            )
        )

        pygame.draw.rect(surface, color_background, self.pygame_rect_positioning)

        surface.blit(self.surface_text, self.pygame_rect_positioning)

    def append_to_list_char(self, char: str):
        self.list_char.append(char)

    def extend_to_list_char(self, sequence: Sequence):
        self.list_char.extend(sequence)

    def get_list_char(self) -> List[str]:
        return self.list_char

    def pop_list_char(self) -> Union[str, None]:
        if self.list_char:
            return self.list_char.pop()
        return None
