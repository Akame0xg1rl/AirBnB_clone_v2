import cmd
import sys
import shlex
from models.base_model import BaseModel
from models.__init__ import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import re

class HBNBCommand(cmd.Cmd):
    """Contains the functionality for the HBNB console"""

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''
    classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
    }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    def preloop(self):
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def postcmd(self, stop, line):
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        exit()

    def help_quit(self):
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        print()
        exit()

    def help_EOF(self):
        print("Exits the program without formatting\n")

    def emptyline(self):
        pass

    def do_create(self, args):
        """Create an object of any class with given parameters"""
        if not args:
            print("** class name missing **")
            return

        args_list = shlex.split(args)
        class_name = args_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        # Parse parameters
        kwargs = {}
        for arg in args_list[1:]:
            if '=' in arg:
                key_val = arg.split('=')
                key = key_val[0]
                val = key_val[1]
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]  # remove surrounding quotes
                    val = val.replace('_', ' ')  # replace underscores with spaces
                elif '.' in val:
                    try:
                        val = float(val)
                    except ValueError:
                        continue  # skip invalid float
                else:
                    try:
                        val = int(val)
                    except ValueError:
                        continue  # skip invalid integer
                kwargs[key] = val

        # Create instance with parsed kwargs
        new_instance = self.classes[class_name](**kwargs)
        new_instance.save()  # Assuming save method exists in BaseModel
        print(new_instance.id)

    def help_create(self):
        print("Creates a class of any type with parameters")
        print("[Usage]: create <className> <key1>=<value1> <key2>=<value2> ...\n")

    def do_show(self, args):
        """Shows an object based on class name and id"""
        if not args:
            print("** class name missing **")
            return

        args_list = shlex.split(args)
        class_name = args_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args_list) < 2:
            print("** instance id missing **")
            return

        obj_id = args_list[1]
        key = "{}.{}".format(class_name, obj_id)
        if key in storage.all():
            print(storage.all()[key])
        else:
            print("** no instance found **")

    def help_show(self):
        print("Shows an instance of a class based on its ID")
        print("[Usage]: show <className> <instanceId>\n")

    def do_destroy(self, args):
        """Deletes an object based on class name and id"""
        if not args:
            print("** class name missing **")
            return

        args_list = shlex.split(args)
        class_name = args_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args_list) < 2:
            print("** instance id missing **")
            return

        obj_id = args_list[1]
        key = "{}.{}".format(class_name, obj_id)
        if key in storage.all():
            del storage.all()[key]
            storage.save()
        else:
            print("** no instance found **")

    def help_destroy(self):
        print("Deletes an instance of a class based on its ID")
        print("[Usage]: destroy <className> <instanceId>\n")

    def do_all(self, args):
        """Prints all instances of a class or all classes if no class is provided"""
        args_list = shlex.split(args)
        if args and args_list[0] not in self.classes:
            print("** class doesn't exist **")
            return

        obj_list = []
        if args:
            for key, obj in storage.all().items():
                if key.split('.')[0] == args_list[0]:
                    obj_list.append(str(obj))
        else:
            for obj in storage.all().values():
                obj_list.append(str(obj))

        print(obj_list)

    def help_all(self):
        print("Prints all instances of a class or all classes if no class is provided")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Counts instances of a class"""
        if not args:
            print("** class name missing **")
            return

        args_list = shlex.split(args)
        class_name = args_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        count = 0
        for key in storage.all():
            if key.split('.')[0] == class_name:
                count += 1
        print(count)

    def help_count(self):
        print("Counts instances of a class")
        print("[Usage]: count <className>\n")

    def do_update(self, args):
        """Updates an instance based on class name and id"""
        if not args:
            print("** class name missing **")
            return

        args_list = shlex.split(args)
        class_name = args_list[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        if len(args_list) < 2:
            print("** instance id missing **")
            return

        obj_id = args_list[1]
        key = "{}.{}".format(class_name, obj_id)
        if key not in storage.all():
            print("** no instance found **")
            return

        if len(args_list) < 3:
            print("** attribute name missing **")
            return

        if len(args_list) < 4:
            print("** value missing **")
            return

        attr_name = args_list[2]
        attr_value = args_list[3]

        try:
            attr_value = eval(attr_value)  # Try to evaluate as Python literal
        except (NameError, SyntaxError):
            pass  # If not a valid literal, keep as string

        setattr(storage.all()[key], attr_name, attr_value)
        storage.all()[key].save()

    def help_update(self):
        print("Updates an instance of a class with new attributes")
        print("[Usage]: update <className> <instanceId> <attributeName> <attributeValue>\n")

if __name__ == "__main__":
    HBNBCommand().cmdloop()
