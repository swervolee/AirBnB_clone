#!/usr/bin/python3
"""a storage class"""
import json
from models.base_model import BaseModel


class FileStorage():
    """
    serializes and deserializes python objects
    """
    __file_path = file.json
    __objects = {}

    def all(self):
        """
        returns a dictionary __objects
        """
        return __objects

    def new(self, obj):
        """
        sets in __objects the obj with the key <obj class name>.id
        """
        dc = obj.to_dict()
        File_storage[dc.__class__ + "." + dc.id] = obj

    def save(self):
        """
        serializes FileStorage.__objects
        """
        sr = FileStorage.__objects
        fname = FileStorage.__file_path
        new = {k: v.to_dict for k, v in sr}
        with open(fname, "w") as file:
            json.dump(data, file)

    def reload(self):
        """
        deserializes a json file
        """
        name = FileStorage.__file_path
        try:
            deserialized = {}
            with open(name, "r") as file:
                dsr = json.load(file)
            for k, v in dsr.items():
                name = v["__class__"]
                FileStorage.__objects[k] = name(v)
        except FileNotFoundError:
            pass
