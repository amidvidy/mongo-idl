from __future__ import print_function

import six

env = {}

def gen():
    print("Generating output...")
    print(env)
    # dummy for now

"""
Metaclass for Structs

inspired by the Django ORM internals

"""
class IdlError(Exception):
    pass

def raise_error_on_init(cls, *args, **kwargs):
    raise IdlError("Cannot create instances of an idl definition.")

class MetaStruct(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(MetaStruct, cls).__new__
        if attrs.get('__abstract__', False):
            return super_new(cls, name, bases, attrs)

        # Don't let users actually create instances of Structs
        attrs['__init__'] = raise_error_on_init

        # Construct the struct
        struct_cls = super_new(cls, name, bases, attrs)
        
        # Add to environment
        env[name] = struct_cls

        return struct_cls


class Struct(six.with_metaclass(MetaStruct)):
    __abstract__ = True

class Field(object):
    def __init__(self, *args, **kwargs):
        pass

class String(Field):
    pass

class Document(Field):
    def __init__(self, *args, **kwargs):
        self.fields = kwargs
        super(Document, self).__init__(self, *args, **kwargs)

class Long(Field):
    pass

class Array(Field):
    def __init__(self, *args, **kwargs):
        pass

class Bool(Field):
    pass
