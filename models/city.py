#!/usr/bin/python3
"""the city class templates"""

from models.base_model import BaseModel


class City(BaseModel):
    """a city class that inherits from the class BaseModel

    Attributes:
        state_id (str): the state id
        name (str): the city's name
    """

    state_id = ''
    name = ''
