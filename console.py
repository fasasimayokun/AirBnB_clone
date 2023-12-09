#!/usr/bin/python3
""" a prog called console.py that contains the entry point
of the command interpreter"""

import cmd
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import re


def pars(arg):
    c_braces = re.search(r"\{(.*?)\}", arg)
    sq_braces = re.search(r"\[(.*?)\]", arg)
    if c_braces is None:
        if sq_braces is None:
            return [nm.strip(',') for nm in split(arg)]
        else:
            token = split(arg[:sq_braces.span()[0]])
            ret = [nm.strip(',') for nm in token]
            ret.append(sq_braces.group())
            return ret
    else:
        token = split(arg[:c_braces.span()[0]])
        ret = [nm.strip(',') for nm in token]
        ret.append(c_braces.group())
        return ret


class HBNBCommand(cmd.Cmd):
    """defines the hobertonbnb command interpreter interface"""
    prompt = "(hbnb) "
    __clss = {
            "BaseModel",
            "User",
            "State",
            "City",
            "Place",
            "Amenity",
            "Review"
            }

    def default(self, cmad):
        """the method that respond to default behavior for invalid input"""
        cmadict = {
                "all": self.do_all,
                "show": self.do_show,
                "destroy": self.do_destroy,
                "count": self.do_count,
                "update": self.do_update
                }
        march = re.search(r'\.', cmad)
        if march is not None:
            val = [cmad[:march.span()[0]], cmad[march.span()[1]:]]
            march = re.search(r'\((.*?)\)', val[1])
            if march is not None:
                cm = [val[1][:march.span()[0]], march.group()[1:-1]]
                if cm[0] in cmadict.keys():
                    invk = '{} {}'.format(val[0], cm[1])
                    return cmadict[cm[0]](invk)
        print('*** Unknown syntax: {}'.format(cmad))
        return False

    def emptyline(self):
        """a method the handles an empty line."""
        pass

    def do_quit(self, cmad):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, cmad):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, val):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        cm = pars(val)
        if len(cm) == 0:
            print('** class name missing **')
        elif cm[0] not in HBNBCommand.__clss:
            print('** class doesn\'t exist **')
        else:
            print(eval(cm[0])().id)
            storage.save()

    def do_show(self, val):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        cm = pars(val)
        insdict = storage.all()
        if len(cm) == 0:
            print('** class name missing **')
        elif cm[0] not in HBNBCommand.__clss:
            print('** class doesn\'t exist **')
        elif len(cm) == 1:
            print('** instance id missing **')
        elif "{}.{}".format(cm[0], cm[1]) not in insdict:
            print('** no instance found **')
        else:
            print(insdict['{}.{}'.format(cm[0], cm[1])])

    def do_destroy(self, val):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        cm = pars(val)
        insdict = storage.all()
        if len(cm) == 0:
            print('** class name missing **')
        elif cm[0] not in HBNBCommand.__clss:
            print('** class doesn\'t exist **')
        elif len(cm) == 1:
            print('** instance id missing **')
        elif '{}.{}'.format(cm[0], cm[1]) not in insdict.keys():
            print('** no instance found **')
        else:
            del insdict["{}.{}".format(cm[0], cm[1])]
            storage.save()

    def do_all(self, val):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        cm = pars(val)
        if len(cm) > 0 and cm[0] not in HBNBCommand.__clss:
            print('** class doesn\'t exist **')
        else:
            cm1 = []
            for ins in storage.all().values():
                if len(cm) > 0 and cm[0] == ins.__class__.__name__:
                    cm1.append(ins.__str__())
                elif len(cm) == 0:
                    cm1.append(ins.__str__())
            print(cm1)

    def do_count(self, val):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        cm = pars(val)
        cnt = 0
        for ins in storage.all().values():
            if cm[0] == ins.__class__.__name__:
                cnt += 1
        print(cnt)

    def do_update(self, val):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        cm = pars(val)
        insdict = storage.all()

        if len(cm) == 0:
            print('** class name missing **')
            return False
        if cm[0] not in HBNBCommand.__clss:
            print('** class doesn\'t exist **')
            return False
        if len(cm) == 1:
            print('** instance id missing **')
            return False
        if '{}.{}'.format(cm[0], cm[1]) not in insdict.keys():
            print('** no instance found **')
            return False
        if len(cm) == 2:
            print('** attribute name missing **')
            return False
        if len(cm) == 3:
            try:
                type(eval(cm[2])) != dict
            except NameError:
                print('** value missing **')
                return False
        if len(cm) == 4:
            ins = insdict['{}.{}'.format(cm[0], cm[1])]
            if cm[2] in ins.__class__.__dict__.keys():
                vtype = type(ins.__class__.__dict__[cm[2]])
                ins.__dict__[cm[2]] = vtype(cm[3])
            else:
                ins.__dict__[cm[2]] = cm[3]
        elif type(eval(cm[2])) == dict:
            ins = insdict['{}.{}'.format(cm[0], cm[1])]
            for ky, val in eval(cm[2]).items():
                if (ky in ins.__class__.__dict__.keys() and
                        type(ins.__class__.__dict__[ky] in {str, int, float})):
                    vtype = type(ins.__class__.__dict__[ky])
                    ins.__dict__[ky] = vtype(val)
                else:
                    ins.__dict__[ky] = val
            storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
