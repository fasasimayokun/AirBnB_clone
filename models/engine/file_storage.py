#!/usr/bin/python3
"""the filestorage class module"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """the filestorage class template with 2 class attributes"""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """the filestorage method that returns the dict __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """the filestorage method that set in __objects obj with
        key <obj_class_name>.id"""
        insclsnm = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(insclsnm, obj.id)] = obj

    def save(self):
        """the filestorage method that serialize _objects to the JSON file
        __file_path."""
        obdict = FileStorage.__objects
        insdict = {obj: obdict[obj].to_dict() for obj in obdict.keys()}
        with open(FileStorage.__file_path, 'w') as fle:
            json.dump(insdict, fle)

    def reload(self):
        """the filestorage method that deserialize the JSON file _file_path
        to __objects, if it is present"""
        try:
            with open(FileStorage.__file_path) as fle:
                insdict = json.load(fle)
                for ins in insdict.values():
                    clnam = ins['__class__']
                    del ins['__class__']
                    self.new(eval(clnam)(**ins))
        except FileNotFoundError:
            return
