#!/usr/bin/python3
"""
A console for the Hbnb
"""
import cmd
import sys
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import models
from datetime import datetime


class HBNBCommand(cmd.Cmd):
    """Hbnb commandline"""

    prompt = "(hbnb) " if sys.__stdin__.isatty() else ""

    class_list = {"BaseModel": BaseModel, "User": User,
                  "Place": Place, "State": State,
                  "City": City, "Amenity": Amenity,
                  "Review": Review}
    dots = ["all", "count", "show", "destroy", "update"]

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

    def help_create(self):
        """
        Help information for the create command
        """
        print("Creates a new instance")
        print("[Usage]: create <className>")

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
            print("** class doesn't exist **")

        elif not id:
            print("** instance id missing **")

        elif f"{name}.{id}" not in dc:
            print("** no instance found **")

        else:
            print(dc[f"{name}.{id}"])

    def help_show(self):
        """
        Help info for the show command
        """
        print("Displays a single instance")
        print("[Usage]: show <ClassName> <Id>\n")

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
        elif name not in self.class_list:
            print("** class doesn't exist **")
        elif f"{name}.{id}" not in all_objects:
            print("** no instance found **")
        else:
            all_objects.pop(f"{name}.{id}")
            storage.save()

    def help_destroy(self):
        """
        help info for the destroy command
        """
        print("Destroys a class instance")
        print("[usage] destroy <className> <ObjectId>\n")

    def do_all(self, arg=None):
        """
        Prints all instances of the class name is absent
        else prints all the instances of the given class
        """
        if not arg:
            print([str(v) for k, v in models.storage.all().items()])
        else:
            if not self.class_list.get(arg):
                print("** class doesn't exist **")
                return False
            print([str(v) for k, v in models.storage.all().items()
                   if type(v) is self.class_list.get(arg)])

    def help_all(self):
        """
        Help for the all command
        """
        print("Prints all object instances of a command")
        print("[usage]: all <ClassName>\n")

    def do_update(self, cmd=None):
        """
        Updates a class with new attributes
        or new values
        """
        cls_name, id, attr_name, attr_val = None, None, None, None
        all_objects = storage.all()

        arg_tuple = cmd.partition(" ")
        if arg_tuple[0]:
            cls_name = arg_tuple[0]
        else:
            print("** class name missing **")
            return

        if cls_name not in self.class_list:
            print("** class doesn't exist **")
            return

        arg_tuple = arg_tuple[2].partition(" ")
        if arg_tuple[0]:
            id = arg_tuple[0]
        else:
            print("** instance id missing **")
            return

        key = f"{cls_name}.{id}"

        if key not in storage.all():
            print("** no instance found **")
            return
        item_dict = all_objects[key]

        if '{' in arg_tuple[2] and '}' in arg_tuple[2] and type(eval(arg_tuple[2])) is dict:
            cmd_list = []
            for k, v in eval(arg_tuple[2]).items():
                cmd_list.append(k)
                cmd_list.append(v)
        else:
            arg = arg_tuple[2]
            if arg and arg[0] == "\"":
                limit = arg.find("\"", 1)
                attr_name = arg[1:limit]
                arg = arg[limit + 1]
            arg = arg.partition(" ")

            if not attr_name and arg[0] != " ":
                attr_name = arg[0]
            if arg[2] and arg[2][0] == "\"":
                attr_val = arg[2][1: arg[2].find("\"", 1)]
            if arg[2] and not attr_val:
                attr_val = arg[2].partition(" ")[0]
            cmd_list = [attr_name, attr_val]
        for i in range(len(cmd_list)):
            if i % 2 == 0:
                attr_name, attr_value = cmd_list[i], cmd_list[i + 1]
                if not attr_name:
                    print("** attribute name missing **")
                    return
                if not attr_value:
                    print("** value missing **")
                    return
                if hasattr(eval(cls_name)(), attr_name):
                    attr_value = type(getattr(eval(cls_name), attr_name))(attr_value)
                setattr(item_dict, attr_name, attr_value)
                item_dict.save()

    def help_update(self):
        """
        Help information for updating class
        """
        print("Updates a class intance with new information")
        print("[usage]: update <ClassName> <Id> <AtrrName> <AttrValue>\n")

    def count(self, cmd):
        """
        counts the number of instances of a class
        """
        all_objects = storage.all()
        count = 0

        for k in all_objects:
            if cmd in k:
                count += 1
        print(count)

    def default(self, cmd):
        """
        Handles class commands
        """
        line = cmd[:]
        if not("." in line and "(" in line and ")" in line):
            print(f"*** Unknown syntax: {cmd}")
            return
        cls_name = line[: line.find(".", 1)]
        if cls_name not in self.class_list:
            print(f"*** Unknown syntax: {line}")
            return
        comd = line[line.find(".", 1) + 1 : line.find("(", 1)]
        if comd not in self.dots:
            print(f"*** Unknown syntax: {line}")
            return
        if comd == "all":
            self.do_all(cls_name)
        if comd == "count":
            self.count(cls_name)
        if comd == "show":
            id = line[line.find("(", 1) + 1 : line.find(")", 1)]
            joined_command = " ".join([cls_name, id])
            self.do_show(joined_command)
        if comd == "destroy":
            id = line[line.find("(", 1) + 1 : line.find(")", 1)]
            joined_command = " ".join([cls_name, id])
            self.do_destroy(joined_command)
        if comd == "update":
            arg = line[line.find("(") + 1 : line.find(")")]
            arg = arg.split(",")
            id = arg[0].strip()
            attr_name = arg[1].strip()
            attr_value = arg[2].strip()
            joined = " ".join([cls_name, id, attr_name, attr_value])
            self.do_update(joined)
if __name__ == "__main__":
    HBNBCommand().cmdloop()
