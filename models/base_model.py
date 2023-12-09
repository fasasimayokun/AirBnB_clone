#!/usr/bin/python3
"""the BaseModel class module"""

from datetime import datetime
import uuid
import models


class BaseModel:
    """the basemodel class template for the Hbnb clone."""
    def __init__(self, *args, **kwargs):
        """the basemodel constructor for initialization of objects"""
        datime_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for ky, val in kwargs.items():
                if ky == "created_at" or ky == "updated_at":
                    self.__dict__[ky] = datetime.strptime(val, datime_format)
                else:
                    self.__dict__[ky] = val
        else:
            models.storage.new(self)

    def save(self):
        """the basemodel method that updates te updated_at
        attr with the current datetime"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """the basemodel method that returns the dictionary of each
        object __class__ representing the name of the class object"""
        basmod_dict = self.__dict__.copy()
        basmod_dict['created_at'] = self.created_at.isoformat()
        basmod_dict['updated_at'] = self.updated_at.isoformat()
        basmod_dict['__class__'] = self.__class__.__name__
        return basmod_dict

    def __str__(self):
        """the methods that returns the str represention
        of the basemodel objects"""
        cls_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)
