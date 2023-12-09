#!/usr/bin/python3
"""the State class templates"""

from models.base_model import BaseModel


class State(BaseModel):
    """the state class that inherits from the class BaseModel
    Attributes:
        name (str): The name of the state.
    """

    name = ''
