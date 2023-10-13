#!/usr/bin/python3
"""
A console for the Hbnb
"""
import sys
import cmd
import models
from models.base_model import BaseModel
from datetime import datetime
from models import storage


class HBNBCommand(cmd.Cmd):
    """Hbnb commandline"""

    prompt = "(hbnb) " if sys.__stdin__.isatty() else ""

    class_list = {"BaseModel": BaseModel}

    def do_EOF(self, signal):
        """
        Exits the program upon EOF signal which is ctrl + d
        """
        print("")
        return True

    def preloop(self):
        """
        Prints the prompt only if isatty is false
        """
        if not sys.__stdin__.isatty():
            print("(hbnb)")

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

    def do_show(self, cmd=None):
        """
        Prints the string representation of an instance
        given the class name and the instance id
        """

        name, id = None, None
        dc = storage.all()

        if cmd:
            cmd_list = cmd.split(" ")
            if len(cmd_list) >= 1:
                name = cmd_list[0]

            if len(cmd_list) >= 2:
                id = cmd_list[1]


        if not cmd:
            print("** class name is  missing **")

        elif not name or name not in self.class_list:
            print("** class doesnt exist **")

        elif not id:
            print("** instance id missing **")

        elif f"{name}.{id}" not in dc:
            print("** no instance found **")

        else:
            print(dc[f"{name}.{id}"])

    def do_destroy(self, cmd=None):
        """
        Destroys an instance based on class name and
        instance id
        """

        name, id = None, None
        all_objects = storage.all()
        if cmd:
            cmd_list = cmd.split(" ")
            if len(cmd_list) >= 1:
                name = cmd_list[0]
            if len(cmd_list) >= 2:
                id = cmd_list[1]

        if not name:
            print("** class name missing **")
        elif not id:
            print("** instance id mising **")
        elif f"{name}.{id}" not in all_objects:
            print("** no instance found **")
        else:
            all_objects.pop(f"{name}.{id}")
            storage.save()

    def do_all(self, cmd=None):
        """
        Prints all instances of the class name is absent
        else prints all the instances of the given class
        """
        all_objects = storage.all()

        if not cmd:
            for k in all_objects:
                print(all_objects[k])



































if __name__ == "__main__":
    HBNBCommand().cmdloop()
