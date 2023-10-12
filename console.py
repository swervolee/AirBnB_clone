#!/usr/bin/python3
"""
A console for the Hbnb
"""
import cmd
import models
from models.base_model import BaseModel
from datetime import datetime


class HBNBCommand(cmd.Cmd):
    """Hbnb commandline"""

    prompt = "(hbnb) "

    class_list = {"BaseModel": BaseModel}

    def do_EOF(self, signal):
        """
        Exits the program upon EOF signal which is ctrl + d
        """
        print("")
        return True

    def do_quit(self, cmd):
        """
        Quit command to exit the program
        """
        return True

    def emptyline(self):
        """
        Does nothing to an empty line command
        """
        pass

    def do_create(self, cmd=None):
        """
        Creates a new instance of BaseModel saves it
        to json file and prints out the id of the instance
        """
        if not cmd:
            print("** class name missing **")
        elif cmd not in self.class_list:
            print("** class doesn't exist **")
        else:
            new = eval(cmd)()
            new.save()
            print(f"{new.id}")
















if __name__ == "__main__":
    HBNBCommand().cmdloop()
