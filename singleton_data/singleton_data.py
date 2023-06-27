"""
Date created: 6/26/2023

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

from abc import ABC
from abc import abstractmethod
from typing import Dict
from typing import Type


class SingletonData(ABC):
    """"
    Simple singleton parent class that will force subclasses to only be singletons
    """
    dict_k_type_singleton_data_v_instance: Dict[Type[SingletonData], SingletonData] = {}

    def __new__(cls, *args, **kwargs):
        if cls.dict_k_type_singleton_data_v_instance.get(cls) is None:
            cls.dict_k_type_singleton_data_v_instance[cls] = (
                super(SingletonData, cls).__new__(cls, *args, **kwargs)
            )

        return cls.dict_k_type_singleton_data_v_instance[cls]

    @abstractmethod
    def reset(self):
        ...