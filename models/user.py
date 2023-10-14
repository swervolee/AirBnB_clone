#!/usr/bin/python3
"""
a class user
"""
import models
from models.base_model import BaseModel


class User(BaseModel):
    """
    defines a class user
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
