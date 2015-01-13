from __future__ import print_function

import six

"""
Metaclass for Structs

inspired by the Django ORM internals

"""
class MetaStruct(type):
    def __new__(cls, name, bases, attrs):

        super_new = super(MetaStruct, cls).__new__

        print(cls, name, bases, attrs)

        return super_new(cls, name, bases, attrs)
        

class Struct(six.with_metaclass(MetaStruct)):
    pass

class Field(object):
    pass

class String(Field):
    pass
