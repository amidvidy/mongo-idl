from __future__ import print_function

import six

def gen():
    print("Generating output...")
    # dummy for now

"""
Metaclass for Structs

inspired by the Django ORM internals

"""
class MetaStruct(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(MetaStruct, cls).__new__
        return super_new(cls, name, bases, attrs)

class Struct(six.with_metaclass(MetaStruct)):
    pass

class Field(object):
    def __init__(self, *args, **kwargs):
        pass

class String(Field):
    pass

class Document(Field):
    pass

class Long(Field):
    pass

class Array(Field):
    def __init__(self, *args, **kwargs):
        pass

class Bool(Field):
    pass
