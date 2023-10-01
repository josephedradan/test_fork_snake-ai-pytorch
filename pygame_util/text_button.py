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


    How to Create Menus in Python Games! (PyGame Tutorial)
        Reference:
            https://www.youtube.com/watch?v=Y52JsDs4cMQ


"""
from typing import List

import pygame

from constants import ColorRGB
from constants import TYPE_POSITION
from pygame_util.text import Text


class TextButton(Text):

    def __init__(self,
                 text: str,
                 position_center: TYPE_POSITION,
                 font_text: pygame.font.Font,
                 color_text: ColorRGB,
                 color_text_hover: ColorRGB,
                 color_text_clicked: ColorRGB,
                 color_text_toggled: ColorRGB,
                 color_background: ColorRGB,
                 color_background_hover: ColorRGB
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
            color_background_hover

        )

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

        # # Old Style
        # return (
        #         position[0] in range(self.pygame_rect_positioning.left, self.pygame_rect_positioning.right)
        #         and position[1] in range(self.pygame_rect_positioning.top, self.pygame_rect_positioning.bottom)
        # )

        return self.pygame_rect_positioning.collidepoint(position)

    def draw(self, surface: pygame.Surface, list_event: List[pygame.event.Event],position: TYPE_POSITION):
        """

        Notes:
            Pygame Event only register ONCE compared to other pygame methods such as
                pygame.mouse.get_pressed()[0]  # This can be useful for actual games and not menus
            which will register all the time

        :param surface:
        :param list_event:
        :param position:
        :return:
        """

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


    # def draw_hover(self, surface: pygame.Surface):
    #     surface.blit(self.surface_text_hover, self.pygame_rect_positioning)
