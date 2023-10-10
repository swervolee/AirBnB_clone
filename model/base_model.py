#!/usr/bin/python3
"""
a base class
"""
import uuid
from datetime import datetime


class BaseModel():
    """
    a base class for the AirBnB for Dolls
    anything for dolls
    """
    def __init__(self):
        """
        innitializes an instance variables

        Args:
            id - the id of the created instance
            created_at - the time at which  the object was created
            updated_at - the time at which the object was updated
        """
        self.id = uuid.uuid4()
        self.created_at = datetime.today()
        self.updated_at = self.created_at

    def __str__(self):
        """
        returns a string representatio of the class
        """
        return (f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")

    def save(self):
        """
        updates the updated_at public instance variable to the current
        time
        """
        self.updated_at = datetime.today()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values of __dict
        """
        store = self.__dict__.copy()

        store.update({"__class__": self.__class__.__name__,
                      "created_at": self.created_at.isoformat(),
                      "updated_at": self.updated_at.isoformat()
                      })
        return store
