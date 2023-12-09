#!/usr/bin/python3
"""the Review class templates"""

from models.base_model import BaseModel


class Review(BaseModel):
    """the review class that inherits from the class BaseModel

    Attributes:
        place_id (str): The Place's id.
        user_id (str): The User's id.
        text (str): The text of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
