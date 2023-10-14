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

    def do_create(self, args):
        """ Create an object of any class"""
        try:
            if not args:
                raise SyntaxError()
            arg_list = args.split(" ")
            kw = {}
            for arg in arg_list[1:]:
                arg_splited = arg.split("=")
                arg_splited[1] = eval(arg_splited[1])
                if type(arg_splited[1]) is str:
                    arg_splited[1] = arg_splited[1].replace("_", " ").replace('"', '\\"')
                kw[arg_splited[0]] = arg_splited[1]
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        new_instance = HBNBCommand.class_list[arg_list[0]](**kw)
        new_instance.save()
        print(new_instance.id)

        """def do_create(self, cmd=None):
        Creates a new instance of BaseModel saves it
        to json file and prints out the id of the instance
        if not cmd:
            print("** class name missing **")
        elif cmd not in self.class_list:
            print("** class doesn't exist **")
        else:
            new = eval(cmd)()
            new.save()
            print(f"{new.id}")"""

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

    def do_all(self, cmd=None):
        """
        Prints all instances of the class name is absent
        else prints all the instances of the given class
        """
        all_objects = storage.all()

        if not cmd:
            for k in all_objects:
                print([str(all_objects[k])])
        else:
            cmd_list = cmd.split(" ")
            if len(cmd_list) < 1:
                print("** class name missing **")
            else:
                class_name = cmd_list[0]
                if class_name not in self.class_list:
                    print("** class doesn't exist **")
                else:
                    for k, v in all_objects.items():
                        if k.split('.')[0] == class_name:
                            print([str(v)])

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


if __name__ == "__main__":
    HBNBCommand().cmdloop()
