#!/usr/bin/python3
"""the constructor to create a unique FileStorage
instance for the application in the models directory"""

from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
