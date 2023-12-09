#!/usr/bin/python3
"""the User class template"""

from models.base_model import BaseModel


class User(BaseModel):
    """a class User that inherits from the class BaseModel

    Attributes:
        email (str): the user's email
        password (str): the user's password
        first_name (str): the user's first Name
        last_name (str): the user's Last Name
    """

    email = ''
    password = ''
    first_name = ''
    last_name = ''
