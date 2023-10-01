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
from constants import ColorRGBPossible
from constants import TYPE_POSITION
from pygame_util.text import Text


class TextBox(Text):
    color_text_active: ColorRGB
    color_background_active: ColorRGB

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
        super().__init__(
            text,
            position_center,
            font_text,
            color_text,
            color_text_hover,
            color_text_clicked,
            color_text_toggled,
            color_background,
            color_background_hover,
            color_background_clicked,
            color_background_toggled
        )

        self.color_text_active = color_text_toggled
        # self.color_background_active = color_background_active

        self.list_char: List[str] = []

        #####

        self.surface_text = self.font_text.render(
            f"{self.text}{''.join(self.list_char)}",
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

    def is_position_colliding(self,
                              position: TYPE_POSITION) -> bool:
        return (
                position[0] in range(self.pygame_rect_positioning.left, self.pygame_rect_positioning.right)
                and position[1] in range(self.pygame_rect_positioning.top, self.pygame_rect_positioning.bottom)
        )

    def draw(self, surface: pygame.Surface, list_event: List[pygame.event.Event], position: TYPE_POSITION):
        self._draw_helper(
            surface,
            list_event,
            position,
        )

    # def draw_hover(self, surface: pygame.Surface):
    #     self._draw_helper(
    #         surface,
    #         self.color_text_hover,
    #         self.color_background_hover,
    #     )
    #
    # def draw_active(self, surface: pygame.Surface):
    #     self._draw_helper(
    #         surface,
    #         self.color_text_active,
    #         self.color_background_active,
    #     )

    def _draw_helper(self,
                     surface: pygame.Surface,
                     list_event: List[pygame.event.Event],
                     position: TYPE_POSITION,
                     ):

        text = f"{self.text}{''.join(self.list_char)}"

        self.set_text(text)

        # Rectangle used for positioning
        self.pygame_rect_positioning = self.surface_text.get_rect(
            center=(
                self.position_center[0],
                self.position_center[1]
            )
        )

        # Draw rectangle on surface
        pygame.draw.rect(surface, ColorRGB.GRAY, self.pygame_rect_positioning)

        bool_pygame_event_type_mouse_button_down: bool = False

        # Any event handling stuff (Avoid putting heave code in here to reduce lag)
        for event in list_event:
            if event.type == pygame.MOUSEBUTTONDOWN:
                bool_pygame_event_type_mouse_button_down = True
                break

        # Clicked (Hovered, Clicked)
        if self.is_position_colliding(position) and bool_pygame_event_type_mouse_button_down:
            print("CLICKED")
            self.bool_toggled = not self.bool_toggled
            surface.blit(self.surface_text_clicked, self.pygame_rect_positioning)

        # Hovered (Hovered, Not Clicked)
        elif self.is_position_colliding(position):
            print("HOVER")
            surface.blit(self.surface_text_hover, self.pygame_rect_positioning)

        # Toggled (Toggled)
        elif self.bool_toggled:
            print("TOGGLED")
            surface.blit(self.surface_text_toggled, self.pygame_rect_positioning)

        # Default (Not Toggled, Not Clicked)
        else:
            print("DEFAULT")
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
