"""
Date created: 5/24/2023

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
from constants import BLOCK_SIZE
from constants import BLOCK_SIZE_OFFSET
from constants import FONT_SIZE
from constants import GAME_SPEED


def get_dimension_corrected(block_size: int, dimension: int):
    """
    Given a block size, get the nearest factor dimension

    :param block_size:
    :param dimension:
    :return:
    """

    dimension_corrected = (dimension // block_size) * block_size

    return dimension_corrected


class Settings:

    def __init__(self,
                 width=640,
                 height=480,
                 block_size=BLOCK_SIZE,
                 block_size_offset=BLOCK_SIZE_OFFSET,
                 fps=GAME_SPEED,
                 font_size=FONT_SIZE,
                 text_line_spacing_offset=5,
                 ):
        """
        Settings files, pass this file around and it will be used throughout the application most likely

        :param width:
        :param height:
        :param block_size:
        :param block_size_offset:
        :param fps:
        :param font_size:
        :param text_line_spacing_offset:
        """
        self.block_size = block_size

        self.height = get_dimension_corrected(self.block_size, height)
        self.width = get_dimension_corrected(self.block_size, width)

        self.block_size_offset = block_size_offset
        self.fps = fps
        self.font_size = font_size

        #####
        self.text_line_spacing_offset = text_line_spacing_offset
        self.text_line_spacing_amount = self.font_size + self.text_line_spacing_offset
