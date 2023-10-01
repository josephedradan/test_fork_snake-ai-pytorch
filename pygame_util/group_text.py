"""
Date created: 8/2/2023

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
from typing import Union

from pygame_util.text import Text

# FIXME: This way is ugly, you have to double loop, 1 loop to check what is selected and whatever is using this object
#  and the other loop is check what which one is selected
class GroupText:
    list_text: List[Text]

    def __init__(self, list_text: List[Text]):
        self.list_text = list_text
        self.set_text = set(list_text)

        self.text_active: Union[Text, None] = None

    def get_selected(self) -> Text:
        return  # This way is ugly
