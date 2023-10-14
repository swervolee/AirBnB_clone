#!/usr/bin/python3
"""a storage class"""
import json
from models.base_model import BaseModel
from models.user import User


class FileStorage():
    """
    serializes and deserializes python objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns a dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        sets in __objects the obj with the key <obj class name>.id
        """
        name = obj.__class__.__name__
        FileStorage.__objects[f"{name}.{obj.id}"] = obj

    def save(self):
        """
        serializes FileStorage.__objects
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """
        deserializes a json file
        """
        try:
            name = FileStorage.__file_path
            deserialized = {}
            with open(name, "r") as file:
                dsr = json.load(file)
            for k, v in dsr.items():
                cls_name = v["__class__"]
                self.__objects[k] = eval(cls_name)(**v)
        except FileNotFoundError:
            pass
