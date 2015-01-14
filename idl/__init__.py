from __future__ import print_function

import six
import mako

"""
Structs that have been defined are stored here
"""
env = {}

"""
Returns the fields from a struct object
"""
def get_fields(cls):
    return (attr for attr in dir(cls) if not attr.startswith('__'))

"""
This will generate code for all the structs that we have defined.
"""
def gen():
    print("Generating output...")
    for (name, cls) in env.iteritems():
        print("Generating code for {}".format(name))
        for field in get_fields(cls):
            print("Got field: {}".format(field))
            print(getattr(cls, field))

"""
Base exception for all mongo-idl exceptions
"""
class IdlError(Exception):
    pass

"""
Dummy init method so that people don't instantiate struct classes.
"""
def raise_error_on_init(cls, *args, **kwargs):
    raise IdlError("Cannot create instances of an idl definition.")

"""
The metaclass for all Structs.
inspired by the Django ORM internals
"""
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


"""
Base class for all Structs. Users inherit from this
to define their own message types.
"""
class Struct(six.with_metaclass(MetaStruct)):
    __abstract__ = True

    def _generate(self, *args, **kwargs):
        fields = get_fields(self.__class__)
        pass


class Field(object):
    def __init__(self, *args, **kwargs):
        pass

    def _field(self, name):
        return """
        {1] _{0};
        """.format(name, self._type)

    def _getter(self, name):
        return """
        {1} get_{0} {
            return _{0}
        }
        """.format(name, self._type)

    def _setter(self, name):
        return """
        void set_{0}({1}& {0}) {
           _{0} = {0};
        }
        """.format(name, self._type)


class String(Field):
    def __init__(self, *args, **kwargs):
        self._type = 'std::string'
        super(String, self).__init__(self, *args, **kwargs)

class Document(Field):
    def __init__(self, *args, **kwargs):
        self.fields = kwargs
        super(Document, self).__init__(self, *args, **kwargs)


class Long(Field):
    def __init__(self, *args, **kwargs):
        self._type = 'long'
        super(Long, self).__init__(self, *args, **kwargs)


class Array(Field):
    def __init__(self, *args, **kwargs):
        pass


class Bool(Field):
    def __init__(self, *args, **kwargs):
        self._type = 'bool'
        super(Bool, self).__init__(self, *args, **kwargs)
